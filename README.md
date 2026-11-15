# Smart Industrial Maintenance BI

**Titre académique :** *Conception et implémentation d'un système décisionnel pour le pilotage de la maintenance industrielle à partir de données IoT*

Smart Industrial Maintenance BI est un projet académique de Business Intelligence réalisé dans le cadre de la filière **INDIA de l'ENSAM Rabat**. Il étudie comment transformer des données issues de capteurs industriels en un modèle décisionnel fiable pour surveiller un compresseur d'air, étudier les périodes de défaillance documentées et préparer des analyses orientées maintenance.

Le projet s'appuie sur le jeu de données réel **MetroPT-3 Dataset**, collecté à partir d'un compresseur d'air installé dans un train de métro portugais. Il s'agit donc d'une étude de cas du secteur ferroviaire portugais, et non de données collectées au Maroc. Les méthodes analytiques développées ont vocation à fournir des enseignements transposables aux environnements industriels, notamment marocains.

> **État du projet - Audit et modèle dimensionnel conçus**
>
> Le dépôt contient la documentation du projet, l'audit local du CSV officiel et la conception du modèle dimensionnel. Aucun pipeline ETL, rapport Power BI, mesure DAX, capture d'écran ou jeu de données dérivé n'a encore été implémenté.

## Contexte industriel et problématique métier

Les compresseurs industriels sont des équipements critiques : des conditions de fonctionnement anormales peuvent affecter la continuité de service, la sécurité et la planification de la maintenance. Les séries de mesures issues des capteurs peuvent révéler des profils de fonctionnement et aider les analystes à étudier le contexte des défaillances documentées, mais les données temporelles brutes ne fournissent pas à elles seules une vision directement exploitable pour la décision.

La problématique métier traitée par ce projet est la suivante :

> Comment organiser des signaux IoT hétérogènes et des périodes de défaillance documentées séparément afin de construire un système décisionnel fiable pour analyser le fonctionnement du compresseur et soutenir l'investigation orientée maintenance ?

À ce stade, le projet ne prétend pas prédire les pannes, quantifier des économies de maintenance ou mesurer la disponibilité d'un équipement. Ces questions nécessiteraient des labels validés, des données métier et des travaux méthodologiques complémentaires.

## Objectifs métier et questions décisionnelles

### Objectifs

- Établir une compréhension traçable des données sources MetroPT-3.
- Définir un modèle multidimensionnel adapté à l'analyse temporelle et aux périodes de défaillance.
- Préparer des transformations reproductibles avec Power Query et M.
- Concevoir des analyses Power BI reposant sur des définitions DAX transparentes et des hypothèses documentées.
- Appliquer des opérations OLAP telles que le roll-up, le drill-down, le slice, le dice et le pivot.
- Produire une solution BI documentée sur le plan académique et révisable sur le plan technique.

### Questions décisionnelles

- Comment les signaux des capteurs évoluent-ils dans le temps et selon les périodes de fonctionnement ?
- Quels profils de signaux sont observés autour des périodes de défaillance documentées séparément ?
- Comment comparer des périodes de fonctionnement apparemment normales avec des fenêtres de défaillance documentées ?
- Quels sont les grains temporels et les hiérarchies appropriés pour l'analyse ?
- Quels problèmes de qualité des données, valeurs manquantes, doublons ou incohérences temporelles pourraient affecter l'interprétation ?
- Quels indicateurs peuvent être calculés à partir des données sources et lesquels nécessiteraient des données supplémentaires de maintenance ou de l'entreprise ?

## Jeu de données

Le projet utilise le **MetroPT-3 Dataset (2020)** officiel, publié par l'UCI Machine Learning Repository :

- [UCI Machine Learning Repository — MetroPT-3 Dataset](https://archive.ics.uci.edu/dataset/791/metropt+3+dataset)
- Taille annoncée : **1 516 948 observations**.
- Contenu annoncé : **15 signaux de capteurs**, dont 7 signaux analogiques et 8 signaux numériques, ainsi que des informations temporelles relatives au compresseur.
- Informations de défaillance : quatre périodes de défaillance documentées et fournies séparément par l'opérateur.

Le fichier CSV d'origine ne contient **pas de label de panne au niveau de chaque ligne**. Les périodes de défaillance doivent donc être traitées comme des informations d'événements externes et reliées aux séries temporelles au moyen de règles temporelles documentées. Toute association de ce type sera explicitement documentée et validée lors de l'implémentation.

Le dataset ne doit pas être confondu avec d'autres datasets ou versions MetroPT. Ce projet fait spécifiquement référence au **MetroPT-3 Dataset publié en 2020 avec 15 signaux**.

## Technologies prévues

| Technologie | Utilisation prévue | État |
| --- | --- | --- |
| Power BI | Modèle sémantique, rapport interactif et analyse visuelle | Prévu |
| Power Query | Ingestion, profilage, nettoyage et transformation des données | Prévu |
| M | Logique de transformation Power Query | Prévu |
| DAX | Mesures, analyse temporelle et calculs du rapport | Prévu |
| Git | Contrôle de version et historique académique traçable | En cours |
| GitHub | Hébergement du dépôt et collaboration | En cours |
| Python | Contrôles et profilage optionnels de la qualité des données | Prévu ; pas encore requis |

Aucune installation de dépendance ni aucun téléchargement du dataset n'est nécessaire pour l'étape actuelle, qui est uniquement documentaire.

## Architecture décisionnelle envisagée

L'architecture suivante constitue une cible de conception et non un pipeline implémenté :

~~~mermaid
flowchart LR
    A[Donnees sources MetroPT-3] --> B[Power Query / M]
    E[Rapports externes des periodes de defaillance] --> B
    B --> C[Modele dimensionnel conforme]
    C --> D[Mesures semantiques DAX]
    D --> F[Rapport Power BI]
    B --> G[Controles de qualite des donnees]
~~~

L'architecture préservera la traçabilité des sources, distinguera les observations brutes des associations d'événements dérivées et rendra les hypothèses visibles pour les utilisateurs du rapport. Aucune source d'événements de maintenance, de coûts, de sites ou de référentiel d'équipements n'est actuellement présente dans le dépôt ; ces concepts ne doivent pas être considérés comme disponibles sans source explicite et validation.

## Approche de modélisation multidimensionnelle

Le modèle conceptuel recommandé est une constellation minimale composée de deux faits de grains distincts et de dimensions temporelles conformes. Son implémentation technique reste à réaliser après validation académique.

### Faits et dimensions candidates — Prévu

- **FactSensorObservation :** une ligne par observation source au grain documenté du timestamp et du signal de capteur.
- **FactFailurePeriod :** une ligne par période de défaillance documentée séparément, avec sa référence source et ses bornes temporelles.
- **DimDate / DimTime :** dimensions calendrier et temps utilisées pour les agrégations temporelles.
- **DimSignal :** nom du signal, type source et métadonnées techniques.
- **DimFailureContext :** attributs contrôlés décrivant le contexte de l'événement documenté, uniquement lorsqu'ils sont supportés par les rapports externes.

La conception finale définira les clés, les relations, la granularité, la gestion des fuseaux horaires et des bornes temporelles ainsi que le traitement des observations manquantes ou dupliquées. Une association à une période de défaillance ne sera pas présentée comme un label natif au niveau de chaque ligne, sauf si cette dérivation est explicitement créée, testée et documentée.

## Catalogue des KPI

### KPI prévus

Les indicateurs suivants sont candidats à une implémentation ultérieure, sous réserve du profilage des données et de définitions formelles :

- Nombre d'observations et couverture des données par période et par signal.
- Taux de valeurs manquantes et de doublons.
- Minimum, maximum, moyenne, médiane et variabilité des signaux lorsque cela est statistiquement pertinent.
- Nombre et durée des périodes de défaillance documentées.
- Volume d'observations à l'intérieur et à l'extérieur des fenêtres de défaillance documentées.
- Synthèses des signaux avant, pendant et après les périodes de défaillance documentées.

Il s'agit d'**indicateurs analytiques prévus**, et non de résultats actuels. Aucun coût de maintenance, nombre d'interventions, taux de disponibilité, taux d'arrêt, MTBF, MTTR ou économie réalisée ne doit être rapporté à partir du dépôt actuel, car les sources validées nécessaires ne sont pas implémentées ici.

### KPI implémentés

**Aucun.** Aucune mesure DAX ni aucun calcul de KPI validé n'a été implémenté dans le dépôt à ce stade.

## Pages Power BI prévues

Toutes les pages ci-dessous sont **Prévues** et n'existent pas encore sous la forme d'un rapport Power BI :

1. **Vue exécutive** — périmètre, couverture des données et contexte général des événements documentés.
2. **Qualité des données** — complétude, doublons, intégrité des timestamps et réserves liées aux sources.
3. **Exploration des capteurs** — tendances, distributions, comparaisons de signaux et drill-down temporel.
4. **Analyse des périodes de défaillance** — observations avant, pendant et après les périodes documentées séparément.
5. **Analyse OLAP** — scénarios de roll-up, drill-down, slice, dice et pivot.
6. **Méthodologie et hypothèses** — grains, règles d'association aux événements, définitions et limites.

## Feuille de route

- [x] Créer le dépôt GitHub et établir la base documentaire initiale.
- [x] Documenter le périmètre du projet, l'attribution des sources et les limites actuelles.
- [x] Auditer le schéma MetroPT-3, les timestamps, les types de signaux, les valeurs manquantes et les doublons.
- [x] Acquérir et enregistrer localement les fichiers sources officiels et les rapports externes des périodes de défaillance.
- [x] Définir le glossaire métier, le dictionnaire de données et les spécifications initiales des KPI.
- [x] Confirmer les grains des tables de faits, les dimensions, les hiérarchies et la matrice en bus.
- [x] Documenter le modèle dimensionnel recommandé et ses compromis.
- [ ] Implémenter et documenter les transformations Power Query / M.
- [ ] Ajouter des contrôles Python optionnels de la qualité des données s'ils présentent une valeur ajoutée.
- [ ] Construire le modèle sémantique Power BI et valider les relations.
- [ ] Implémenter et tester les mesures DAX.
- [ ] Construire et revoir les pages du rapport interactif.
- [ ] Valider les résultats, les hypothèses et les limites.
- [ ] Produire le rapport académique et la présentation.

## Organisation du dépôt

Le dépôt contient actuellement les fichiers suivis suivants :

~~~text
smart-industrial-maintenance-bi/
├── .gitignore
├── LICENSE
├── README.md
├── docs/
    ├── data_audit.md
    └── data_dictionary.md
├── scripts/
    └── audit_data.py
└── model/
    ├── dimensional_model.md
    ├── bus_matrix.md
    └── grain_and_measures.md
~~~

Le répertoire `data/raw/` est réservé aux téléchargements locaux et ignoré par Git. Les futurs répertoires et fichiers ne sont volontairement pas présentés comme des artefacts existants. Leur organisation finale sera documentée ici lorsqu'ils auront effectivement été créés et vérifiés.

## Installation et reproduction

**État actuel : audit local et conception dimensionnelle réalisés.** Le script `scripts/audit_data.py` exécute l'audit en lecture par blocs sur les fichiers locaux. Les documents `model/` décrivent le grain, les faits, les dimensions, la matrice en bus et les mesures candidates. Aucune procédure d'installation Power BI ou de reproduction complète n'est encore revendiquée.

Les instructions de reproduction seront ajoutées uniquement lorsque les fichiers sources concernés, la logique de transformation, les artefacts de reporting et la procédure de validation auront été implémentés et testés.

## Références, attribution et licences

- Dataset : [MetroPT-3 Dataset — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/791/metropt+3+dataset).
- Documentation du dataset et exigences de citation : suivre la page officielle UCI et les métadonnées de publication associées.
- Le dataset reste attribué à ses créateurs et à son fournisseur d'origine. Ce dépôt ne revendique aucun droit de propriété sur les données sources.
- Le dépôt contient une [licence MIT](./LICENSE) pour le code et la documentation du projet. Cette licence du dépôt ne modifie pas et ne remplace pas automatiquement les conditions d'utilisation propres au dataset ; les utilisateurs doivent consulter la page officielle du dataset avant toute redistribution des données.

## Limites et hypothèses

- Les données sources décrivent un compresseur installé dans un train de métro portugais ; il ne s'agit pas de données opérationnelles marocaines.
- Le CSV d'origine ne fournit pas de label de panne au niveau de chaque ligne. Les périodes de défaillance proviennent de rapports opérateur séparés et nécessitent une association temporelle documentée.
- Le dataset seul ne permet pas d'établir les interventions de maintenance, les coûts, l'impact sur la production, la disponibilité ou les économies.
- Tout choix concernant le grain temporel, les bornes des fenêtres d'événements, le traitement des valeurs manquantes, la méthode d'agrégation ou la règle d'anomalie peut affecter l'analyse et doit être validé.
- Les KPI prévus sont soumis au profilage des sources et pourront être révisés si leurs définitions ne sont pas supportées par les champs disponibles.
- Le projet est une étude académique de système décisionnel. Il ne doit pas être présenté comme un système de maintenance en production ni comme un modèle de maintenance prédictive validé sans éléments supplémentaires.

## Livrables académiques

Les livrables académiques prévus sont les suivants :

- analyse de la problématique métier et des besoins ;
- audit des données sources et dictionnaire de données ;
- modèle multidimensionnel, schéma en étoile ou constellation et matrice en bus ;
- documentation de la préparation Power Query / M ;
- catalogue des mesures DAX et notes de validation ;
- tableau de bord Power BI interactif ;
- scénarios d'analyse OLAP et interprétation des résultats ;
- rapport académique présentant la méthodologie, les hypothèses, les limites et les références ;
- présentation finale et démonstration du projet.

## Règles de contribution

Les modifications doivent rester ciblées, documentées et traçables avec Git. Chaque étape d'implémentation doit distinguer clairement les états **Prévu**, **En cours** et **Terminé**, et éviter de présenter des résultats qui n'ont pas été calculés et validés.
