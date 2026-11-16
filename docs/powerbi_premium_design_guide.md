# Refonte visuelle premium Power BI — MetroPT-3

## Statut d'automatisation

Le fichier `powerbi/Smart_Industrial_Maintenance.pbix` a été inspecté et sauvegardé avant toute intervention sous un nom horodaté dans le même dossier. Les sept mesures DAX et la logique métier existante sont conservées.

La modification directe d'un PBIX n'est pas réalisée par édition de son conteneur interne : cette méthode serait non documentée et risquerait de corrompre le rapport. Le thème JSON est prêt à être importé. La mise en page détaillée ci-dessous est la procédure sûre à appliquer dans Power BI Desktop.

Power BI Desktop est installé en version `2.158.1304.0 (26.09)`. Aucun fichier `.pbip` ou `.pbir` n'a été trouvé dans le dépôt ; aucune conversion n'a donc été tentée.

## Constats sur les captures actuelles

- La page Vue générale contient déjà les quatre KPI et les deux graphiques demandés, mais les cartes sont trop hautes, le titre de page est peu visible et la hiérarchie exécutive peut être renforcée.
- La page Surveillance des capteurs contient bien TP3, Oil_temperature et Motor_current. Les trois courbes sont lisibles, mais la page manque d'un bandeau de titre, d'une sélection temporelle commune et d'une hiérarchie principale/secondaire.
- La page Incidents et OLAP contient l'historique, l'histogramme, la matrice et les segments MonthName/Hour. Le tableau et la matrice doivent gagner en contraste, en espacement et en ordre visuel.
- Les captures disponibles sont des résultats réels, mais leur largeur est limitée à 785–793 px. Le guide ne les remplace pas par des maquettes et ne prétend pas qu'une refonte a été appliquée au PBIX.

## Thème

Importer `powerbi/themes/industrial_premium_theme.json` par **Affichage > Thèmes > Parcourir les thèmes**. Vérifier ensuite que le fond de page reste `#F4F7FB` et que les cartes utilisent un fond blanc.

Palette : marine `#14283F`, bleu industriel `#2474A6`, turquoise `#0D9488`, orange `#F59E0B`, rouge incident `#DC4C4C`, fond `#F4F7FB`, texte `#263445`.

## Règles communes aux trois pages

1. Format de page 16:9, fond `#F4F7FB`, marges visuelles régulières de 16 à 24 px.
2. Bandeau supérieur de 64 px : titre à gauche, sous-titre sous le titre, filet marine discret.
3. Utiliser Aptos/Aptos Display, titres 16–20 pt et valeurs KPI 26–32 pt.
4. Fond blanc, bordure `#D9E2EC`, rayon visuel proche de 8 px pour les cartes et visuels.
5. Désactiver les en-têtes de visuel lorsque les interactions ne sont pas nécessaires.
6. Ne créer aucun seuil d'alerte : les couleurs expriment la nature du signal, pas un diagnostic automatique.

## Page 1 — SMART INDUSTRIAL MAINTENANCE — VUE GÉNÉRALE

Sous-titre : *Monitoring décisionnel de l'unité de production d'air ferroviaire MetroPT-3*.

### Composition

- Ligne supérieure : quatre cartes alignées de largeur identique.
- Carte 1 : `[Nombre observations]`, accent bleu industriel.
- Carte 2 : `[Nombre incidents documentés]`, accent rouge incident.
- Carte 3 : `[Observations dans incidents documentés]`, accent orange.
- Carte 4 : `[Taux observations incidentées]`, accent turquoise.
- Graphique principal à gauche et plus large : ligne avec `DimDate[CalendarDate]` en axe et `[Nombre observations]` en valeur.
- Graphique secondaire à droite : barres horizontales avec `FactFailurePeriod[FailureReportCode]` et `DurationSeconds` ou une mesure de durée existante, tri chronologique par identifiant.
- Zone basse : slicers de date, année et mois uniquement si déjà présents dans le modèle.

### Filtres et interactions

Les quatre cartes doivent réagir aux filtres temporels. Le graphique d'incidents ne doit pas transformer les quatre périodes en quatre pannes par observation : il doit utiliser `FactFailurePeriod` et ses quatre clés documentées.

## Page 2 — INDUSTRIAL SENSOR MONITORING

Sous-titre : *Analyse temporelle des principaux paramètres de fonctionnement de l'APU*.

### Composition

- Grande courbe supérieure : `DimDate[CalendarDate]` en axe avec `[Pression moyenne TP3 (bar)]`, bleu industriel `#2474A6`.
- Deux courbes inférieures de même taille : `[Température moyenne huile (°C)]`, orange `#F59E0B`, puis `[Courant moyen moteur (A)]`, turquoise `#0D9488`.
- Slicer commun à gauche ou en bandeau inférieur : année, mois et date selon la hiérarchie existante.

### Format

Afficher l'unité dans chaque titre. Limiter le nombre d'étiquettes de l'axe X. Ne pas ajouter de lignes constantes de seuil. Les pics sont à interpréter avec le contexte des autres signaux et ne constituent pas seuls une panne confirmée.

## Page 3 — INCIDENT ANALYTICS & OLAP

Sous-titre : *Analyse des événements documentés et exploration multidimensionnelle*.

### Composition

- Bandeau supérieur : slicers `DimDate[MonthName]` et `DimTime[Hour]` dans deux cartes blanches compactes.
- Partie gauche : table historique des quatre incidents avec code, dates début/fin, durée en heures, type et gravité.
- Partie droite : barres horizontales, axe `FailureReportCode`, valeur observations associées, étiquettes de données activées.
- Partie basse : matrice OLAP avec année/mois/date en lignes et heures en colonnes, totaux activés, en-têtes marine et lignes alternées très légères.

### Contrôles

Trier les dates par la vraie colonne de date et non par texte. Formater les durées à deux décimales. Vérifier que les slicers filtrent table, histogramme et matrice. Conserver slice, dice, drill-down, roll-up et pivot uniquement lorsqu'ils sont effectivement démontrables dans le modèle.

## Captures HD pour le rapport

Les captures actuellement présentes mesurent 785×482, 791×485 et 793×486 px. Elles ne doivent pas être agrandies artificiellement. Après application du design, utiliser **Fichier > Exporter > Exporter au format PDF** ou une capture de la page Power BI Desktop à résolution native d'au moins 1600 px de largeur. Remplacer uniquement les PNG de `reports/figures/` après vérification visuelle.

Des pictogrammes SVG originaux et légers sont disponibles dans `powerbi/themes/icons/` : `sensor.svg`, `compressor.svg`, `maintenance.svg`, `incident.svg` et `analytics.svg`. Ils sont facultatifs et doivent rester discrets.

## Validation finale

- Ouvrir chaque page et vérifier l'alignement des cartes.
- Tester les slicers et les interactions entre visuels.
- Vérifier les quatre relations du modèle et les sept mesures sans modification.
- Comparer les KPI à 1 516 948 observations, 4 incidents, 29 954 observations incidentées et 1,97 % dans le contexte global.
- Enregistrer sous un nouveau nom, par exemple `Smart_Industrial_Maintenance_Premium.pbix`, après validation manuelle.
