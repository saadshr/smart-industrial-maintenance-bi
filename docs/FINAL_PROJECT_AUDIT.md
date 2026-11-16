# Final Project Audit — Smart Industrial Maintenance BI

Date de l'audit : 16 novembre 2026  
Dépôt : `smart-industrial-maintenance-bi`  
Branche inspectée : `main`

## 1. Verdict global

**READY FOR FINAL COMMIT**

Le dépôt contient les livrables finaux demandés : PBIX, sources et PDF du rapport LaTeX, PPTX modifiable, PDF final de soutenance, notes orales, scripts Python, requêtes M, mesures DAX et documentation du modèle. Les contrôles réalisés n'ont pas révélé d'incohérence bloquante entre les résultats vérifiables et les livrables.

Une réserve opérationnelle demeure : Power BI Desktop n'était pas piloté pendant cet audit. L'intégrité binaire du PBIX est vérifiée, mais les interactions visuelles ne sont pas revalidées ici par ouverture de Desktop.

## 2. Arborescence finale utile

```text
BI_MetroPT_Report/       # rapport académique LaTeX, figures et PDF
data/raw/                # CSV et documentation source, non suivis par Git
data/processed/          # tables dérivées, non suivies par Git
dax/                     # 7 mesures DAX
docs/                    # audits, guides et dictionnaire
model/                   # modèle dimensionnel, grains et bus matrix
powerbi/                 # PBIX, sauvegarde, thème et icônes
powerquery/              # paramètres et 4 requêtes M
presentation/            # 6 illustrations sources
presentation_pfe/        # assets, script, PPTX, PDF et notes
reports/figures/         # 3 captures pour la documentation
scripts/                 # audit et préparation reproductibles
```

## 3. Contrôle des données et du modèle

Le comptage direct du CSV source a confirmé :

| Contrôle | Résultat |
| --- | ---: |
| Lignes du CSV | 1 516 948 |
| Observations dans les fenêtres inclusives | 29 954 |
| Rapport #1 | 8 657 |
| Rapport #2 | 2 360 |
| Rapport #3 | 17 315 |
| Rapport #4 | 1 622 |
| Première observation | 2020-02-01 00:00:00 |
| Dernière observation | 2020-09-01 03:59:50 |

La somme des quatre rapports est 29 954, soit 1,97 % du volume source. La règle est temporelle et inclusive ; elle ne transforme pas chaque ligne associée en panne indépendante.

Le modèle documente quatre tables : `FactSensorObservation`, `FactFailurePeriod`, `DimDate` et `DimTime`. Les requêtes M se trouvent dans [`powerquery/`](../powerquery) et les sept mesures dans [`dax/measures.dax`](../dax/measures.dax). Les faits ne sont pas reliés directement entre eux.

## 4. Contrôles exécutés

| Vérification | État | Résultat |
| --- | --- | --- |
| Présence des dossiers principaux | PASS | `data`, `scripts`, `model`, `powerquery`, `dax`, `powerbi`, `docs`, rapport, présentation et figures présents |
| Pipeline source | PASS PARTIEL | Le script Python est présent et la logique de préparation est lisible ; son environnement pandas complet n'a pas pu être exécuté dans l'environnement d'audit |
| Comptage source | PASS | 1 516 948 lignes et 29 954 associations inclusives confirmés par lecture CSV standard |
| Mesures DAX | PASS | 7 expressions présentes dans `dax/measures.dax` |
| Requêtes M | PASS | Paramètre de chemin et quatre requêtes présentes |
| PBIX | PASS STRUCTUREL | Fichier et sauvegarde présents, en-tête ZIP valide ; interactions Power BI non testées dans Desktop |
| PPTX | PASS | Archive OOXML lisible, 22 diapositives, 22 notes, 8 médias embarqués |
| Rapport PDF | PASS | PDF final présent, en-tête `%PDF` et marqueur final `%%EOF` présents ; PDF déjà compilé et livré |
| PDF de soutenance | PASS | Nouveau fichier manuel identifié dans `presentation_pfe/output/`, conservé comme référence finale |
| Données brutes | PASS | `data/raw/` et `data/processed/` sont ignorés par Git |
| État Git | PASS | Aucune modification du PBIX, du rapport, du PPTX ou des données par cet audit |

Le script [`scripts/audit_data.py`](../scripts/audit_data.py) dépend de `pandas` et `pypdf`. L'interpréteur virtuel proposé par l'environnement n'était pas exécutable ; la validation quantitative ci-dessus a donc utilisé une lecture CSV Python standard, sans réécrire les fichiers du projet.

## 5. Validation Power BI

Fichiers présents :

- [`powerbi/Smart_Industrial_Maintenance.pbix`](../powerbi/Smart_Industrial_Maintenance.pbix)
- [`powerbi/Smart_Industrial_Maintenance_backup_20261116_035445.pbix`](../powerbi/Smart_Industrial_Maintenance_backup_20261116_035445.pbix)
- [`powerbi/themes/industrial_premium_theme.json`](../powerbi/themes/industrial_premium_theme.json)

Le PBIX et sa sauvegarde font chacun environ 67 MiB et commencent par la signature ZIP attendue d'un fichier PBIX. Cette vérification ne permet pas d'affirmer que les interactions, relations affichées ou filtres ont été ouverts dans Power BI Desktop pendant cet audit. Les chiffres de référence restent ceux validés dans les documents et captures : 1 516 948, 4, 29 954 et 1,97 %.

## 6. Validation du rapport scientifique

Le rapport final est [`BI_MetroPT_Report/output/BI_MetroPT_Report.pdf`](../BI_MetroPT_Report/output/BI_MetroPT_Report.pdf). Les sources principales sont [`BI_MetroPT_Report/main.tex`](../BI_MetroPT_Report/main.tex), [`BI_MetroPT_Report/preamble.tex`](../BI_MetroPT_Report/preamble.tex) et [`BI_MetroPT_Report/references.bib`](../BI_MetroPT_Report/references.bib).

La page de garde contient les trois auteurs, l'encadrante Pr. Safaâ Dafrallah, l'ENSAM Rabat, l'Université Mohammed V, la filière INDIA et l'année 2026/2027. Les figures des trois dashboards sont présentes dans `BI_MetroPT_Report/figures/dashboards/`. Le rapport distingue correctement l'association temporelle à une période documentée d'une panne ligne par ligne.

Le dépôt contient aussi les fichiers de compilation auxiliaires dans `BI_MetroPT_Report/output/`. Ils sont désormais couverts par le `.gitignore` pour les futures compilations ; les fichiers déjà suivis ne sont pas supprimés automatiquement.

## 7. Validation de la présentation finale

Les six illustrations sources sont présentes dans [`presentation/assets/`](../presentation/assets) et leurs copies de travail dans [`presentation_pfe/assets/`](../presentation_pfe/assets). Le PPTX modifiable est [`presentation_pfe/output/MetroPT3_PFE_Presentation_Premium.pptx`](../presentation_pfe/output/MetroPT3_PFE_Presentation_Premium.pptx). Le PDF ajouté manuellement et utilisé comme référence est [`presentation_pfe/output/SMART INDUSTRIAL MAINTENANCE — Version finale—.pdf`](<../presentation_pfe/output/SMART INDUSTRIAL MAINTENANCE — Version finale—.pdf>).

Le PPTX contient 22 diapositives et 22 notes orales. L'archive contient les trois dashboards et les illustrations techniques APU, compression de l'air et chaîne BI. La présentation conserve les quatre KPI et les informations institutionnelles. La version Canva correspondante est accessible via [la présentation finale Canva](https://www.canva.com/d/ATJE0o0qA9oBnpT).

Le PDF manuel est conservé tel quel et n'a pas été remplacé par une exportation ancienne. Aucun contrôle d'interactions Canva ou PowerPoint n'est substitué à une ouverture locale par l'utilisateur.

## 8. README et nettoyage réalisés

Modifications effectuées par cet audit :

1. Reconstruction de [`README.md`](../README.md) avec le statut réel des livrables, les auteurs, les KPI vérifiés, l'architecture, le pipeline, les mesures DAX, les dashboards, les livrables et les limites.
2. Ajout de ce document d'audit final.
3. Extension du [`.gitignore`](../.gitignore) aux artefacts LaTeX, runtimes de présentation et fichiers temporaires futurs.
4. Aucun fichier scientifique, image, source, donnée ou PBIX supprimé.

Le répertoire `presentation_pfe/.runtime/` contient des dépendances de génération déjà suivies par Git. Il est volumineux et redondant pour une exécution locale si le runtime peut être réinstallé, mais il n'a pas été désindexé afin de ne pas modifier l'historique sans accord explicite.

## 9. Problèmes restants

| Problème | Impact | État |
| --- | --- | --- |
| Power BI Desktop non ouvert pendant cet audit | Les interactions ne sont pas revalidées ici | Non bloquant pour le commit ; vérification manuelle recommandée |
| Environnement Python virtuel inaccessible dans cette session | Le script pandas complet n'a pas été relancé | Non bloquant ; le comptage CSV indépendant est PASS |
| Données brutes et tables dérivées absentes du suivi Git | Reproduction nécessite de fournir/télécharger les sources locales | Conforme à la protection des données volumineuses |
| Runtime Node suivi sous `presentation_pfe/.runtime/` | Dépôt plus lourd que nécessaire | À rationaliser dans un commit ultérieur si souhaité |
| Fichiers auxiliaires LaTeX déjà suivis | Bruit dans le dépôt | Ignorés pour les futures générations, non supprimés |

## 10. État Git et commit proposé

L'état Git avant les modifications documentaires était propre sur la branche `main`, alignée sur `origin/main`. Aucun `git add`, `git commit` ou `git push` n'a été exécuté par cet audit.

Après vérification du diff, les commandes proposées sont :

```powershell
git status
git add README.md .gitignore docs/FINAL_PROJECT_AUDIT.md
git commit -m "docs: finalize BI project, dashboards, report and presentation"
git push origin main
```

Ces commandes restent volontairement à exécuter manuellement après validation du propriétaire du dépôt.
