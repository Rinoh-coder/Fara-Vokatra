# Registre de stockage et d’archivage — DS-011B

Ce registre sera rempli au fur et à mesure des années collectées. Il ne doit jamais être complété à partir d’une estimation : chaque ligne doit correspondre à un manifeste et à un rapport qualité validés.

| Année | Période | Zones | Enregistrements attendus | Manifeste local | Rapport qualité | Archive Drive | Checksum archive | Statut |
|---|---|---:|---:|---|---|---|---|---|
| 1991 | 1991-01-01 → 1991-12-31 | 5 | 1 825 | `/tmp/fara-vokatra-1991/.../year_1991_rnl_final.json` | `year_1991_quality.json`, `valid=true` | Drive `Fara-Vokatra/1991/fara-vokatra-1991-cleaned.zip` | `fara-vokatra-1991-archive-checksums.txt` | Validé |
| 1992 | 1992-01-01 → 1992-12-31 | 5 | 1 830 | À produire | À produire | À produire | À produire | À faire |
| 1993–2020 | annuel | 5 | À calculer par année | À produire | À produire | À produire | À produire | À faire |
| 2021–2024 | annuel | 5 | À calculer par année | À produire | À produire | À produire | À produire | À faire |

La période complète contient **12 419 jours** et **62 095 couples date/zone** pour cinq zones. Ce total inclut les neuf années bissextiles de 1992 à 2024.

## Règle de stockage

Les fichiers bruts globaux ne sont que des fichiers de travail locaux. Ils ne sont pas copiés sur Drive. Les sorties nettoyées sont regroupées dans un ZIP annuel pour réduire les appels API ; les manifestes, rapports qualité et checksums sont archivés séparément dans `Fara-Vokatra/<année>/`.

## Règle de reprise

Une année est reprise uniquement à partir de son manifeste. Un fichier `.part`, un fichier sans checksum ou un rapport `valid=false` ne compte pas comme acquis. Une reprise ne doit pas écraser un artefact validé sans produire une nouvelle version et une nouvelle trace de décision.

## Contrôle du quota

Le quota Drive doit être vérifié avant chaque groupe d’années. Si le quota restant devient inférieur à l’estimation de l’année suivante plus une marge de sécurité de 20 %, la collecte est arrêtée avant téléchargement.
