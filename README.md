# Smart Industrial Maintenance BI

Ce projet de Business Intelligence vise à suivre l’état des équipements industriels, leurs pannes et leurs interventions de maintenance. Le tableau de bord permettra d’explorer les mesures des capteurs IoT et les temps d’arrêt par période, site et équipement.

## État du dépôt

- `README.md` présente le projet et son architecture cible.
- `.gitignore` exclut notamment les environnements Python, les caches et les fichiers de configuration locaux comme `.env`.
- `LICENSE` contient la licence MIT du projet.

## Architecture cible

```mermaid
flowchart LR
    A[Exports IoT et maintenance] --> B[Power Query]
    B --> C[Modèle dimensionnel]
    C --> D[Mesures DAX]
    D --> E[Rapport Power BI]
```

Power Query importe les relevés capteurs, le référentiel équipements et les historiques de panne et d’intervention. Il harmonise les identifiants, les horodatages et les unités, puis contrôle les doublons et les valeurs manquantes. Le modèle dimensionnel relie les événements aux équipements et au calendrier. Les mesures DAX permettent ensuite l’analyse OLAP dans le rapport, par exemple en passant des arrêts mensuels d’un site au détail par équipement.

### Arborescence prévue

Les fichiers ci-dessous seront ajoutés au fil de la mise en œuvre.

```text
data/
└── samples/
    ├── equipment.csv
    ├── sensor_readings.csv
    ├── failures.csv
    └── maintenance_events.csv
docs/
├── data-dictionary.md
└── dimensional-model.md
power-bi/
└── maintenance.pbix
```

### Rôle des fichiers prévus

- `data/samples/equipment.csv` répertorie les équipements et leurs attributs, dont l’identifiant, le type et le site.
- `data/samples/sensor_readings.csv` contient une ligne par mesure, avec l’équipement, le capteur, l’horodatage, la valeur et l’unité.
- `data/samples/failures.csv` contient une ligne par panne, avec l’équipement, le début et, lorsqu’elle est connue, la fin de l’arrêt.
- `data/samples/maintenance_events.csv` contient une ligne par intervention, avec l’équipement, le type d’intervention, les dates et une référence à la panne lorsqu’elle existe.
- `docs/data-dictionary.md` documente les colonnes, les types, les unités et les règles de validation des sources.
- `docs/dimensional-model.md` décrit le grain des tables, leurs clés et relations, ainsi que les définitions métier des indicateurs.
- `power-bi/maintenance.pbix` regroupe les requêtes Power Query, les relations du modèle, les mesures DAX et les pages du rapport Power BI.

### Modèle dimensionnel initial

- `DimEquipment` contient une ligne par équipement et porte les attributs de site et de type.
- `DimDate` contient une ligne par jour et permet les agrégations par mois, trimestre et année.
- `FactSensorReading` contient une ligne par relevé et sert à analyser l’évolution des valeurs capteurs.
- `FactFailure` contient une ligne par panne et sert à compter les pannes et à mesurer les arrêts.
- `FactMaintenance` contient une ligne par intervention et sert à analyser la charge de maintenance.

Les dimensions communes filtrent les tables de faits via des relations de type un-à-plusieurs. Le premier rapport pourra suivre le nombre de pannes, le temps d’arrêt cumulé, le nombre d’interventions et les tendances des mesures capteurs. Les règles de calcul préciseront comment traiter les pannes en cours et les arrêts qui chevauchent plusieurs périodes.
