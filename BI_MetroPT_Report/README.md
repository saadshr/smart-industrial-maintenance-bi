# Rapport LaTeX BI MetroPT-3

Ce dossier reprend l'identité graphique du rapport ML précédent : classe book, logos UM5/ENSAM, palette navy/gold, en-têtes fancyhdr, boîtes pédagogiques et bibliographie biblatex.

## Compilation

Depuis ce dossier, utiliser :

    pdflatex -interaction=nonstopmode main.tex
    biber main
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex

La compilation de validation a été effectuée avec MiKTeX 26.5 installé localement, en appelant directement les exécutables depuis `C:\Users\hp\AppData\Local\Programs\MiKTeX\miktex\bin\x64` ; le PATH système n'a pas été modifié. Le moteur retenu est pdfLaTeX avec Biber. Le PDF validé est généré dans `output/`.

Les chiffres du texte proviennent de l'audit local et des captures effectivement présentes dans le dépôt. Les captures Power BI sont des artefacts inspectés ; le fichier PBIX reste la source de validation interactive.
