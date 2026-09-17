# Pilote multi-zone CHIRPS

## Objectif

`src/multi_zone_download.py` exécute le pipeline CHIRPS sur plusieurs boîtes d’échantillonnage en partageant un seul fichier brut par date et en écrivant un résultat nettoyé séparé pour chaque zone. Cette organisation évite les téléchargements redondants et interdit l’écrasement silencieux des sorties entre zones.

## Exemple limité

```bash
python3 src/multi_zone_download.py \
  --zones config/zones_madagascar.json \
  --start 2024-01-01 \
  --end 2024-01-03 \
  --data-root data
```

Le premier essai recommandé porte sur trois jours seulement. Il vérifie l’accès, les URL, les dimensions des sorties, les valeurs nodata et les chemins par zone. Il ne constitue pas encore un jeu d’analyse scientifique.

## Organisation des fichiers

Le brut est écrit dans `data/raw/chirps/<stage>/<product>/YYYYMMDD.tif`. Les sorties sont écrites dans `data/processed/chirps/<stage>/<product>/<zone_id>/YYYYMMDD.tif`. Le manifeste global est placé dans `data/processed/chirps/manifests/`.

Le brut partagé est une optimisation de stockage, pas une modification de méthode. Chaque sortie conserve le SHA-256 du brut et son propre SHA-256. Les configurations de zones, dates, produit et stage sont enregistrées dans le manifeste.

## Usage du Drive

Le Drive peut servir d’archive de travail pour les fichiers CHIRPS volumineux et les rapports générés. Le dépôt Git ne doit conserver que le code, les configurations, les manifestes légers, les tests et les documents. Toute archive Drive doit conserver son manifeste, sa version de dataset, sa date d’accès et sa licence.

## Limites

Les boîtes restent exploratoires. Le pilote ne télécharge pas les frontières administratives, ne masque pas les terres cultivées et ne valide pas les données par station. Après ce pilote, il faudra vérifier que les rasters produisent une série quotidienne complète avant de lancer une période multi-années.
