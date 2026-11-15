"""Prepare the four Power BI tables from the original MetroPT-3 CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import csv
from datetime import datetime, timedelta


FAILURES = [
    (1, "Report #1", "2020-04-18 00:00:00", "2020-04-18 23:59:00", "Air leak", "High stress", "Non indiquée"),
    (2, "Report #2", "2020-05-29 23:30:00", "2020-05-30 06:00:00", "Air leak", "High stress", "Maintenance on 30Apr at 12:00"),
    (3, "Report #3", "2020-06-05 10:00:00", "2020-06-07 14:30:00", "Air leak", "High stress", "Maintenance on 8Jun at 16:00"),
    (4, "Report #4", "2020-07-15 14:30:00", "2020-07-15 19:00:00", "Air leak", "High stress", "Maintenance on 16Jul at 00:00"),
]


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=root / "data/raw/MetroPT3(AirCompressor).csv")
    parser.add_argument("--output-dir", type=Path, default=root / "data/processed")
    parser.add_argument("--chunksize", type=int, default=100_000)
    return parser.parse_args()


FAILURE_BOUNDS = [
    (key, datetime.fromisoformat(start), datetime.fromisoformat(end))
    for key, _code, start, end, *_ in FAILURES
]


def failure_key_for(timestamp: datetime) -> str:
    for key, start, end in FAILURE_BOUNDS:
        if start <= timestamp <= end:
            return str(key)
    return ""


def write_dimensions(output_dir: Path, first_date: datetime, last_date: datetime) -> None:
    with (output_dir / "DimDate.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["DateKey", "CalendarDate", "Year", "QuarterNumber", "MonthNumber", "MonthName", "DayOfMonth"])
        current = first_date.date()
        while current <= last_date.date():
            writer.writerow([current.strftime("%Y%m%d"), current.isoformat(), current.year, (current.month - 1) // 3 + 1, current.month, current.strftime("%B"), current.day])
            current += timedelta(days=1)

    with (output_dir / "DimTime.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["TimeKey", "TimeLabel", "Hour", "Minute", "Second", "TimeBucket"])
        for seconds in range(86_400):
            hour, remainder = divmod(seconds, 3600)
            minute, second = divmod(remainder, 60)
            writer.writerow([seconds, f"{hour:02d}:{minute:02d}:{second:02d}", hour, minute, second, f"{hour:02d}:00-{hour:02d}:59"])


def write_failure_periods(output_dir: Path) -> None:
    rows = []
    for key, code, start, end, failure_type, severity, note in FAILURES:
        start_ts = datetime.fromisoformat(start)
        end_ts = datetime.fromisoformat(end)
        rows.append({
            "FailurePeriodKey": key,
            "FailureReportCode": code,
            "StartTimestamp": start_ts,
            "EndTimestamp": end_ts,
            "StartDateKey": int(start_ts.strftime("%Y%m%d")),
            "EndDateKey": int(end_ts.strftime("%Y%m%d")),
            "FailureType": failure_type,
            "Severity": severity,
            "MaintenanceNoteRaw": note,
            "SourceReference": "Data Description_Metro.pdf; docs/data_audit.md",
            "DurationSeconds": (end_ts - start_ts).total_seconds(),
            "FailurePeriodCount": 1,
        })
    with (output_dir / "FactFailurePeriod.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def prepare(input_path: Path, output_dir: Path, chunksize: int) -> None:
    if not input_path.exists():
        raise FileNotFoundError(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    fact_path = output_dir / "FactSensorObservation.csv"
    if fact_path.exists():
        fact_path.unlink()

    first_date = None
    last_date = None
    observation_key = 1
    observation_count = 0
    with input_path.open(newline="", encoding="utf-8-sig") as source, fact_path.open("w", newline="", encoding="utf-8") as target:
        reader = csv.DictReader(source)
        source_key_name = (reader.fieldnames or [""])[0]
        fields = ["ObservationKey", "SourceRowKey", "DateKey", "TimeKey", "ObservationTimestamp", "FailurePeriodKey", "ObservationCount"] + [name for name in (reader.fieldnames or [])[1:] if name != "timestamp"]
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        for row_number, row in enumerate(reader, start=1):
            timestamp = datetime.fromisoformat(row["timestamp"])
            row_out = {
                "ObservationKey": row_number,
                "SourceRowKey": row[source_key_name],
                "DateKey": timestamp.strftime("%Y%m%d"),
                "TimeKey": timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second,
                "ObservationTimestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "FailurePeriodKey": failure_key_for(timestamp),
                "ObservationCount": 1,
            }
            for name in fields[7:]:
                value = row[name]
                if name not in {"COMP", "DV_eletric", "Towers", "MPG", "LPS", "Pressure_switch", "Oil_level", "Caudal_impulses"}:
                    try:
                        value = format(float(value), ".6g")
                    except ValueError:
                        pass
                row_out[name] = value
            writer.writerow(row_out)
            observation_count += 1
            first_date = timestamp if first_date is None else min(first_date, timestamp)
            last_date = timestamp if last_date is None else max(last_date, timestamp)

    assert first_date is not None and last_date is not None
    write_dimensions(output_dir, first_date, last_date)
    write_failure_periods(output_dir)
    print(f"FactSensorObservation: {observation_count:,} rows")
    print(f"FactFailurePeriod: {len(FAILURES)} rows")
    print(f"DimDate: {(last_date.date() - first_date.date()).days + 1:,} rows")
    print("DimTime: 86,400 rows")


if __name__ == "__main__":
    args = parse_args()
    prepare(args.input, args.output_dir, args.chunksize)
