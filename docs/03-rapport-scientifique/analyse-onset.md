# Analyse des dates d’onset — protocole et interprétation

## Résumé pour un lecteur non technique

Cette étape transforme une série quotidienne de pluie en une estimation du début de la saison humide pour chaque année. Deux méthodes sont comparées. La première cherche une séquence de pluie suffisante et vérifie qu’elle n’est pas immédiatement suivie d’une longue période sèche. La seconde compare la pluie de l’année à une climatologie calculée à partir d’autres années.

Le résultat est une date estimée, pas une certitude sur la date de semis. Une date d’onset météorologique ne garantit pas que le sol soit suffisamment humide, que les semences soient disponibles ou que les conditions agronomiques soient favorables.

## Question scientifique

Les deux méthodes donnent-elles des dates cohérentes sur les années couvertes par CHIRPS, et dans quelles situations divergent-elles fortement ? Cette question est descriptive et falsifiable. Elle ne prétend pas encore démontrer une amélioration du rendement.

## Données d’entrée

Le programme attend la table produite par `src/chirps_series.py`. Chaque ligne contient une date, une pluie moyenne en millimètres par jour et une fraction de couverture valide. Les journées sans moyenne ne sont pas imputées. Une année est considérée comme exploitable uniquement si les 365 jours non bissextiles sont présents.

## Méthode de validation contre la fuite d’information

Pour calculer la méthode d’anomalies cumulées pour une année donnée, la climatologie quotidienne est calculée avec les autres années disponibles, sans inclure l’année évaluée. Cette stratégie dite « leave-one-year-out » évite que l’année test contribue à sa propre référence.

Une année incomplète est signalée avec le statut `incomplete`. Lorsqu’une seule année est disponible, la méthode Liebmann reçoit le statut `no_independent_climatology` et n’est pas produite. Cette décision est volontaire : une moyenne calculée sur la même année ne constitue pas une référence indépendante.

## Sorties

La table de résultats contient le statut de qualité, le nombre de jours utilisés, le jour de l’année estimé par chaque méthode et le nombre d’années utilisées pour la climatologie. Les divergences entre méthodes doivent être analysées comme des cas à expliquer, et non comme une preuve automatique qu’une méthode est correcte.

## Limites

La première version agrège une BBOX et ne représente pas nécessairement une région administrative ou une zone cultivée. Les seuils sont des paramètres de démonstration. La période climatique, les années atypiques, les données manquantes et les différences entre pluies satellite et stations peuvent modifier les dates estimées.

Avant toute conclusion agricole, il faut comparer les dates à des observations locales, à l’humidité du sol et aux calendriers culturaux documentés. Les performances devront ensuite être mesurées sur des années tenues à l’écart, avec une analyse d’incertitude et une revue agronomique.

## Commande

```bash
python3 src/season_analysis.py \
  --input data/processed/chirps/series/daily.csv \
  --output reports/onsets.csv
```
