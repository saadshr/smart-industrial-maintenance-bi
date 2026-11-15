# Catalogue des visuels Power BI

## Vue générale

- Cartes : Nombre observations, Nombre incidents documentés, Observations dans incidents documentés, Taux observations incidentées.
- Courbe : axe DimDate[CalendarDate], valeur Nombre observations ; filtres DimDate[Year], DimDate[MonthName].
- Histogramme : axe FactFailurePeriod[FailureReportCode], valeur FactFailurePeriod[DurationSeconds] ; formater l'axe ou la colonne en heures dans Power Query/Power BI.
- Segmenteurs : DimDate[Year], DimDate[MonthName], FactFailurePeriod[FailureReportCode].

## Surveillance des capteurs

- Courbe TP3 : axe FactSensorObservation[ObservationTimestamp], valeur AVERAGE(FactSensorObservation[TP3]) ; filtres DimDate, DimTime[Hour].
- Courbes séparées : axe ObservationTimestamp, valeurs moyennes TP2, TP3, H1, Reservoirs ; ne pas mélanger les unités avec Oil_temperature.
- Courbe température/courant : deux visuels séparés avec AVERAGE(Oil_temperature) et AVERAGE(Motor_current) ; filtre de date et heure.
- Matrice temporelle : lignes DimDate[CalendarDate], valeurs Nombre observations, AVERAGE(Motor_current).

## Analyse des incidents et OLAP

- Table des incidents : FailureReportCode, StartTimestamp, EndTimestamp, FailureType, Severity, DurationSeconds, MaintenanceNoteRaw.
- Colonnes empilées : axe DimDate[CalendarDate], légende FactSensorObservation[FailurePeriodKey], valeur Nombre observations ; le blanc signifie hors fenêtre documentée, pas « normal ».
- Courbe filtrée incident : axe ObservationTimestamp, valeurs moyennes TP3, Oil_temperature, Motor_current ; filtre FailurePeriodKey non vide et segment FailureReportCode.
- Drill-down OLAP : Year > QuarterNumber > MonthNumber > CalendarDate, puis slice sur un FailureReportCode et dice sur DimTime[Hour].

Ne présenter aucune disponibilité, MTTR, MTBF, coût, intervention ou économie : ces données ne sont pas présentes dans les sources.
