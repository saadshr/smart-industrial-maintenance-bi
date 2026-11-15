# Dictionnaire des données — MetroPT-3

## Portée et sources

Ce dictionnaire s'appuie sur le PDF technique fourni avec le dataset et sur la documentation officielle :

- [MetroPT-3 Dataset — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/791/metropt+3+dataset)
- [Publication associée et métadonnées de citation](https://doi.org/10.24432/C5VW3R)

Le fichier local contient 15 signaux de capteurs et deux colonnes techniques. Le CSV utilise **Unnamed: 0** comme index technique, alors que la documentation décrit cette colonne comme **index**. Les noms réels du CSV sont utilisés ci-dessous ; les libellés documentaires sont indiqués lorsqu'ils diffèrent.

## Variables documentées et vérifiées

| Nom réel du CSV | Type observé | Unité documentée | Signification documentée | Catégorie | Utilisation BI envisagée |
| --- | --- | --- | --- | --- | --- |
| **Unnamed: 0** | int64 | Non spécifiée | Index technique de la donnée ; équivalent documentaire de index | Technique | Contrôle d'unicité et traçabilité ; ne pas considérer comme un identifiant d'équipement sans validation |
| **timestamp** | str, parsé en date-heure sans échec | Non spécifiée | Date et heure de l'observation | Temporelle | Axe temporel, tri, calcul des intervalles et association aux périodes de défaillance |
| **TP2** | float64 | bar | Pression sur le compresseur | Analogique | Évolution temporelle et statistiques descriptives |
| **TP3** | float64 | bar | Pression générée au niveau du panneau pneumatique | Analogique | Évolution temporelle et comparaison avec les autres pressions |
| **H1** | float64 | bar | Pression générée par la chute de pression lors de la décharge du filtre du séparateur cyclonique | Analogique | Évolution temporelle et analyse autour des événements |
| **DV_pressure** | float64 | bar | Chute de pression lors de la décharge des tours de séchage d'air ; une valeur nulle indique que le compresseur fonctionne en charge | Analogique | Analyse du fonctionnement en charge, sous réserve de validation du codage |
| **Reservoirs** | float64 | bar | Pression en aval des réservoirs, censée être proche de la pression du panneau pneumatique, TP3 | Analogique | Analyse de pression et comparaison avec TP3 |
| **Oil_temperature** | float64 | °C | Température de l'huile du compresseur | Analogique | Tendance et statistiques de température |
| **Motor_current** | float64 | A | Courant d'une phase du moteur triphasé | Analogique | Tendance et analyse des régimes documentés par la source |
| **COMP** | float64 ; valeurs 0.0/1.0 | Non spécifiée | Signal électrique de la vanne d'admission d'air ; actif lorsqu'il n'y a pas d'admission d'air, ce qui indique un compresseur arrêté ou déchargé | Numérique | Comptage et séquences d'états |
| **DV_eletric** (documentation : DV electric) | float64 ; valeurs 0.0/1.0 | Non spécifiée | Signal électrique commandant la vanne de sortie du compresseur ; actif lorsque le compresseur fonctionne en charge | Numérique | Analyse des états de fonctionnement |
| **Towers** (documentation : TOWERS) | float64 ; valeurs 0.0/1.0 | Non spécifiée | Signal définissant la tour responsable du séchage et de l'évacuation de l'humidité | Numérique | Analyse des états de commutation des tours |
| **MPG** | float64 ; valeurs 0.0/1.0 | Non spécifiée | Signal électrique de démarrage du compresseur en charge lorsque la pression de l'APU descend sous 8,2 bar | Numérique | Analyse des activations ; le seuil est une information documentaire, pas un KPI calculé |
| **LPS** | float64 ; valeurs 0.0/1.0 | Non spécifiée | Signal électrique qui détecte et s'active lorsque la pression descend sous 7 bar | Numérique | Analyse des activations ; le seuil est une information documentaire, pas un KPI calculé |
| **Pressure_switch** | float64 ; valeurs 0.0/1.0 | Non spécifiée | Signal électrique qui détecte la décharge dans les tours de séchage d'air | Numérique | Analyse des états et séquences |
| **Oil_level** | float64 ; valeurs 0.0/1.0 | Non spécifiée | Signal électrique qui détecte le niveau d'huile ; actif lorsque l'huile est sous le niveau attendu | Numérique | Analyse des alertes d'état, sans interpréter automatiquement le signal comme une panne |
| **Caudal_impulses** (documentation : Caudal Impulse) | float64 ; valeurs 0.0/1.0 | Non spécifiée | Signal électrique comptant les impulsions produites par la quantité absolue d'air allant de l'APU vers les réservoirs | Numérique | Analyse des impulsions et du fonctionnement |

## Résultats de l'audit local

- Le CSV contient **1 516 948 lignes et 17 colonnes**.
- **timestamp** est lu comme texte puis parsé sans échec ; les dates couvrent **2020-02-01 00:00:00** à **2020-09-01 03:59:50**.
- Les sept signaux analogiques et les huit signaux numériques sont lus comme **float64**.
- Aucune valeur nulle n'a été trouvée dans les 17 colonnes.
- L'index technique est unique, mais ses valeurs vont de 0 à 15 169 470 par pas de 10 ; il ne constitue donc pas un compteur séquentiel de lignes.
- Les huit signaux numériques observés prennent uniquement les valeurs 0.0 et 1.0.

## Points d'attention

- Les noms du CSV ne sont pas tous identiques aux libellés de la documentation : Unnamed: 0/index, DV_eletric/DV electric, Towers/TOWERS et Caudal_impulses/Caudal Impulse.
- Le CSV réel couvre jusqu'au 1er septembre 2020, alors que la documentation décrit une période allant de février à août 2020.
- Le PDF annonce 15 169 480 points dans deux passages ; le comptage du CSV réel est 1 516 948 lignes. Cette valeur du PDF doit être considérée comme une coquille documentaire.
- Le PDF annonce une acquisition à 1 Hz ; le CSV présente un intervalle modal de 10 secondes. La fréquence effective du fichier local doit être utilisée pour l'analyse.
- Les unités physiques des signaux analogiques sont documentées ; aucune unité supplémentaire ne doit être déduite des valeurs.
