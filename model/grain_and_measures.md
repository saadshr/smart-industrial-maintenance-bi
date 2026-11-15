# Grains, clés et mesures — Modèle MetroPT-3

## 1. Règle de grain

Chaque table de faits doit avoir un grain unique, écrit en une phrase avant toute implémentation :

- FactSensorObservation : une ligne par observation originale du CSV, avec un timestamp et les 15 signaux associés.
- FactFailurePeriod : une ligne par période de défaillance externe documentée.

Le fait des observations et le fait des périodes ne doivent pas être fusionnés. Une ligne de défaillance représente un intervalle, pas une observation répétée à chaque timestamp.

## 2. Clés

| Table | Clé de substitution | Clé métier ou source | Clés étrangères |
| --- | --- | --- | --- |
| FactSensorObservation | ObservationKey | SourceRowKey, correspondant à Unnamed: 0 | DateKey, TimeKey |
| FactFailurePeriod | FailurePeriodKey | FailureReportCode, par exemple Report #1 | StartDateKey, EndDateKey |
| DimDate | DateKey | CalendarDate | — |
| DimTime | TimeKey | TimeLabel ou seconde de la journée | — |

ObservationKey et FailurePeriodKey seront générées lors d'une future implémentation. SourceRowKey est unique dans l'audit, mais ses valeurs sont espacées de 10 et ne sont pas un compteur de lignes. Dans Power BI, StartDateKey sera reliée activement à DimDate ; EndDateKey sera une seconde relation inactive vers la même dimension.

## 3. Mesures et additivité

### FactSensorObservation

| Mesure ou attribut | Type | Additivité | Interprétation |
| --- | --- | --- | --- |
| ObservationCount | Entier | Additive | Compte des lignes d'observation |
| TP2, TP3, H1 | Décimal | Non additive | Pressions ; résumés adaptés : moyenne, minimum, maximum, écart-type |
| DV_pressure, Reservoirs | Décimal | Non additive | Pressions ; ne pas sommer pour un KPI physique |
| Oil_temperature | Décimal | Non additive | Température ; moyenne ou extrêmes selon l'analyse |
| Motor_current | Décimal | Non additive | Courant ; moyenne ou extrêmes, sans somme métier automatique |
| COMP, DV_eletric, Towers, MPG, LPS, Pressure_switch, Oil_level, Caudal_impulses | État numérique 0/1 | Non additive comme mesure physique | Un compte de lignes à 1 peut décrire une durée d'observation, mais pas un nombre de pannes |

Les statistiques min/max/moyenne/écart-type seront des agrégations de mesures de capteurs, pas des colonnes stockées comme résultats définitifs dans la table source.

### Distinction additive, semi-additive et non additive

- **Additive :** ObservationCount, FailurePeriodCount et DurationSeconds lorsque les périodes ne se chevauchent pas et qu'elles sont agrégées sans double comptage entre les rôles de date.
- **Semi-additive :** une mesure future de type LastObservedValue peut être agrégée sur les dimensions descriptives mais pas sommée sur le temps. Cette mesure n'est pas encore implémentée.
- **Non additive :** les valeurs instantanées des sept signaux analogiques, les états numériques 0/1 et les attributs textuels. Ils doivent utiliser des agrégations adaptées, par exemple moyenne, minimum, maximum, dernier état ou comptage de lignes dans un état.

La somme des états numériques à 1 est un nombre d'observations dans cet état ; elle ne représente pas un nombre de pannes.

### FactFailurePeriod

| Mesure ou attribut | Type | Additivité | Interprétation |
| --- | --- | --- | --- |
| FailurePeriodCount | Entier | Additive | Compte des périodes externes documentées |
| DurationSeconds | Décimal | Additive si les intervalles ne se chevauchent pas | Durée calculée entre les bornes documentées |
| FailureType | Texte | Non applicable | Type documenté, par exemple Air leak |
| Severity | Texte | Non applicable | Gravité documentée, par exemple High stress |
| MaintenanceNoteRaw | Texte | Non applicable | Note source conservée sans créer un événement de maintenance |

## 4. Association temporelle future

La condition de rattachement doit être :

ObservationTimestamp >= StartTimestamp et ObservationTimestamp <= EndTimestamp

Cette condition doit être appliquée sur les timestamps complets. Une jointure sur DateKey seule est incorrecte, notamment pour le rapport #1 et les périodes qui commencent ou se terminent au milieu d'une journée.

Une observation dans une période documentée peut recevoir FailurePeriodKey dans une vue dérivée. Elle ne devient pas une nouvelle occurrence de panne. Une observation hors période documentée doit rester « hors événement documenté », sans être appelée automatiquement « normale ».

Dans Power BI, cette association ne doit pas être créée par une relation directe entre les deux faits. Elle devra être matérialisée ultérieurement dans une vue dérivée ou une table de pont si nécessaire.

## 5. Variante long format

Si le modèle long est retenu plus tard :

- grain : une ligne par timestamp et par signal ;
- volume théorique : 22 754 220 lignes pour 15 signaux et 1 516 948 timestamps ;
- DimSignal devient une dimension nécessaire ;
- ValueNumeric est une mesure de valeur, non additive ;
- SignalCategory distingue analogique et numérique ;
- DigitalStateValue reste un état, pas un événement de panne.

Cette variante ne doit pas être mélangée au fait large dans une même table. Elle doit être comparée sur la performance et la lisibilité Power BI avant décision.

## 6. Variante agrégée cinq minutes

Un fait à cinq minutes serait une seconde table de faits :

- grain : une ligne par tranche de cinq minutes et éventuellement par signal ;
- mesures : moyenne, minimum, maximum, écart-type, nombre d'observations et taux de couverture ;
- risque : perte des transitions courtes et dépendance à une règle de traitement des trous ;
- relation aux incidents : la tranche doit être comparée à l'intervalle externe, sans propager artificiellement une panne.

Ce fait agrégé peut servir à la performance d'un futur rapport, mais il ne remplace pas FactSensorObservation.
