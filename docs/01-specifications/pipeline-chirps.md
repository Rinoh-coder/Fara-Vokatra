# Pipeline CHIRPS v3 — téléchargement et nettoyage

## Objectif

Le script `src/chirps_pipeline.py` télécharge les rasters quotidiens CHIRPS v3, conserve les originaux hors Git, découpe chaque raster sur une emprise géographique et écrit un GeoTIFF nettoyé ainsi qu’un manifeste JSON de provenance.

La source par défaut est CHIRPS v3 **final/rnl**. `rnl` utilise ERA5 pour désagréger les cumuls pentadaires en valeurs quotidiennes. Le produit `sat`, fondé sur IMERG, est disponible comme option. Le choix doit être conservé dans le manifeste, car ces produits ne sont pas interchangeables.

## Zone d’étude initiale

En l’absence d’une emprise régionale fournie, le prototype accepte une BBOX explicite. Pour une première vérification de Madagascar, utiliser approximativement : ouest `43.0`, sud `-26.0`, est `51.0`, nord `-11.0`. Cette emprise est une zone de téléchargement technique et ne constitue pas encore une définition administrative ou agronomique de la zone d’étude.

## Exemple

```bash
python src/chirps_pipeline.py \
  --start 2024-01-01 \
  --end 2024-01-03 \
  --bbox 43 -26 51 -11 \
  --product rnl \
  --stage final \
  --data-root data
```

Chaque journée produit un fichier dans `data/processed/chirps/` et une entrée dans le manifeste. Les fichiers bruts se trouvent dans `data/raw/chirps/` et sont ignorés par Git.

## Contrôles appliqués

Le script vérifie la réponse HTTP et évite de télécharger à nouveau un fichier déjà présent. Il calcule un SHA-256 du brut et du fichier nettoyé. Il recadre l’emprise, convertit les valeurs en `float32`, transforme les valeurs négatives ou non finies en nodata `-9999`, compresse le GeoTIFF et ajoute des tags de provenance.

Le script échoue si une date est introuvable ou si une erreur est enregistrée dans le manifeste. Il ne remplit pas les valeurs manquantes et ne corrige pas les biais climatiques. Ces choix doivent rester explicites dans l’analyse.

## Licence et citation

CHIRPS v3 est présenté par le Climate Hazards Center comme disponible sous CC BY 4.0, avec renonciation au droit dans la mesure permise par la loi. La citation, la date d’accès et la version doivent être conservées dans les rapports. Source : <https://www.chc.ucsb.edu/data/chirps3>.

## Limites

Une valeur CHIRPS est une estimation surfacique et non une mesure locale. La BBOX ne remplace pas une géométrie administrative ou une zone de culture. Le script ne télécharge pas automatiquement les frontières ni les stations météorologiques. Toute analyse d’onset devra comparer plusieurs zones, versions et, lorsque possible, observations de stations.
