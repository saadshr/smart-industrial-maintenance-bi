let
    Source = #table(
        {"FailurePeriodKey", "FailureReportCode", "StartTimestamp", "EndTimestamp", "StartDateKey", "EndDateKey", "FailureType", "Severity", "MaintenanceNoteRaw", "SourceReference", "DurationSeconds", "FailurePeriodCount"},
        {
            {1, "Report #1", #datetime(2020,4,18,0,0,0), #datetime(2020,4,18,23,59,0), 20200418, 20200418, "Air leak", "High stress", "Non indiquée", "Data Description_Metro.pdf; docs/data_audit.md", 86340, 1},
            {2, "Report #2", #datetime(2020,5,29,23,30,0), #datetime(2020,5,30,6,0,0), 20200529, 20200530, "Air leak", "High stress", "Maintenance on 30Apr at 12:00", "Data Description_Metro.pdf; docs/data_audit.md", 23400, 1},
            {3, "Report #3", #datetime(2020,6,5,10,0,0), #datetime(2020,6,7,14,30,0), 20200605, 20200607, "Air leak", "High stress", "Maintenance on 8Jun at 16:00", "Data Description_Metro.pdf; docs/data_audit.md", 189000, 1},
            {4, "Report #4", #datetime(2020,7,15,14,30,0), #datetime(2020,7,15,19,0,0), 20200715, 20200715, "Air leak", "High stress", "Maintenance on 16Jul at 00:00", "Data Description_Metro.pdf; docs/data_audit.md", 16200, 1}
        }
    ),
    Typed = Table.TransformColumnTypes(Source, {{"FailurePeriodKey", Int64.Type}, {"StartTimestamp", type datetime}, {"EndTimestamp", type datetime}, {"StartDateKey", Int64.Type}, {"EndDateKey", Int64.Type}, {"DurationSeconds", type number}, {"FailurePeriodCount", Int64.Type}})
in
    Typed
