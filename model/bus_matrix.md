# Matrice en bus — Smart Industrial Maintenance BI

## Principe

La matrice en bus relie les processus métier aux dimensions conformes. Une case indique qu'une dimension décrit le processus et peut servir de filtre ou de regroupement. Elle ne signifie pas qu'une relation physique a déjà été implémentée.

## Matrice

| Processus / fait | DimDate | DimTime | DimSignal |
| --- | :---: | :---: | :---: |
| Observation des capteurs | X | X | - |
| Période de défaillance documentée | Rôles début/fin | - | - |

## Lecture de la matrice

### Observation des capteurs

FactSensorObservation utilise DimDate et DimTime grâce au timestamp de chaque ligne. DimSignal n'est pas retenue dans le modèle physique recommandé, car le fait conserve les 15 signaux en colonnes dans le format large original. Une dimension DimSignal deviendrait naturelle uniquement si une table longue était choisie plus tard.

La période de défaillance n'est pas une dimension ordinaire appliquée par date seule. Une association future doit comparer ObservationTimestamp à StartTimestamp et EndTimestamp. Elle peut produire une clé d'événement dérivée ou une table de pont, mais ne doit pas modifier la source originale.

### Période de défaillance documentée

FactFailurePeriod utilise DimDate deux fois, avec deux rôles Power BI :

- StartDate : date de début de l'intervalle, relation active ;
- EndDate : date de fin de l'intervalle, relation inactive à activer explicitement pour les analyses par date de fin.

Le code de rapport, le type Air leak, la gravité High stress et la note de maintenance sont des attributs provenant de la source externe. Les notes de maintenance ne constituent pas un processus de maintenance complet.

## Dimensions conformes

| Dimension | Processus concernés | Pourquoi elle est conforme |
| --- | --- | --- |
| DimDate | Observations et périodes externes | Même calendrier civil, avec des rôles de date différents pour le fait des incidents |
| DimTime | Observations | Même définition de l'heure de la journée pour toutes les observations |

DimDate et DimTime sont les dimensions partagées du modèle. DimSignal reste une option de variante long format et n'est pas nécessaire dans le schéma large recommandé. La référence aux rapports externes reste un attribut de FactFailurePeriod, pas une dimension supplémentaire. Aucun référentiel d'équipement, de site, de coût ou d'intervention n'est conforme car aucune source validée ne le fournit.

## Dimensions volontairement absentes

- **DimEquipment :** aucun identifiant d'équipement métier distinct n'est présent ; le dataset décrit le compresseur étudié.
- **DimSite :** aucune localisation d'exploitation n'est fournie comme dimension analytique ; le contexte portugais est une attribution de source, pas un axe de parc marocain.
- **DimMaintenance :** les mentions de maintenance des rapports sont ponctuelles et ambiguës ; elles ne suffisent pas à créer des interventions.
- **DimOperationalState :** aucun état métier global validé ne peut être déduit automatiquement des huit signaux numériques.
- **DimSignal dans le modèle principal :** inutile avec le fait large ; elle sera réévaluée uniquement si la variante long format est retenue.

## Conséquence pour Power BI

Le modèle peut être présenté comme deux étoiles partageant DimDate et DimTime. Les dimensions conformes permettent des analyses temporelles comparables sans forcer une relation artificielle entre des faits de grains différents.
