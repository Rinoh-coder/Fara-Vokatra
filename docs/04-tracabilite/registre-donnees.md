# Registre des données et de la provenance

Ce registre distingue les sources candidates des données effectivement utilisées. Une source ne devient « retenue » qu’après contrôle de couverture, version, unités, qualité, licence et reproductibilité d’accès.

| ID | Jeu de données | Fournisseur | Usage envisagé | Couverture/résolution | Licence ou accès | Statut | Limites principales |
|---|---|---|---|---|---|---|---|
| DATA-001 | CHIRPS quotidien | Climate Hazards Center | Pluie, onset, sécheresse | 1981–présent ; 0,05° | Domaine public dans la mesure permise ; vérifier version | Candidat prioritaire | Estimation maillée, biais relief, transition v2–v3 |
| DATA-002 | ERA5-Land | Copernicus CDS | Température, sol, évaporation | Depuis 1950 ; environ 0,1° | CC-BY selon fiche consultée | Candidat complémentaire | Réanalyse, pas observation locale |
| DATA-003 | NASA POWER | NASA | Prototype point ou variables météo | 1981–présent selon variable | Conditions API à vérifier | Candidat complémentaire | Résolution et mélange de produits |
| DATA-004 | FAOSTAT/HDX Crops and Livestock | FAO / HDX | Production, superficie, rendement | 1961–2024 ; surtout national | CC BY-IGO indiqué par HDX ; vérifier FAO | Candidat rendement | Définitions et granularité variables |
| DATA-005 | HarvestStat-Africa | HarvestStat | Statistiques infranationales | Madagascar ADM2 selon dépôt | MIT indiqué par dépôt | À auditer | Sources harmonisées, couverture à confirmer |
| DATA-006 | Calendrier agricole Madagascar | FAO | Fenêtres culturales et contraintes | National/régional selon document | CC BY-NC-SA 3.0 indiqué | Référence contextuelle | Ne remplace pas les calendriers locaux |
| DATA-007 | C3S Seasonal Forecast | Copernicus CDS | Prévision probabiliste | Hindcasts 1993–2016 ; grille 1° | CC-BY selon fiche ; vérifier | Hors MVP immédiat | Résolution grossière, compte CDS |
| DATA-008 | Stations météorologiques | DGM Madagascar | Validation locale | À obtenir | À négocier/vérifier | Non disponible | Accès, métadonnées et qualité inconnus |
| DATA-009 | CHIRPS v3 daily final/rnl | Climate Hazards Center | Pipeline MVP, pluie quotidienne | 1981–présent ; 0,05° | CC BY 4.0 selon page officielle | Implémenté | Valeurs quotidiennes désagrégées ; biais de maille et relief |

## Manifeste minimal requis pour une donnée utilisée

Pour chaque téléchargement, conserver l’URL ou la requête, la date d’accès, la version, le checksum si possible, les unités, la projection, la période, le traitement, la licence et le chemin de sortie. Les fichiers volumineux ne sont pas committés ; un script idempotent doit permettre de les récupérer.

## Sources détaillées

Voir `docs/05-recherche/01-climat.md`, `02-rendements.md`, `03-onset.md`, `04-prevision.md`, `05-optimisation.md` et `06-reproductibilite.md`.

Le script utilisé pour DATA-009 est `src/chirps_pipeline.py`. La version, l’URL exacte, les empreintes SHA-256 et les paramètres de découpage sont écrits dans le manifeste JSON généré sous `data/processed/chirps/manifests/`.
