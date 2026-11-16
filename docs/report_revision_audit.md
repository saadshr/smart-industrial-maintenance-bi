# Audit de révision du rapport BI MetroPT-3

## Périmètre contrôlé

- Template ENSAM Rabat et logos UM5/ENSAM conservés.
- Sources LaTeX : `BI_MetroPT_Report/main.tex`, `preamble.tex`, `references.bib` et tous les fichiers de `chapters/` lus.
- Données et implémentation : `scripts/prepare_powerbi_data.py`, fichiers `powerquery/*.pq`, `dax/measures.dax` et `powerbi/Smart_Industrial_Maintenance.pbix` inspectés.
- Trois captures présentes dans `reports/figures/` et leurs copies dans `BI_MetroPT_Report/figures/dashboards/` comparées.

## Constats factuels

Les captures disponibles mesurent 785 x 482, 791 x 485 et 793 x 486 pixels. Aucun original HD de 1600 pixels ou plus n'a été trouvé ; aucune interpolation artificielle n'a été utilisée. Le fichier PBIX est présent dans le dépôt, mais la lecture détaillée des visuels repose sur les captures effectivement disponibles.

Les résultats conservés sont 1 516 948 observations, 17 colonnes initiales, 15 signaux, 4 périodes externes et 29 954 observations rattachées aux fenêtres inclusives, soit 1,97 %. Les comptages par rapport sont 8 657, 2 360, 17 315 et 1 622.

## Corrections scientifiques

- Le mode Import Power BI n'est plus décrit automatiquement comme ROLAP : le rapport précise le rôle du modèle tabulaire et du stockage en mémoire, sans revendiquer un cube MOLAP ou une architecture ROLAP.
- La séparation entre préparation Python exécutée, CSV importés dans Power BI et scripts M préparés mais non prouvés comme exécutés est explicitée.
- Le grain des deux faits et la règle inclusive `StartTimestamp <= ObservationTimestamp <= EndTimestamp` sont détaillés.
- Les mesures additives, semi-additives et non additives sont distinguées.
- `CALCULATE`, le remplacement de filtres et l'usage potentiel de `KEEPFILTERS` sont expliqués.
- Le problème des quatre barres identiques est documenté comme un retour d'expérience de contexte de filtre, sans présenter une formule incorrecte comme résultat final.
- Les trous temporels ne sont pas convertis en arrêts et les variations de capteurs ne sont pas transformées en causalité ou en panne.

## Enrichissements

- Contexte industriel : architecture pneumatique ferroviaire, chaîne APU, composants, états génériques et limites de confirmation.
- Dataset : tableau analogique/numérique, lecture pédagogique des variables, relations entre signaux et conséquences de la cadence irrégulière.
- BI : tableau OLTP/OLAP, tableau Inmon/Kimball, grain, clés, cardinalités et niveaux d'additivité.
- Data Warehouse : relations actives/inactives, filtres, rôle des dimensions et association temporelle.
- ETL/DAX : tableau de statut des composants, tableau de lecture des sept mesures et distinction des dashboards.
- Dashboards : dimensions exactes, filtres visibles, résolution mesurée et procédure de reprise manuelle HD.
- Résultats : comparaison des quatre incidents et matrice question métier / indicateur / table / mesure / dashboard.
- Figures vectorielles TikZ ajoutées pour l'architecture ferroviaire, la chaîne BI et les opérations OLAP.

## Validation finale

La compilation finale avec les exécutables MiKTeX locaux a produit un PDF de 41 pages dans `BI_MetroPT_Report/output/BI_MetroPT_Report.pdf`. Le contrôle d'intégrité ne relève aucune erreur fatale ni page manquante. Les seuls avertissements restants sont des `Underfull \\hbox` non bloquants dans des tableaux compacts et un repli de police pour les petites capitales italiques. Aucun commit GitHub ni push n'est autorisé dans cette révision.
