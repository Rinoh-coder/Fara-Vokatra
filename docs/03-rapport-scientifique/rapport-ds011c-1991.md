# Rapport scientifique DS-011C — Collecte CHIRPS 1991

**Version :** 1.0 — 2026-09-17  
**Statut :** collecte complète et contrôle qualité validé

## Résumé accessible

L’année 1991 a été collectée à partir des fichiers quotidiens CHIRPS v3 pour cinq boîtes d’échantillonnage à Madagascar. Chaque journée a été téléchargée, découpée par zone, contrôlée par checksum, puis le fichier brut a été supprimé après validation. Le résultat contient 365 jours pour chacune des cinq zones, soit 1 825 observations spatiales quotidiennes.

## Résultat de collecte

| Élément | Résultat |
|---|---:|
| Période | 1 janvier–31 décembre 1991 |
| Zones | 5 |
| Jours attendus | 365 |
| Couples date-zone attendus | 1 825 |
| Couples observés | 1 825 |
| Dates manquantes | 0 |
| Doublons | 0 |
| Fichiers nettoyés | 1 825 |
| Fichiers partiels résiduels | 0 |
| Rapport qualité | `valid=true` |

## Correction méthodologique importante

Le premier rapport comparait les pixels valides à tous les pixels des rectangles géographiques. Cette comparaison pénalisait artificiellement les zones qui incluent l’océan. Par exemple, la BBOX Nord-Ouest ne contient qu’environ 22,8 % de pixels terrestres dans la grille CHIRPS, tandis que la BBOX des Hautes Terres en contient environ 97,7 %.

La version 0.2 du contrôle qualité définit donc une **empreinte terrestre stable** comme les pixels valides au moins 95 % des jours de l’année. La couverture d’une journée est ensuite calculée uniquement à l’intérieur de cette empreinte. Cette règle sépare la géométrie fixe de la BBOX des véritables données manquantes temporelles.

| Zone | Pixels terrestres stables | Fraction terrestre de la BBOX | Couverture minimale dans l’empreinte |
|---|---:|---:|---:|
| Est | 2 884 | 36,05 % | 100 % |
| Hautes Terres | 5 274 | 97,67 % | 100 % |
| Nord-Ouest | 1 641 | 22,79 % | 100 % |
| Sud | 6 787 | 84,84 % | 100 % |
| Ouest | 7 168 | 85,33 % | 100 % |

## Interprétation

La collecte et la complétude temporelle sont validées. Cela ne signifie pas que CHIRPS est une mesure directe au sol : il s’agit d’une estimation maillée des précipitations. Les moyennes spatiales produites ensuite devront être interprétées comme des indicateurs régionaux et, si possible, comparées à des observations de stations indépendantes.

Les BBOX sont des zones techniques d’échantillonnage et non des frontières administratives. Elles contiennent des proportions terrestres différentes ; les comparaisons entre zones devront donc conserver cette information et éviter de présenter les zones comme ayant la même surface terrestre.

## Reproductibilité et provenance

Le manifeste complet est `year_1991_rnl_final.json`. Le contrôle qualité est `year_1991_quality_v02.json`. La version du code, les checksums, les URLs CHIRPS, les paramètres de découpage et les règles de reprise sont conservés dans le dépôt Git et dans le journal de session. Les données brutes n’ont pas été conservées après validation ; les rasters nettoyés sont archivés sur Drive.

## Décision scientifique

DS-011C peut être clôturée pour l’année 1991. L’analyse d’onset et les modèles de prévision restent des étapes ultérieures : elles ne doivent commencer qu’après construction des séries quotidiennes et définition indépendante des critères de validation.
