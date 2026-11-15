let
    Source = Csv.Document(File.Contents(pSourceFolder & "\MetroPT3(AirCompressor).csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Renamed = Table.RenameColumns(PromotedHeaders, {{"Unnamed: 0", "SourceRowKey"}, {"timestamp", "ObservationTimestamp"}}),
    Typed = Table.TransformColumnTypes(Renamed, {
        {"SourceRowKey", Int64.Type}, {"ObservationTimestamp", type datetime},
        {"TP2", type number}, {"TP3", type number}, {"H1", type number}, {"DV_pressure", type number},
        {"Reservoirs", type number}, {"Oil_temperature", type number}, {"Motor_current", type number},
        {"COMP", Int64.Type}, {"DV_eletric", Int64.Type}, {"Towers", Int64.Type}, {"MPG", Int64.Type},
        {"LPS", Int64.Type}, {"Pressure_switch", Int64.Type}, {"Oil_level", Int64.Type}, {"Caudal_impulses", Int64.Type}
    }),
    AddObservationKey = Table.AddIndexColumn(Typed, "ObservationKey", 1, 1, Int64.Type),
    AddDateKey = Table.AddColumn(AddObservationKey, "DateKey", each Date.Year(Date.From([ObservationTimestamp])) * 10000 + Date.Month(Date.From([ObservationTimestamp])) * 100 + Date.Day(Date.From([ObservationTimestamp])), Int64.Type),
    AddTimeKey = Table.AddColumn(AddDateKey, "TimeKey", each Time.Hour(Time.From([ObservationTimestamp])) * 3600 + Time.Minute(Time.From([ObservationTimestamp])) * 60 + Time.Second(Time.From([ObservationTimestamp])), Int64.Type),
    AddFailurePeriodKey = Table.AddColumn(AddTimeKey, "FailurePeriodKey", each
        if [ObservationTimestamp] >= #datetime(2020, 4, 18, 0, 0, 0) and [ObservationTimestamp] <= #datetime(2020, 4, 18, 23, 59, 0) then 1
        else if [ObservationTimestamp] >= #datetime(2020, 5, 29, 23, 30, 0) and [ObservationTimestamp] <= #datetime(2020, 5, 30, 6, 0, 0) then 2
        else if [ObservationTimestamp] >= #datetime(2020, 6, 5, 10, 0, 0) and [ObservationTimestamp] <= #datetime(2020, 6, 7, 14, 30, 0) then 3
        else if [ObservationTimestamp] >= #datetime(2020, 7, 15, 14, 30, 0) and [ObservationTimestamp] <= #datetime(2020, 7, 15, 19, 0, 0) then 4
        else null, Int64.Type),
    AddObservationCount = Table.AddColumn(AddFailurePeriodKey, "ObservationCount", each 1, Int64.Type)
in
    AddObservationCount
