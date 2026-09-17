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

La sortie est un rapport JSON contenant `valid`, les anomalies et les dimensions attendues. Le statut `valid=true` est un contrôle de cohérence du pipeline, pas une preuve que CHIRPS est sans biais ni que l’onset est agronomiquement exact.

## Commande

```bash
python3 src/manifest_validator.py \
  --manifest data/processed/chirps/manifests/multi_zone_20240101_20240103_rnl_final.json \
  --output reports/quality/multi_zone_quality.json
```

Le code retour vaut `0` si le manifeste est cohérent, `2` si des anomalies sont détectées et `1` si le rapport ne peut pas être construit. `--skip-file-check` permet de vérifier uniquement la structure d’un manifeste déplacé sans ses fichiers, mais ce mode ne doit pas être utilisé pour déclarer un jeu de données prêt à l’analyse.

## Règle scientifique

Aucune série multi-zone ne doit alimenter l’analyse d’onset tant que son manifeste n’a pas été contrôlé et archivé avec le rapport de qualité. Un manifeste invalide devient une information de traçabilité, jamais une raison d’imputer silencieusement les données manquantes.
