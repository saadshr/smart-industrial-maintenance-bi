let
    Source = FactSensorObservation,
    Dates = Table.Distinct(Table.SelectColumns(Source, {"DateKey"})),
    AddCalendarDate = Table.AddColumn(Dates, "CalendarDate", each #date(Number.IntegerDivide([DateKey], 10000), Number.Mod(Number.IntegerDivide([DateKey], 100), 100), Number.Mod([DateKey], 100)), type date),
    AddYear = Table.AddColumn(AddCalendarDate, "Year", each Date.Year([CalendarDate]), Int64.Type),
    AddQuarter = Table.AddColumn(AddYear, "QuarterNumber", each Date.QuarterOfYear([CalendarDate]), Int64.Type),
    AddMonthNumber = Table.AddColumn(AddQuarter, "MonthNumber", each Date.Month([CalendarDate]), Int64.Type),
    AddMonthName = Table.AddColumn(AddMonthNumber, "MonthName", each Date.MonthName([CalendarDate], "fr-FR"), type text),
    AddDay = Table.AddColumn(AddMonthName, "DayOfMonth", each Date.Day([CalendarDate]), Int64.Type)
in
    AddDay
