let
    Seconds = List.Numbers(0, 86400),
    Source = Table.FromList(Seconds, Splitter.SplitByNothing(), {"TimeKey"}),
    AddTime = Table.AddColumn(Source, "TimeLabel", each Time.ToText(#time(Number.IntegerDivide([TimeKey], 3600), Number.IntegerDivide(Number.Mod([TimeKey], 3600), 60), Number.Mod([TimeKey], 60)), "HH:mm:ss"), type text),
    AddHour = Table.AddColumn(AddTime, "Hour", each Number.IntegerDivide([TimeKey], 3600), Int64.Type),
    AddMinute = Table.AddColumn(AddHour, "Minute", each Number.IntegerDivide(Number.Mod([TimeKey], 3600), 60), Int64.Type),
    AddSecond = Table.AddColumn(AddMinute, "Second", each Number.Mod([TimeKey], 60), Int64.Type),
    AddBucket = Table.AddColumn(AddSecond, "TimeBucket", each Text.PadStart(Text.From([Hour]), 2, "0") & ":00-" & Text.PadStart(Text.From([Hour]), 2, "0") & ":59", type text)
in
    AddBucket
