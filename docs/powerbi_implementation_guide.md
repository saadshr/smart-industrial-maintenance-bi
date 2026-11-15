# Guide express d'implémentation Power BI

## 1. Préparer les fichiers

Dans le dossier du projet, exécuter :

    c:/Users/hp/Desktop/github_repos/.venv/Scripts/python.exe scripts/prepare_powerbi_data.py

Les quatre CSV sont créés dans data/processed/. Le CSV original dans data/raw/ n'est jamais modifié et les fichiers générés restent ignorés par Git.

## 2. Importer avec Power Query

Dans Power BI Desktop : Accueil > Transformer les données > Nouvelle source > Texte/CSV. Importer les quatre fichiers de data/processed/, puis appliquer les types indiqués par les noms de colonnes.

Pour démontrer une transformation M réelle, créer un paramètre texte pSourceFolder, puis coller les requêtes du dossier powerquery/. La requête FactSensorObservation lit directement le CSV brut, renomme les colonnes, typifie les signaux, crée les clés temporelles et applique les quatre fenêtres inclusives. Les trois autres requêtes créent les dimensions et le fait des incidents.

## 3. Modèle

Créer les relations, en filtre simple :

- DimDate[DateKey] (1) vers FactSensorObservation[DateKey] (*) — active ;
- DimTime[TimeKey] (1) vers FactSensorObservation[TimeKey] (*) — active ;
- DimDate[DateKey] (1) vers FactFailurePeriod[StartDateKey] (*) — active ;
- DimDate[DateKey] (1) vers FactFailurePeriod[EndDateKey] (*) — inactive.

Ne créer aucune relation directe entre les deux faits. FailurePeriodKey dans le fait des observations est une association dérivée par timestamp ; elle ne représente pas une nouvelle panne par observation.

## 4. Mesures et pages

Copier les expressions de dax/measures.dax dans Power BI, une mesure à la fois. Créer trois pages : Vue générale, Surveillance des capteurs, Analyse des incidents et OLAP, selon le catalogue docs/powerbi_visual_catalog.md.

## 5. Contrôle final

Vérifier que le nombre d'observations est 1 516 948, que le nombre d'incidents est 4 et que les timestamps restent de type date/heure. Les valeurs analytiques doivent être lues dans Power BI après actualisation ; aucune valeur analytique n'est pré-écrite dans la documentation.
