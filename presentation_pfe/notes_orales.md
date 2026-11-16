# Notes orales — SMART INDUSTRIAL MAINTENANCE

Les notes sont également intégrées dans le fichier PowerPoint. Elles suivent les 22 diapositives dans l’ordre.

1. Présenter la chaîne complète, des capteurs de l’APU jusqu’à l’exploration OLAP.
2. Annoncer quatre axes : contexte industriel, données et architecture, résultats Power BI, puis bilan.
3. Expliquer pourquoi les mesures doivent être contextualisées pour devenir décisionnelles.
4. Décrire les composants de l’APU : prise d’air, filtration, moteur, compresseur, refroidissement, réservoir et distribution.
5. Relier les étapes physiques du procédé aux points de surveillance.
6. Présenter le passage des capteurs au contexte temporel, puis aux KPI et à la question technique. Une variation capteur ne confirme pas une panne.
7. Donner les chiffres de périmètre : 1 516 948 observations, 17 colonnes, cadence modale de 10 secondes, février à septembre 2020.
8. Distinguer visuellement les mesures continues des états et commandes numériques 0/1. Un état numérique ne compte pas les pannes.
9. Présenter la chaîne IoT, ETL, modèle en étoile, DAX, dashboards et décision.
10. Expliquer le pipeline ETL : audit, Power Query, modèle, DAX puis pages Power BI, avec un contrôle à chaque étape.
11. Décrire les quatre relations temporelles : DimDate et DimTime vers chaque fait, dont une inactive. Aucune relation directe entre les faits.
12. Rappeler la règle inclusive : Observation.Timestamp ∈ [StartTimestamp, EndTimestamp]. Un incident documenté reste un seul incident.
13. Présenter les KPI strictement vérifiés : 1 516 948, 4, 29 954 et 1,97 %.
14. Introduire la vue générale comme synthèse exécutive ; l’image est une illustration de présentation.
15. Montrer le passage des volumes globaux vers les tendances et les durées d’incident.
16. Introduire les trois courbes : pression TP3, température d’huile et courant moteur.
17. Préciser que les variations sont des signaux à investiguer, pas des pannes confirmées.
18. Présenter l’historique des quatre incidents, l’histogramme, la matrice et les segments temporels.
19. Démontrer slice, dice, drill-down et roll-up avec l’exemple total annuel, mois, tranche horaire et observations.
20. Introduire le bilan et la prudence scientifique avant la conclusion.
21. Séparer ce que le projet établit de ce qu’il ne conclut pas : pas de coûts, MTTR, disponibilité ou seuils inventés.
22. Conclure par la proposition centrale et ouvrir les questions.

## Sources de présentation

- Rapport scientifique : `BI_MetroPT_Report/output/BI_MetroPT_Report.pdf`.
- Illustrations et dashboards fournis : `presentation/assets/`.
- Résultats KPI conservés : 1 516 948 observations, 4 incidents documentés, 29 954 observations incidentées, 1,97 %.
