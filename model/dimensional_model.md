# Modèle dimensionnel recommandé — Smart Industrial Maintenance BI

## 1. Périmètre et statut

Ce document formalise le modèle conceptuel à partir de l'audit réel de MetroPT-3. Il ne crée ni pipeline ETL, ni requête Power Query, ni mesure DAX, ni dashboard.

Le modèle couvre uniquement deux processus réellement représentés :

1. l'observation temporelle des signaux du compresseur ;
2. l'analyse des quatre périodes de défaillance documentées séparément par l'opérateur.

Il ne modélise pas les coûts, les interventions de maintenance, les équipements d'un parc, les sites, la production ou la disponibilité, car ces données ne sont pas présentes dans le CSV audité.

## 2. Problématique industrielle

Comment organiser les observations de capteurs et les quatre périodes de défaillance externes afin d'analyser le fonctionnement temporel du compresseur, de comparer les signaux autour des périodes documentées et de préserver la distinction entre mesure, état numérique et événement de défaillance ?

Le modèle ne transforme pas une période de défaillance en milliers de pannes. Une période reste un événement intervalle ; les observations peuvent être associées à cette période par une règle temporelle documentée, sans devenir de nouvelles pannes.

## 3. Acteurs décisionnels

| Acteur | Besoin analytique réaliste |
| --- | --- |
| Analyste BI / data engineer | Contrôler la qualité, la couverture temporelle et la traçabilité des sources |
| Responsable maintenance, dans le cadre de l'étude | Examiner les signaux avant, pendant et après les périodes externes documentées |
| Enseignant et jury académique | Vérifier le grain, les clés, les relations, l'additivité et les hypothèses |
| Ingénieur condition monitoring, dans le cadre d'une extension | Explorer les régimes et états des signaux sans confondre anomalie et panne validée |

Le propriétaire métier réel des données d'exploitation n'est pas identifié dans le dépôt. Les interprétations opérationnelles doivent donc rester prudentes.

## 4. Processus et méthode GQM

| Goal | Questions | Metrics candidates |
| --- | --- | --- |
| Comprendre la couverture et la fiabilité des observations | Combien d'observations sont disponibles ? La série est-elle complète et régulière ? | ObservationCount, NullCount, DuplicateCount, première et dernière date, intervalle modal, nombre d'intervalles supérieurs à la cadence modale |
| Analyser le comportement des signaux | Comment les sept mesures analogiques évoluent-elles ? | Minimum, maximum, moyenne, écart-type, nombre d'observations par signal et par période |
| Décrire les états numériques | Quels états 0/1 sont observés et à quelle fréquence ? | Compte par valeur et par période pour les huit signaux numériques |
| Mettre en contexte les événements externes | Quels signaux sont observés dans une période documentée ? | FailurePeriodCount, durée documentée, ObservationCountInsidePeriod, statistiques avant/pendant/après |
| Préserver la traçabilité académique | Quelle source et quelle règle ont produit une association ? | SourceReference, FailureReportCode, règles de borne temporelle, qualité du timestamp |

Ces metrics sont des candidats de conception ; ils ne constituent pas encore des mesures DAX implémentées.

## 5. Comparaison des granularités

| Option | Définition | Volume indicatif | Avantages | Limites | Décision |
| --- | --- | ---: | --- | --- | --- |
| Observation originale, format large | Une ligne du fait par ligne du CSV, avec les 15 signaux en colonnes | 1 516 948 lignes | Conserve exactement la source, moins de lignes, lecture simple, comparaison directe des signaux | La sélection dynamique d'un signal est moins élégante ; les colonnes analogiques et numériques sont hétérogènes | **Grain principal recommandé** |
| Capteur et timestamp, format long | Une ligne par timestamp et par signal | 22 754 220 lignes au maximum, soit 1 516 948 × 15 | DimSignal devient naturelle, filtrage et visualisation des signaux uniformes | Environ 15 fois plus de lignes ; mélange des mesures analogiques et états dans une valeur générique ; plus coûteux dans Power BI | Variante future si l'analyse multi-signal le justifie |
| Agrégation de cinq minutes | Une ligne par tranche de cinq minutes, avec statistiques par signal | Non fixé sans règle de gestion des trous | Réduit fortement le volume et facilite les tendances | Perd les transitions et les extrêmes courts ; dépend d'une règle d'agrégation et du traitement des trous | Vue agrégée future, jamais le remplacement du fait source |

Les granularités ne doivent pas être mélangées dans une même table de faits. Si un fait 5 minutes est créé plus tard, il devra être une table ou une vue de faits séparée avec ses propres clés et mesures.

## 6. Schéma recommandé

Le choix est une **constellation minimale** : deux faits partagent les dimensions temporelles conformes.

~~~mermaid
erDiagram
    DIM_DATE ||--o{ FACT_SENSOR_OBSERVATION : "date d observation"
    DIM_TIME ||--o{ FACT_SENSOR_OBSERVATION : "heure d observation"
    DIM_DATE ||--o{ FACT_FAILURE_PERIOD : "StartDate active"
    DIM_DATE ||--o{ FACT_FAILURE_PERIOD : "EndDate inactive"

    DIM_DATE {
        int DateKey PK
        date CalendarDate
        int Year
        int QuarterNumber
        int MonthNumber
        string MonthName
        int DayOfMonth
    }

    DIM_TIME {
        int TimeKey PK
        string TimeLabel
        int Hour
        int Minute
        int Second
        string TimeBucket
    }

    FACT_SENSOR_OBSERVATION {
        bigint ObservationKey PK
        int SourceRowKey
        int DateKey FK
        int TimeKey FK
        datetime ObservationTimestamp
        decimal TP2
        decimal TP3
        decimal H1
        decimal DV_pressure
        decimal Reservoirs
        decimal Oil_temperature
        decimal Motor_current
        decimal COMP
        decimal DV_eletric
        decimal Towers
        decimal MPG
        decimal LPS
        decimal Pressure_switch
        decimal Oil_level
        decimal Caudal_impulses
        int ObservationCount
    }

    FACT_FAILURE_PERIOD {
        int FailurePeriodKey PK
        string FailureReportCode UK
        datetime StartTimestamp
        datetime EndTimestamp
        int StartDateKey FK
        int EndDateKey FK
        string FailureType
        string Severity
        string MaintenanceNoteRaw
        string SourceReference
        decimal DurationSeconds
        int FailurePeriodCount
    }
~~~

Le diagramme exprime les relations conceptuelles. L'association d'une observation à un intervalle de défaillance est une règle temporelle à documenter ; elle n'est pas une relation directe sur la date seule et n'est pas implémentée dans cette étape.

## 7. Description des tables

### FactSensorObservation

**Rôle :** conserver les observations réelles du CSV et permettre l'analyse temporelle des 15 signaux.

**Grain :** une ligne par observation originale du CSV, correspondant à un timestamp et aux 15 signaux enregistrés dans la même ligne.

**Clés :**

- ObservationKey : clé de substitution technique, générée lors d'une future préparation ; elle ne remplace pas la source.
- SourceRowKey : valeur réelle de Unnamed: 0 ; clé métier technique source, unique dans l'audit mais non séquentielle.
- DateKey et TimeKey : clés étrangères vers les dimensions temporelles.
- ObservationTimestamp : timestamp source conservé pour les règles d'intervalle.

**Mesures :**

- ObservationCount = 1 : additive sur les lignes.
- Les sept signaux analogiques : mesures numériques, additives uniquement pour un total mathématique sans sens métier ; elles sont principalement non additives et doivent être résumées par moyenne, minimum, maximum ou écart-type selon le besoin.
- Les huit signaux numériques : états 0/1, non additifs comme des grandeurs physiques ; les sommes sont des comptes d'observations dans l'état 1, pas des pannes.

### FactFailurePeriod

**Rôle :** conserver les quatre périodes de défaillance fournies séparément par l'opérateur.

**Grain :** une ligne par rapport de période de défaillance externe.

**Clés :**

- FailurePeriodKey : clé de substitution.
- FailureReportCode : clé métier externe, par exemple Report #1 à Report #4.
- StartDateKey et EndDateKey : rôles de date distincts vers DimDate.
- StartTimestamp et EndTimestamp : bornes nécessaires pour l'association précise aux observations.

**Attributs et mesures :**

- FailureType et Severity : attributs tels que documentés, sans enrichissement inventé.
- MaintenanceNoteRaw : texte source conservé comme note non normalisée ; il ne constitue pas une table d'interventions.
- DurationSeconds : durée dérivée des bornes, additive entre périodes si la règle de non-chevauchement est confirmée.
- FailurePeriodCount = 1 : additive pour compter les périodes documentées.

### DimDate

**Rôle :** fournir une hiérarchie calendrier commune.

**Grain :** une ligne par date civile.

**Clé et hiérarchie :** DateKey, CalendarDate, Year > Quarter > Month > Day. Les numéros de mois doivent être conservés pour trier les noms de mois.

### DimTime

**Rôle :** analyser les observations selon l'heure de la journée et faciliter les regroupements temporels.

**Grain :** une ligne par seconde de la journée. La valeur exacte du timestamp reste dans le fait ; DimTime sert uniquement à l'analyse de l'heure de la journée.

**Clé et hiérarchie :** TimeKey, Hour, Minute, Second ; TimeBucket peut regrouper par heure ou tranche, sans remplacer l'horodatage original.

Une dimension d'état opérationnel n'est pas retenue : les données permettent de décrire des signaux binaires, mais ne fournissent pas une définition validée de « normal », « en charge », « déchargé » ou « en panne » applicable à toutes les observations.

## 8. Association rigoureuse des incidents

La stratégie future doit utiliser une condition d'intervalle :

ObservationTimestamp >= StartTimestamp
et
ObservationTimestamp <= EndTimestamp

Les bornes inclusives devront être confirmées à partir de la convention des rapports. Une jointure sur CalendarDate seule est interdite, car elle classerait toute la journée du 18 avril comme incident alors que le modèle doit respecter les heures de début et de fin.

Deux implémentations sont possibles plus tard :

1. une colonne dérivée FailurePeriodKey dans une vue ou table analytique séparée, avec une valeur nulle hors période ;
2. une table de pont ObservationFailurePeriod, uniquement si des chevauchements ou plusieurs contextes apparaissent.

La première option est suffisante si les quatre intervalles ne se chevauchent pas et si chaque observation appartient au plus à une période. Dans les deux cas, une observation dans une période n'est pas une nouvelle panne, et une observation hors période n'est pas une preuve de fonctionnement normal.

## 9. Comparaison des architectures

### Schéma en étoile

Simple à expliquer et performant pour Power BI. Il convient au fait large d'observations et aux dimensions Date/Time. C'est la meilleure base pédagogique pour ce projet.

### Schéma en flocon

Normaliser davantage les attributs temporels ou les catégories réduirait la redondance, mais ajouterait des jointures sans bénéfice démontré pour ce dataset. Il n'est pas retenu.

### Constellation

Deux faits de grains différents partagent des dimensions conformes. Elle représente correctement les observations et les périodes externes sans les mélanger. C'est le choix recommandé, avec deux étoiles simples plutôt qu'un modèle complexe.

## 10. Relations et cardinalités Power BI

Les relations physiques recommandées sont les suivantes :

| Relation | Cardinalité | État Power BI | Justification |
| --- | --- | --- | --- |
| DimDate[DateKey] -> FactSensorObservation[DateKey] | 1 vers plusieurs | Active | Une date décrit plusieurs observations |
| DimTime[TimeKey] -> FactSensorObservation[TimeKey] | 1 vers plusieurs | Active | Une heure décrit plusieurs observations |
| DimDate[DateKey] -> FactFailurePeriod[StartDateKey] | 1 vers plusieurs | Active | Rôle calendrier principal des périodes, par date de début |
| DimDate[DateKey] -> FactFailurePeriod[EndDateKey] | 1 vers plusieurs | Inactive | Second rôle de date ; activation explicite uniquement pour les analyses par date de fin |

Les dimensions filtrent les faits dans un sens unique. Il n'y a pas de relation directe entre FactSensorObservation et FactFailurePeriod dans le modèle physique recommandé. Leur association future repose sur les timestamps complets dans une vue dérivée ou une table de pont, pas sur une relation de dimension ambiguë.

## 11. Contrôles de cohérence et limites

- FactSensorObservation et FactFailurePeriod ont des grains différents et ne doivent pas être concaténés.
- Les quatre périodes externes ne doivent pas être dupliquées pour chaque observation dans le fait source.
- DimDate est conforme aux deux faits ; les rôles StartDate et EndDate doivent être distingués.
- La relation StartDate active et la relation EndDate inactive sont nécessaires pour rester compatible avec les règles de relations actives de Power BI.
- DimTime sert à l'analyse de l'heure mais ne remplace jamais ObservationTimestamp.
- Les trous temporels et la fréquence modale de 10 secondes doivent être documentés avant toute agrégation 5 minutes.
- Le modèle ne permet pas à lui seul de calculer coûts, MTBF, MTTR, disponibilité ou économies.
- Les noms de colonnes réels et les incohérences du PDF doivent rester traçables.

## 12. Décisions encore à valider

- Convention de fuseau horaire et bornes inclusives des incidents.
- Convention de nommage des clés et génération de ObservationKey.
- Inclusion physique de DimTime dans le modèle Power BI.
- Règle de traitement des intervalles supérieurs à 10 secondes.
- Nécessité éventuelle d'une vue longue ou d'un fait agrégé 5 minutes pour la performance.
- Validation métier du sens de 0 et 1 pour chaque signal numérique.
