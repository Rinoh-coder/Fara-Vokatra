# Baselines de détection de l’onset

## Objectif

Le module `src/onset.py` fournit deux baselines explicables avant tout modèle supervisé : une règle agronomique à seuils et une méthode d’anomalies cumulées inspirée de Liebmann. Elles opèrent sur une série quotidienne de précipitation agrégée pour une zone.

## Règle à seuils

La méthode cherche le premier jour d’une fenêtre de `window_days` dont le cumul dépasse `min_cumulative_mm`, contenant au moins un jour supérieur à `wet_day_mm`. Elle inspecte ensuite `lookahead_days` et rejette le candidat si une séquence d’au moins `max_dry_days` jours sous `dry_day_mm` apparaît. Ce contrôle prospectif vise à limiter les faux onsets.

Les paramètres par défaut sont des valeurs de démonstration et ne sont pas validés pour Madagascar. Ils doivent être testés par région, culture et type de saison. Une analyse de sensibilité devra rapporter l’effet de chaque paramètre sur la date détectée.

## Méthode des anomalies cumulées

La méthode calcule la somme cumulée de `pluie_jour - climatologie_jour` et retourne le minimum de cette somme. Une climatologie indépendante doit être utilisée pour une évaluation historique. Le mode de repli qui utilise la moyenne de la série est uniquement exploratoire et ne doit pas être présenté comme une validation hors échantillon.

## Validation prévue

Les tests actuels utilisent des séries synthétiques pour vérifier les propriétés logiques : rejet d’un faux onset, absence de détection sans fenêtre valide, calcul du minimum d’anomalie et validation des entrées. La prochaine étape est de relier ces fonctions à une série CHIRPS multi-années, puis de comparer les dates aux stations et aux informations agronomiques disponibles.

## Limites

Une détection météorologique ne prouve pas que le sol est prêt à semer. Les paramètres peuvent être instables selon la culture, le relief et le régime pluviométrique. Les années à deux saisons, les données manquantes et les calendriers agricoles non grégoriens devront être traités explicitement avant l’analyse régionale.
