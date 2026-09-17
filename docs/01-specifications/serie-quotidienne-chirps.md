# Série quotidienne régionale CHIRPS

## Objectif

`src/chirps_series.py` transforme les GeoTIFF CHIRPS nettoyés par le pipeline de téléchargement en une table quotidienne auditable. Pour chaque date, la première version calcule la moyenne spatiale des pixels valides dans la BBOX déjà découpée.

## Contrôle de couverture

La colonne `coverage_fraction` est le rapport entre les pixels valides et le nombre total de pixels du raster. Si cette couverture est inférieure à `--min-coverage`, la moyenne est laissée vide plutôt que d’être imputée. Ce choix évite de transformer une absence d’observation en pluie nulle.

Les colonnes produites sont `date`, `mean_mm`, `valid_pixels`, `total_pixels`, `coverage_fraction`, `min_mm` et `max_mm`. Les valeurs sont exprimées en millimètres par jour, conformément aux métadonnées du pipeline CHIRPS.

## Exemple

```bash
python3 src/chirps_series.py \
  --input-dir data/processed/chirps/final/rnl \
  --output data/processed/chirps/series/daily.csv \
  --min-coverage 0.95 \
  --start 2024-01-01 \
  --end 2024-12-31
```

Lorsque `--start` et `--end` sont utilisés, le script vérifie qu’un fichier existe pour chaque journée attendue. Cette vérification ne garantit pas la qualité scientifique de la donnée ; elle détecte uniquement les trous de fichiers.

## Limites scientifiques

La moyenne spatiale d’une BBOX n’est pas une moyenne administrative pondérée par surface et ne tient pas compte des zones réellement cultivées. La prochaine version devra accepter une géométrie de zone d’étude et documenter le masque spatial utilisé. La couverture pixel ne mesure pas le biais de CHIRPS ni sa représentativité pluviométrique.

La table produite constitue une variable intermédiaire pour l’onset. Elle ne doit pas être utilisée seule pour conclure à l’état agronomique des sols ou à la réussite d’un semis.
