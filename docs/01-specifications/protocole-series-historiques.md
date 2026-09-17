# Protocole des séries historiques CHIRPS

## Objet

Ce protocole transforme les GeoTIFF nettoyés et validés en une série quotidienne par boîte d’échantillonnage. Il ne doit être appliqué qu’à des années dont le manifeste et le rapport qualité sont valides.

## Unité d’observation

Une ligne correspond à une date et une zone. La valeur principale `mean_mm` est la moyenne des pixels valides de la boîte, exprimée en millimètres par jour. Les colonnes `valid_pixels`, `total_pixels` et `coverage_fraction` rendent visible la qualité spatiale de cette moyenne.

Une date dont la couverture est inférieure à 0,95 est conservée comme date observée mais sa moyenne est enregistrée comme manquante. Cette règle évite de présenter une moyenne calculée sur une fraction non représentative de la boîte comme une observation complète.

## Contrôles temporels

Pour chaque année civile :

1. compter 365 jours, ou 366 pour une année bissextile ;
2. vérifier l’unicité des dates ;
3. vérifier l’absence de date en dehors de l’année ;
4. vérifier les cinq zones attendues ;
5. conserver les jours manquants dans un rapport d’anomalie plutôt que de les imputer automatiquement.

Les années 1991–2020 constituent la référence. Les années 2021–2024 sont évaluées séparément. Aucune statistique de référence ne doit utiliser l’année évaluée lorsque l’objectif est un backtesting.

## Contrôles numériques

Les précipitations négatives et les valeurs nodata sont exclues des statistiques. Les valeurs sont conservées en millimètres par jour. Les minima, maxima, nombre de pixels valides et nombre de pixels nodata sont conservés pour audit.

Une série complète est un produit de données validé, pas une preuve de qualité locale. CHIRPS est une estimation maillée ; les séries doivent être comparées à des observations indépendantes dès qu’une source de stations documentée sera disponible.

## Sorties attendues

```text
data/processed/chirps/series/<zone_id>/daily_1991.csv
data/processed/chirps/series/<zone_id>/daily_1992.csv
...
data/processed/chirps/series/<zone_id>/series_1991_2024.csv
```

Chaque fichier doit être accompagné d’un manifeste ou d’un rapport indiquant les années incluses, les dates manquantes, la version CHIRPS, le seuil de couverture et la commande utilisée.

## Reproductibilité

La génération des séries s’effectue avec `src/chirps_series.py`. Toute modification du seuil de couverture, de l’emprise ou de la version du produit doit produire une nouvelle fiche d’expérience et une nouvelle version de sortie. Les séries ne doivent pas être écrasées silencieusement.

## Limites d’interprétation

Une moyenne spatiale quotidienne ne représente pas nécessairement la pluie reçue par chaque agriculteur. Les différences entre zones sont descriptives tant qu’elles n’ont pas été confrontées à une validation locale et à une analyse d’incertitude.
