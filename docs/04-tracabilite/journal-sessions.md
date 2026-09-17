# Journal des sessions

## Session 2026-09-17 — Initialisation documentaire

### Objectif
Transformer le brief initial en base de projet scientifique traçable et préparer la recherche des ressources ouvertes.

### Actions réalisées

Le dépôt vide a été initialisé avec une structure documentaire. Le contexte vivant, le cadrage scientifique, le registre des hypothèses, la spécification du MVP, le backlog, le rapport scientifique, le README et les registres de provenance ont été créés.

### Décisions

Le périmètre prioritaire est le MVP d’onset. Les affirmations socio-économiques et agricoles du brief sont conservées comme hypothèses à vérifier. La recherche des ressources sera organisée par thèmes indépendants : climat, rendements, onset, prévision, optimisation et reproductibilité.

### Résultats

Aucun résultat empirique n’a été produit. La prochaine étape est de consolider les rapports de recherche, puis de sélectionner les données selon leur licence et leur capacité à soutenir une validation temporelle.

### Points ouverts

La définition exacte de l’onset, la source climatique principale, la disponibilité des rendements régionaux, la licence du code et la participation d’un référent agronomique restent à préciser.

## Session 2026-09-17 — Pipeline CHIRPS

### Actions réalisées

Une branche `feat/chirps-download-cleaning` a été créée. Le script `src/chirps_pipeline.py` télécharge CHIRPS v3 final/rnl, recadre une BBOX, transforme les valeurs invalides en nodata, calcule des empreintes SHA-256 et génère un manifeste JSON. Les rasters bruts et dérivés restent ignorés par Git.

### Validation

Trois tests unitaires passent. Un téléchargement CHIRPS réel sur une journée et une petite emprise a également été exécuté avec succès dans `/tmp`, sans ajouter de données volumineuses au dépôt.

### Points ouverts

La BBOX doit être remplacée par une géométrie officielle de la zone d’étude lorsque celle-ci sera définie. La couverture, les biais par région et la comparaison à des stations restent à évaluer.

## Session 2026-09-17 — Baselines d’onset

### Actions réalisées

Deux méthodes paramétrables ont été ajoutées dans `src/onset.py` : une règle à seuils avec contrôle prospectif des séquences sèches et une méthode d’anomalies cumulées. La documentation se trouve dans `docs/01-specifications/baseline-onset.md`.

### Validation

Les tests synthétiques couvrent le rejet d’un faux onset, l’absence de détection sans fenêtre valide, le minimum d’anomalie cumulée, les erreurs de date et les entrées invalides. La suite complète compte maintenant sept tests réussis.

### Limites

Les paramètres par défaut sont des valeurs de démonstration. Ils ne sont pas validés pour Madagascar et ne doivent pas être interprétés comme des seuils agronomiques opérationnels.

## Session 2026-09-17 — Série quotidienne CHIRPS

### Actions réalisées

Le module `src/chirps_series.py` agrège les GeoTIFF nettoyés en table CSV quotidienne. Il calcule la moyenne spatiale des pixels valides, la couverture, les valeurs min/max et vérifie les dates manquantes lorsqu’une période est fournie.

### Validation

Trois tests supplémentaires couvrent le calcul de moyenne, le rejet explicite d’une couverture insuffisante et l’écriture d’une série avec contrôle des dates. La suite complète compte dix tests réussis.

### Limites

La moyenne actuelle porte sur la BBOX découpée. Elle ne constitue pas une moyenne administrative ou une moyenne pondérée par les terres cultivées. Une géométrie de zone d’étude devra être ajoutée avant les analyses régionales.

## Session 2026-09-17 — Analyse annuelle d’onset

### Actions réalisées

Le module `src/season_analysis.py` lit la série quotidienne, vérifie les années complètes, applique les deux baselines d’onset et écrit une table annuelle. Pour la méthode Liebmann, la climatologie de chaque année est calculée avec les autres années disponibles selon une stratégie leave-one-year-out.

### Validation

Trois tests supplémentaires couvrent la climatologie indépendante, le signalement d’une année incomplète et la sortie CSV. La suite complète compte treize tests réussis.

### Limites

L’analyse est actuellement calendaire et exploratoire. Elle ne définit pas encore une saison agricole locale traversant deux années civiles et ne remplace pas une validation par stations ou par observations de semis.

## Session 2026-09-17 — Protocole multi-zone

### Actions réalisées

Les prochaines analyses sont cadrées par cinq boîtes d’échantillonnage techniques dans `config/zones_madagascar.json`. Le protocole distingue explicitement les sources établissant une variabilité climatique générale des choix de coordonnées qui restent exploratoires.

### Validation méthodologique

Le protocole impose les mêmes produit, période, seuil de couverture et paramètres d’onset entre zones. Il prévoit une comparaison stratifiée, une analyse des divergences supérieures à 30 jours comme outil de tri et une revue des années atypiques plutôt qu’une conclusion automatique.

### Limites

Les boîtes ne sont ni des frontières administratives ni des zones agricoles. Leur pertinence devra être contrôlée avec des données géographiques, des calendriers locaux et, si possible, des observations de stations.

## Session 2026-09-17 — Pilote multi-zone contrôlé

### Actions réalisées

Un orchestrateur multi-zone a été ajouté. Il partage un raster brut par date et écrit une sortie indépendante pour chaque zone, avec un manifeste global. Le premier essai réel sur trois jours a été lancé avec les cinq boîtes.

### Résultat et décision

Le premier jour a été téléchargé et découpé correctement pour les cinq zones. Le téléchargement du deuxième raster est resté bloqué avec un fichier partiel ; le job a été arrêté proprement afin de ne pas prolonger une collecte non nécessaire. Les fichiers partiels ont été supprimés. Ce résultat valide le chemin d’exécution du premier jour, mais ne constitue pas une validation multi-jours.

La fonction de téléchargement supprime désormais les fichiers `.part` lorsqu’une exception survient. La suite de tests compte seize tests réussis.

## Session 2026-09-17 — Validation des manifestes

### Actions réalisées

Le module `src/manifest_validator.py` vérifie la complétude des couples date/zone, les doublons, les dates inattendues, les erreurs du manifeste, l’existence des fichiers et les checksums SHA-256. Il produit un rapport JSON exploitable avant l’analyse scientifique.

### Validation

Les tests couvrent un manifeste valide, les enregistrements manquants et dupliqués, un checksum incorrect et l’écriture du rapport. La suite complète compte vingt tests réussis.

### Décision

Un manifeste invalide doit être conservé comme trace de qualité, mais ne doit pas alimenter les dates d’onset. Les anomalies ne sont pas imputées silencieusement.

## Session 2026-09-17 — Consolidation du pilotage

### Audit effectué

L’état Git était propre et les modules présents correspondaient au périmètre du MVP : téléchargement CHIRPS, agrégation, onset, analyse annuelle, pilote multi-zone et validation des manifestes. Le principal écart concernait la planification : le backlog listait les tâches, mais ne rendait pas assez explicites les dépendances, les blocages, les modules différés et le prochain objectif unique.

### Actions réalisées

Une feuille de route versionnée décrit les modules A à F, les jalons J0 à J6, les risques, les critères de sortie et les règles de clôture. Le backlog a été réécrit comme tableau de pilotage. Un registre des tâches conserve les dépendances et les conditions de reprise. L’index documentaire, le contexte et le journal des décisions ont été synchronisés.

### Décision de périmètre

La seule tâche autorisée au prochain cycle est DS-011A : obtenir un manifeste multi-zone court et valide. Les séries multi-années, le backtesting, les rendements et l’optimisation restent bloqués jusqu’à la preuve de qualité des données.

## Session 2026-09-17 — Clôture DS-011A

### Résultat

Les artefacts déjà disponibles ont été examinés. Les journées du 1er et du 2 janvier 2024 sont complètes pour les cinq zones. Le 3 janvier reste un fichier `.part` vide et a été exclu. Un manifeste de dix couples date/zone a été construit, puis contrôlé avec vérification des fichiers et des checksums.

### Validation

Le rapport qualité indique `valid=true`, 10 enregistrements attendus, 10 observés, aucun doublon, aucune date manquante, aucune erreur, aucun fichier manquant et aucun checksum divergent. Le manifeste et le rapport qualité sont archivés dans `docs/04-tracabilite/artefacts/ds011a-20240101-20240102/`. Le rapport scientifique lisible se trouve dans `docs/03-rapport-scientifique/rapport-ds011a.md`.

### Décision

DS-011A est terminée. DS-011B devient le prochain objectif : préparer une collecte multi-années avant son exécution. Les deux jours validés ne doivent pas être utilisés pour calculer une climatologie ou un onset.
