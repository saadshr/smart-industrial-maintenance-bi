# Audit exploratoire — MetroPT-3

## Méthode et reproductibilité

L'audit a été exécuté avec le script [audit_data.py](../scripts/audit_data.py), en lecture par blocs de 100 000 lignes. Le CSV original n'a pas été modifié. Les dépendances pandas et pypdf ont été utilisées uniquement dans l'environnement Python local.

Le PDF technique a été lu avec pypdf. Le script vérifie également que le PDF est lisible, comporte trois pages et contient du texte extractible.

## Vérification des fichiers

| Fichier | Présence | Taille | Contrôle |
| --- | --- | ---: | --- |
| data/raw/MetroPT3(AirCompressor).csv | Oui | 218 300 507 octets | Lecture complète réussie |
| data/raw/Data Description_Metro.pdf | Oui | 81 208 octets | Lecture complète réussie, 3 pages |

Les fichiers bruts restent exclus de Git par les règles data/raw/ et data/processed/ du fichier .gitignore.

Empreintes SHA-256 relevées après l'audit :

- CSV : `DB30CCB4EA402E3C8BF2C99DB06E288D4F2A772F6928F9DBE26A920D69793E24`
- PDF : `B00FAC0E8899854078309BEF4ADAA480D82ECF14DC81C5097C3646973E824127`

## Résumé des résultats

| Contrôle | Résultat réel | Interprétation et conséquence BI |
| --- | ---: | --- |
| Nombre de lignes | **1 516 948** | Conforme au nombre d'instances annoncé par l'UCI |
| Nombre de colonnes | **17** | Deux colonnes techniques et 15 signaux |
| Première date | **2020-02-01 00:00:00** | Début réel de la série observée |
| Dernière date | **2020-09-01 03:59:50** | Le fichier dépasse légèrement la période « février à août » annoncée dans la documentation |
| Échecs de parsing timestamp | **0** | Tous les timestamps ont été parsés avec succès |
| Valeurs nulles | **0** dans les 17 colonnes | Aucune imputation nécessaire sur ce contrôle |
| Doublons complets | **0 groupe, 0 ligne** par empreinte de ligne | Aucun doublon détecté ; le contrôle est basé sur des empreintes pandas |
| Timestamps répétés | **0** | Un timestamp n'apparaît pas plusieurs fois dans le fichier |
| Intervalles non croissants | **0** | L'ordre temporel est strictement croissant |
| Intervalle modal | **10 secondes** | Le fichier réel correspond à une cadence modale de 0,1 Hz, et non à 1 Hz |
| Intervalles supérieurs à 10 secondes | **51 147** | Irrégularités et trous temporels à traiter comme un sujet de qualité, sans imputation automatique |
| Plus grand intervalle | **172 918 secondes**, environ 47 h 58 min 38 s | Au moins une coupure temporelle majeure existe |

## Colonnes et types

Les 17 colonnes réelles sont :

**Unnamed: 0**, **timestamp**, **TP2**, **TP3**, **H1**, **DV_pressure**, **Reservoirs**, **Oil_temperature**, **Motor_current**, **COMP**, **DV_eletric**, **Towers**, **MPG**, **LPS**, **Pressure_switch**, **Oil_level**, **Caudal_impulses**.

Types observés :

- Unnamed: 0 : int64.
- timestamp : texte à la lecture pandas, parsé avec succès en date-heure.
- Les sept signaux analogiques : float64.
- Les huit signaux numériques : float64, avec uniquement les valeurs 0.0 et 1.0.

Écarts de nommage par rapport à la documentation : Unnamed: 0 correspond à index, DV_eletric à DV electric, Towers à TOWERS et Caudal_impulses à Caudal Impulse.

## Qualité temporelle

L'intervalle modal est de 10 secondes et 1 337 521 des 1 516 947 transitions ont exactement cet intervalle. Le fichier contient aussi des intervalles de 9, 11, 12 et 13 secondes, ainsi que des écarts beaucoup plus importants.

La conséquence BI est importante : les agrégations temporelles ne doivent pas supposer une série parfaitement régulière. Il faudra distinguer une observation absente, une coupure d'acquisition et un simple décalage de cadence. Aucune ligne ne doit être créée pour combler les trous avant qu'une règle métier et technique soit validée.

## Doublons, index et intégrité

Les doublons complets n'ont pas été détectés par empreinte de ligne. Aucun timestamp n'est répété. La colonne Unnamed: 0 est unique, mais ses valeurs vont de 0 à 15 169 470 par pas de 10 ; elle ne doit donc pas être utilisée comme un compteur séquentiel de lignes. Elle peut rester une clé technique de traçabilité, sous réserve de documenter son origine.

## Statistiques descriptives des signaux analogiques

| Signal | Unité | Minimum | Maximum | Moyenne | Écart-type |
| --- | --- | ---: | ---: | ---: | ---: |
| TP2 | bar | -0,032 | 10,676 | 1,367826 | 3,250930 |
| TP3 | bar | 0,730 | 10,302 | 8,984611 | 0,639095 |
| H1 | bar | -0,036 | 10,288 | 7,568155 | 3,333200 |
| DV_pressure | bar | -0,032 | 9,844 | 0,055956 | 0,382402 |
| Reservoirs | bar | 0,712 | 10,300 | 8,985233 | 0,638307 |
| Oil_temperature | °C | 15,400 | 89,050 | 62,644182 | 6,516261 |
| Motor_current | A | 0,020 | 9,295 | 2,050171 | 2,302053 |

Les minima légèrement négatifs de TP2, H1 et DV_pressure sont des valeurs à examiner, pas des erreurs à corriger automatiquement. Leur signification doit être confrontée à la précision des capteurs et à la documentation technique.

## Distributions des signaux numériques

| Signal réel | Valeur 0.0 | Valeur 1.0 | Total | Commentaire |
| --- | ---: | ---: | ---: | --- |
| COMP | 247 328 | 1 269 620 | 1 516 948 | Codage binaire observé |
| DV_eletric | 1 273 310 | 243 638 | 1 516 948 | Codage binaire observé |
| Towers | 121 586 | 1 395 362 | 1 516 948 | Codage binaire observé |
| MPG | 253 840 | 1 263 108 | 1 516 948 | Codage binaire observé |
| LPS | 1 511 760 | 5 188 | 1 516 948 | Valeur 1 rare, à interpréter avec la définition du signal |
| Pressure_switch | 12 990 | 1 503 958 | 1 516 948 | Valeur 0 rare, à interpréter avec la définition du signal |
| Oil_level | 145 391 | 1 371 557 | 1 516 948 | Valeur 0 minoritaire, sans la transformer directement en panne |
| Caudal_impulses | 95 406 | 1 421 542 | 1 516 948 | Codage binaire observé malgré le nom « impulse » |

La distribution binaire est un constat descriptif. Elle ne suffit pas à définir le sens métier de 0 et 1, ni à créer des labels de panne.

## Incidents externes documentés

La source indique que le dataset est non étiqueté et que les rapports de défaillance sont séparés du CSV. Les périodes ci-dessous sont conservées comme événements externes ; aucune colonne de panne n'a été ajoutée au fichier original.

| Rapport | Début | Fin | Défaillance | Gravité | Information de maintenance affichée par la source |
| --- | --- | --- | --- | --- | --- |
| #1 | 2020-04-18 00:00 | 2020-04-18 23:59 | Air leak | High stress | Non indiquée |
| #2 | 2020-05-29 23:30 | 2020-05-30 06:00 | Air leak | High stress | Maintenance on 30Apr at 12:00 |
| #3 | 2020-06-05 10:00 | 2020-06-07 14:30 | Air leak | High stress | Maintenance on 8Jun at 16:00 |
| #4 | 2020-07-15 14:30 | 2020-07-15 19:00 | Air leak | High stress | Maintenance on 16Jul at 00:00 |

Le rapport #2 présente une information de maintenance affichée au 30 avril, antérieure à la période du 29–30 mai. Cette anomalie documentaire doit être vérifiée et ne doit pas être corrigée automatiquement.

## Incohérences documentaires

- Le PDF technique contient deux mentions de 15 169 480 points ; le CSV réel contient 1 516 948 lignes. Le PDF comporte vraisemblablement un zéro supplémentaire.
- Le PDF technique annonce 1 Hz, alors que les timestamps réels ont un intervalle modal de 10 secondes. Le rythme réel du CSV doit prévaloir pour l'audit.
- La documentation décrit une période de février à août 2020, tandis que le dernier timestamp observé est le 1er septembre 2020 à 03:59:50.
- Les libellés de quatre colonnes diffèrent entre la documentation et le CSV. Cette correspondance doit être conservée dans le dictionnaire de données.

## Recommandations pour la suite BI

1. Conserver le CSV brut hors Git et documenter son empreinte ou sa provenance.
2. Utiliser timestamp comme référence temporelle, après confirmation du fuseau horaire.
3. Ne pas utiliser Unnamed: 0 comme compteur de lignes ; le garder uniquement comme attribut technique traçable.
4. Ajouter des contrôles de couverture temporelle et de durée des trous avant toute agrégation.
5. Conserver les signaux numériques comme états binaires, sans interpréter automatiquement 0 ou 1 comme une panne.
6. Traiter les quatre incidents comme une table externe d'événements documentés, sans modifier le CSV ni créer de labels originaux.
7. Examiner les valeurs négatives des pressions avec la documentation capteur avant toute règle d'anomalie.
8. Ne commencer la modélisation multidimensionnelle qu'après validation de cet audit.

## Sources et licence

- [MetroPT-3 Dataset — UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/791/metropt+3+dataset)
- [DOI du dataset](https://doi.org/10.24432/C5VW3R)
- [Licence Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
