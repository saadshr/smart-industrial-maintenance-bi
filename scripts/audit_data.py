"""Reproducible, read-only audit of the MetroPT-3 CSV dataset.

The script reads the CSV in chunks and writes a JSON report to stdout.
It never modifies the source CSV. Complete-row duplicates are detected
through stable pandas row hashes; repeated hashes are counted as duplicate
row candidates and should be reviewed if present.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd
from pypdf import PdfReader


ANALOG_COLUMNS = [
    "TP2",
    "TP3",
    "H1",
    "DV_pressure",
    "Reservoirs",
    "Oil_temperature",
    "Motor_current",
]

DIGITAL_COLUMNS = [
    "COMP",
    "DV_eletric",
    "Towers",
    "MPG",
    "LPS",
    "Pressure_switch",
    "Oil_level",
    "Caudal_impulses",
]

TECHNICAL_COLUMNS = ["Unnamed: 0", "timestamp"]


def json_number(value: float) -> float | None:
    """Return JSON-safe finite numbers."""
    return value if math.isfinite(value) else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("data/raw/MetroPT3(AirCompressor).csv"),
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        default=Path("data/raw/Data Description_Metro.pdf"),
    )
    parser.add_argument("--chunksize", type=int, default=100_000)
    return parser.parse_args()


def audit_pdf(pdf_path: Path) -> dict[str, Any]:
    reader = PdfReader(str(pdf_path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return {
        "exists": pdf_path.exists(),
        "size_bytes": pdf_path.stat().st_size,
        "pages": len(reader.pages),
        "text_length": len(text),
        "signal_names_found": [
            name for name in ANALOG_COLUMNS + DIGITAL_COLUMNS if name in text
        ],
    }


def audit_csv(csv_path: Path, chunksize: int) -> dict[str, Any]:
    header = pd.read_csv(csv_path, nrows=0)
    columns = header.columns.tolist()
    expected_columns = TECHNICAL_COLUMNS + ANALOG_COLUMNS + DIGITAL_COLUMNS
    missing_expected = [name for name in expected_columns if name not in columns]
    unexpected = [name for name in columns if name not in expected_columns]

    row_count = 0
    null_counts = Counter()
    dtype_names: dict[str, set[str]] = {name: set() for name in columns}
    row_hash_counts: Counter[int] = Counter()
    timestamp_counts: Counter[str] = Counter()
    interval_counts: Counter[float] = Counter()
    first_timestamp: pd.Timestamp | None = None
    last_timestamp: pd.Timestamp | None = None
    previous_timestamp: pd.Timestamp | None = None
    non_increasing_intervals = 0
    technical_index_values: list[int] = []
    analog_state: dict[str, dict[str, float]] = {
        name: {"count": 0, "sum": 0.0, "sum_sq": 0.0, "min": math.inf, "max": -math.inf}
        for name in ANALOG_COLUMNS
    }
    digital_counts: dict[str, Counter[str]] = {name: Counter() for name in DIGITAL_COLUMNS}

    for chunk in pd.read_csv(csv_path, chunksize=chunksize, low_memory=False):
        row_count += len(chunk)
        for name, dtype in chunk.dtypes.items():
            dtype_names[name].add(str(dtype))

        null_counts.update(chunk.isna().sum().to_dict())
        row_hashes = pd.util.hash_pandas_object(chunk, index=False)
        row_hash_counts.update(int(value) for value in row_hashes)
        technical_index_values.extend(chunk["Unnamed: 0"].astype("int64").tolist())

        timestamps = pd.to_datetime(chunk["timestamp"], errors="coerce")
        valid_timestamps = timestamps.dropna()
        if not valid_timestamps.empty:
            current_first = valid_timestamps.iloc[0]
            current_last = valid_timestamps.iloc[-1]
            first_timestamp = current_first if first_timestamp is None else min(first_timestamp, current_first)
            last_timestamp = current_last if last_timestamp is None else max(last_timestamp, current_last)
            timestamp_counts.update(
                timestamps.dropna().dt.strftime("%Y-%m-%dT%H:%M:%S.%f").tolist()
            )

            ordered = timestamps.tolist()
            if previous_timestamp is not None and ordered:
                delta = (ordered[0] - previous_timestamp).total_seconds()
                interval_counts[delta] += 1
                if delta <= 0:
                    non_increasing_intervals += 1
            for left, right in zip(ordered, ordered[1:]):
                if pd.isna(left) or pd.isna(right):
                    continue
                delta = (right - left).total_seconds()
                interval_counts[delta] += 1
                if delta <= 0:
                    non_increasing_intervals += 1
            previous_timestamp = ordered[-1]

        for name in ANALOG_COLUMNS:
            values = pd.to_numeric(chunk[name], errors="coerce").dropna()
            state = analog_state[name]
            state["count"] += int(values.size)
            if not values.empty:
                state["sum"] += float(values.sum())
                state["sum_sq"] += float((values * values).sum())
                state["min"] = min(state["min"], float(values.min()))
                state["max"] = max(state["max"], float(values.max()))

        for name in DIGITAL_COLUMNS:
            digital_counts[name].update(
                chunk[name].dropna().map(str).value_counts().to_dict()
            )

    analog_stats: dict[str, dict[str, float | int | None]] = {}
    for name, state in analog_state.items():
        count = int(state["count"])
        mean = state["sum"] / count if count else None
        variance = (
            (state["sum_sq"] - count * mean * mean) / (count - 1)
            if count > 1 and mean is not None
            else None
        )
        analog_stats[name] = {
            "count": count,
            "min": json_number(state["min"]) if count else None,
            "max": json_number(state["max"]) if count else None,
            "mean": json_number(mean) if mean is not None else None,
            "std": json_number(math.sqrt(max(variance, 0.0))) if variance is not None else None,
        }

    interval_mode = interval_counts.most_common(1)[0][0] if interval_counts else None
    gap_count = (
        sum(count for interval, count in interval_counts.items() if interval > interval_mode)
        if interval_mode is not None
        else None
    )
    duplicate_hash_rows = sum(
        count for count in row_hash_counts.values() if count > 1
    )
    duplicate_hash_groups = sum(
        1 for count in row_hash_counts.values() if count > 1
    )
    repeated_timestamp_rows = sum(
        count for count in timestamp_counts.values() if count > 1
    )
    repeated_timestamp_values = sum(
        1 for count in timestamp_counts.values() if count > 1
    )
    largest_intervals = sorted(
        ((interval, count) for interval, count in interval_counts.items()),
        reverse=True,
    )[:10]
    index_series = pd.Series(technical_index_values, dtype="int64")

    return {
        "file": str(csv_path),
        "size_bytes": csv_path.stat().st_size,
        "rows": row_count,
        "columns_count": len(columns),
        "columns": columns,
        "expected_columns_missing": missing_expected,
        "unexpected_columns": unexpected,
        "technical_index": {
            "column": "Unnamed: 0",
            "min": int(index_series.min()),
            "max": int(index_series.max()),
            "unique": int(index_series.nunique()),
            "duplicate_values": int(index_series.duplicated().sum()),
            "strictly_sequential": bool(
                index_series.equals(pd.Series(range(len(index_series)), dtype="int64"))
            ),
        },
        "dtypes": {name: sorted(values) for name, values in dtype_names.items()},
        "null_counts": dict(null_counts),
        "total_nulls": int(sum(null_counts.values())),
        "first_timestamp": first_timestamp.isoformat() if first_timestamp is not None else None,
        "last_timestamp": last_timestamp.isoformat() if last_timestamp is not None else None,
        "timestamp_parse_failures": int(row_count - sum(timestamp_counts.values())),
        "repeated_timestamps": {
            "rows_in_repeated_groups": repeated_timestamp_rows,
            "distinct_repeated_values": repeated_timestamp_values,
        },
        "duplicate_row_hashes": {
            "rows_in_duplicate_groups": duplicate_hash_rows,
            "duplicate_groups": duplicate_hash_groups,
        },
        "temporal_intervals_seconds": {
            "mode": interval_mode,
            "min": min(interval_counts) if interval_counts else None,
            "max": max(interval_counts) if interval_counts else None,
            "non_increasing_count": non_increasing_intervals,
            "interval_counts": {str(key): value for key, value in sorted(interval_counts.items())},
            "gaps_greater_than_mode": gap_count,
            "largest_intervals_seconds": [
                {"seconds": interval, "count": count}
                for interval, count in largest_intervals
            ],
        },
        "analog_statistics": analog_stats,
        "digital_distributions": {
            name: dict(sorted(counts.items())) for name, counts in digital_counts.items()
        },
    }


def main() -> None:
    args = parse_args()
    for path in (args.csv, args.pdf):
        if not path.exists():
            raise FileNotFoundError(path)
    report = {
        "audit": "MetroPT-3",
        "chunksize": args.chunksize,
        "csv": audit_csv(args.csv, args.chunksize),
        "pdf": audit_pdf(args.pdf),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
