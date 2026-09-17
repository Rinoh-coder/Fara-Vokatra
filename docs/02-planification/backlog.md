# Backlog initial

## Méthode

Le backlog est organisé par preuves à obtenir, et non par fonctionnalités isolées. Une tâche n’est terminée que lorsque son artefact, son test ou sa décision est traçable dans Git.

## Jalon 0 — Cadrage et reproductibilité

| ID | Tâche | Critère de sortie | Priorité |
|---|---|---|---|
| DS-001 | Finaliser l’inventaire des sources | Tableau avec couverture, résolution, licence, accès et limites | Haute |
| DS-002 | Définir la cible d’onset | Formule, paramètres, justification et test sur cas synthétiques | Haute |
| DS-003 | Écrire le protocole de validation | Partition temporelle et métriques approuvées avant entraînement | Haute |
| DS-004 | Préparer l’environnement | Installation reproductible et commande de vérification | Haute |

## Jalon 1 — MVP onset

| ID | Tâche | Critère de sortie | Priorité |
|---|---|---|---|
| DS-010 | Télécharger un échantillon ouvert | Script idempotent, manifeste de provenance et respect de licence | Haute |
| DS-011 | Contrôler qualité et valeurs manquantes | Rapport de couverture par région et année | Haute |
| DS-012 | Implémenter la baseline déterministe | Tests unitaires et sorties reproductibles | Haute |
| DS-013 | Construire les variables précoces | Variables définies sans accès au futur | Haute |
| DS-014 | Entraîner le modèle candidat | Validation temporelle et configuration versionnée | Moyenne |
| DS-015 | Produire le rapport de backtesting | Métriques, intervalles, erreurs et limites | Haute |

## Jalon 2 — Rendement exploratoire

| ID | Tâche | Critère de sortie | Priorité |
|---|---|---|---|
| DS-020 | Auditer les rendements par culture | Couverture régionale et temporelle documentée | Haute |
| DS-021 | Relier climat et rendement | Jeu analytique avec contrôle des jointures | Haute |
| DS-022 | Tester une baseline de rendement | Comparaison transparente, sans promesse opérationnelle | Moyenne |

## Jalon 3 — Décision et restitution

| ID | Tâche | Critère de sortie | Priorité |
|---|---|---|---|
| DS-030 | Formaliser les contraintes agricoles | Consultation agronomique et registre des hypothèses | Haute |
| DS-031 | Prototyper l’optimisation | Scénarios et analyse de sensibilité | Moyenne |
| DS-032 | Concevoir la restitution d’incertitude | Maquettes testées avec utilisateurs cibles | Moyenne |

## Définition générale de terminé

Une tâche est terminée si elle possède un résultat vérifiable, une documentation suffisante pour être reprise, des tests ou contrôles adaptés et une entrée dans le journal des décisions lorsque son choix modifie la méthode.

## État au 2026-09-17

DS-010 est implémentée pour CHIRPS v3 quotidien : téléchargement idempotent, découpage BBOX, nettoyage des valeurs invalides, SHA-256 et manifeste JSON. DS-011 est partiellement couverte par les contrôles de valeurs négatives, non finies et nodata ; l’agrégation quotidienne, le contrôle de couverture et l’analyse annuelle leave-one-year-out sont maintenant disponibles, mais le rapport géographique multi-années reste à produire.

Le pilote multi-zone est implémenté et testé. Un essai réel d’un jour a réussi pour les cinq zones ; l’essai de trois jours a été interrompu pendant le téléchargement du deuxième raster après détection d’un blocage réseau prolongé. Aucune conclusion scientifique multi-jours n’est tirée de cet essai.

Le contrôle qualité des manifestes est maintenant implémenté : complétude date/zone, doublons, erreurs, existence des fichiers et checksums SHA-256. L’analyse multi-années reste bloquée jusqu’à l’obtention d’un manifeste valide sur la période retenue.
