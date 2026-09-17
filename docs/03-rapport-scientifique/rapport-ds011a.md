# Rapport DS-011A — Échantillon CHIRPS multi-zone contrôlé

## Conclusion

Un échantillon de deux jours, du **1er au 2 janvier 2024**, a été obtenu pour les cinq boîtes d’échantillonnage techniques. Le manifeste contient **10 couples date/zone attendus et 10 observés**. Le validateur a confirmé l’absence de doublons, de dates manquantes, d’erreurs enregistrées, de fichiers manquants et de divergences de checksum.

Cette réussite valide le chemin d’acquisition et de contrôle pour un petit échantillon. Elle ne constitue pas encore une série climatique suffisante pour analyser l’onset ou comparer des zones sur plusieurs années.

## Données et provenance

Le produit utilisé est `CHIRPS v3 daily final/rnl`. Les fichiers bruts et nettoyés sont conservés hors Git dans `/tmp/fara-vokatra-multizone-test/`. Le manifeste et le rapport qualité légers sont archivés dans [`docs/04-tracabilite/artefacts/ds011a-20240101-20240102/`](../04-tracabilite/artefacts/ds011a-20240101-20240102/).

Le checksum SHA-256 du manifeste archivé est `9b852775eb6ff0f6fc42b334e506160013bba3a42b78336ac29f3c1d8f75bc0b`. Le checksum du rapport qualité est `52b94c249bdc8465187c8b96ae63f1a44d80f7b1d822dfc9e0678316c1fe15a1`.

## Contrôles effectués

Le rapport JSON confirme :

| Contrôle | Résultat |
|---|---:|
| Enregistrements attendus | 10 |
| Enregistrements observés | 10 |
| Zones | 5 |
| Dates | 2 |
| Doublons | 0 |
| Dates ou zones inattendues | 0 |
| Erreurs de traitement | 0 |
| Fichiers manquants | 0 |
| Checksums divergents | 0 |

## Incident associé

La collecte initialement lancée sur trois jours a produit un fichier partiel pour le 3 janvier. Ce jour a été exclu du manifeste DS-011A. Cette exclusion est obligatoire : une journée partielle ne doit pas être transformée en observation valide.

## Interprétation scientifique

L’échantillon permet de vérifier l’architecture technique, les chemins séparés par zone, le calcul des checksums et le validateur. Deux jours ne permettent pas d’estimer une climatologie, une saison des pluies, une date d’onset ou une différence régionale. Aucun résultat agronomique n’est donc déduit de cet échantillon.

## Prochaine condition

La tâche DS-011A peut être considérée comme terminée. La tâche DS-011B reste bloquée : il faut d’abord décider d’une stratégie de téléchargement multi-années robuste, archiver les données lourdes sur Drive si nécessaire et définir une période suffisante avant de produire des séries d’onset.
