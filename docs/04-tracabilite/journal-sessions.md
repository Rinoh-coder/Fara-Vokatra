# Journal des sessions

## Session 2026-09-17 — Initialisation documentaire

### Objectif
Transformer le brief initial en base de projet scientifique traçable et préparer la recherche des ressources ouvertes.

### Actions réalisées

Le dépôt vide a été initialisé avec une structure documentaire. Le contexte vivant, le cadrage scientifique, le registre des hypothèses, la spécification du MVP, le backlog, le rapport scientifique, le README et les registres de provenance ont été créés.

### Décisions

Le périmètre prioritaire est le MVP d’onset. Les affirmations socio-économiques et agricoles du brief sont conservées comme hypothèses à vérifier. La recherche des ressources sera organisée par thèmes indépendants : climat, rendements, onset, prévision, optimisation et reproductibilité.

### Résultats

Aucun résultat empirique n’a été produit. La prochaine étape est de consolider les rapports de recherche, puis de sélectionner les données selon leur licence et leur capacité à soutenir une validation temporelle.

### Points ouverts

La définition exacte de l’onset, la source climatique principale, la disponibilité des rendements régionaux, la licence du code et la participation d’un référent agronomique restent à préciser.

## Session 2026-09-17 — Pipeline CHIRPS

### Actions réalisées

Une branche `feat/chirps-download-cleaning` a été créée. Le script `src/chirps_pipeline.py` télécharge CHIRPS v3 final/rnl, recadre une BBOX, transforme les valeurs invalides en nodata, calcule des empreintes SHA-256 et génère un manifeste JSON. Les rasters bruts et dérivés restent ignorés par Git.

### Validation

Trois tests unitaires passent. Un téléchargement CHIRPS réel sur une journée et une petite emprise a également été exécuté avec succès dans `/tmp`, sans ajouter de données volumineuses au dépôt.

### Points ouverts

La BBOX doit être remplacée par une géométrie officielle de la zone d’étude lorsque celle-ci sera définie. La couverture, les biais par région et la comparaison à des stations restent à évaluer.
