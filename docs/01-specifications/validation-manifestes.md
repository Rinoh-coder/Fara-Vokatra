# Validation des manifestes CHIRPS

## Pourquoi cette étape est nécessaire

Un téléchargement qui se termine sans erreur réseau ne garantit pas qu’un jeu de données est complet. Une date peut manquer, une zone peut ne pas avoir été découpée, un fichier peut être dupliqué ou une sortie peut avoir été modifiée après le téléchargement. Le validateur transforme ces risques en contrôles explicites avant toute analyse d’onset.

## Contrôles réalisés

Le module `src/manifest_validator.py` vérifie :

- le nombre attendu de couples date/zone ;
- les dates manquantes ;
- les zones inattendues ;
- les doublons ;
- les erreurs enregistrées dans le manifeste ;
- l’existence des fichiers bruts et nettoyés ;
- les checksums SHA-256 des fichiers présents.

Le module `src/annual_quality.py` ajoute le contrôle de couverture spatiale. Les BBOX de Madagascar peuvent inclure l’océan : comparer les pixels valides à tous les pixels de la BBOX confondrait donc « pixel hors terre » et « donnée manquante ». Depuis la version 0.2, une empreinte stable est construite par zone avec les pixels valides au moins 95 % des jours disponibles. La couverture quotidienne est calculée uniquement à l’intérieur de cette empreinte et la fraction terrestre de la BBOX est conservée dans `stable_land_footprint`.

La sortie est un rapport JSON contenant `valid`, les anomalies et les dimensions attendues. Le statut `valid=true` est un contrôle de cohérence du pipeline, pas une preuve que CHIRPS est sans biais ni que l’onset est agronomiquement exact.

## Commande

```bash
python3 -m src.annual_quality \
  --manifest data/processed/chirps/manifests/year_1991_rnl_final.json \
  --output reports/quality/year_1991_quality.json
```

Le code retour vaut `0` si le manifeste et la couverture terrestre sont cohérents, `2` si des anomalies sont détectées et `1` si le rapport ne peut pas être construit. Le contrôle structurel peut être effectué séparément avec `src/manifest_validator.py`.

## Règle scientifique

Aucune série multi-zone ne doit alimenter l’analyse d’onset tant que son manifeste n’a pas été contrôlé et archivé avec le rapport de qualité. Un manifeste invalide devient une information de traçabilité, jamais une raison d’imputer silencieusement les données manquantes. Une année complète ne constitue pas une validation de l’exactitude de CHIRPS ; une comparaison avec des stations indépendantes reste nécessaire.
