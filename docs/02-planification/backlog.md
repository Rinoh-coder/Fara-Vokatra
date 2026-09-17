# Backlog de pilotage scientifique — Fara-Vokatra

**Dernière mise à jour :** 2026-09-17

Le backlog est organisé par preuves à obtenir. Les statuts sont synchronisés avec [`feuille-de-route.md`](feuille-de-route.md), `CONTEXT.md` et le journal des sessions.

## Statuts

- **Terminé :** preuve et validation disponibles.
- **En cours :** tâche autorisée par le jalon courant.
- **Bloqué :** tâche définie mais dépendance ou incident non résolu.
- **À faire :** tâche non commencée.
- **Hors périmètre immédiat :** tâche volontairement différée.

## Jalon J0 — Gouvernance et reproductibilité

| ID | Tâche | Statut | Critère de sortie | Artefacts |
|---|---|---|---|---|
| GOV-001 | Créer le contexte vivant | Terminé | Reprise inter-agent possible | `CONTEXT.md` |
| GOV-002 | Structurer la documentation | Terminé | Index, cadrage, spécifications et rapports présents | `docs/` |
| GOV-003 | Historiser décisions et sessions | En cours permanent | Chaque étape clôturée possède une trace | `docs/04-tracabilite/` |
| GOV-004 | Maintenir la feuille de route | Terminé | Jalons, dépendances, risques et prochain objectif unique | `feuille-de-route.md` |

## Jalon J1 — Acquisition contrôlée et qualité

| ID | Tâche | Statut | Critère de sortie | Artefacts |
|---|---|---|---|---|
| DS-010 | Pipeline CHIRPS idempotent | Terminé | Téléchargement, recadrage, nettoyage, checksum et manifeste | `src/chirps_pipeline.py` |
| DS-010B | Pilote multi-zone isolé | Terminé | Un brut partagé, une sortie par zone, manifeste global | `src/multi_zone_download.py` |
| DS-011 | Validateur de manifeste | Terminé | Dates, zones, doublons, erreurs, fichiers et checksums contrôlés | `src/manifest_validator.py` |
| DS-011A | Collecte courte multi-zone valide | Terminé | Manifeste court sans anomalie et rapport qualité archivé | `docs/04-tracabilite/artefacts/ds011a-20240101-20240102/` |
| DS-011B | Préparer la collecte multi-années | Terminé | Période, volume, stockage Drive, reprise et critères d’arrêt documentés | `config/collecte_multi_annees.json`, `strategie-collecte-multi-annees.md` |
| DS-011C | Collecter et valider une première année complète | À faire | Année 1991 validée avant toute accélération | Manifeste, rapport qualité et archive Drive |
| DS-011D | Rapport multi-années de couverture | Bloqué | Couverture par zone et année sur période retenue | Rapport qualité et tables |

## Jalon J2 — Série quotidienne et onset

| ID | Tâche | Statut | Critère de sortie | Artefacts |
|---|---|---|---|---|
| DS-012 | Baselines d’onset | Terminé | Deux méthodes explicables et tests synthétiques | `src/onset.py` |
| DS-013 | Agrégation quotidienne | Terminé | Moyenne, couverture, valeurs extrêmes et dates manquantes | `src/chirps_series.py` |
| DS-014 | Analyse annuelle sans fuite | Terminé au niveau code | Climatologie indépendante, statuts et tests | `src/season_analysis.py` |
| DS-014A | Calcul multi-zone réel | Bloqué | Séries valides et résultats par zone/année | J1 validé |
| DS-015 | Rapport d’onset | À faire | Divergences, cas atypiques, incertitudes et limites | Rapport scientifique |

## Jalon J3 — Validation temporelle

| ID | Tâche | Statut | Critère de sortie | Artefacts |
|---|---|---|---|---|
| DS-020 | Protocole de backtesting | À faire | Partition temporelle, métriques et paramètres gelés | Protocole validé |
| DS-021 | Référence de validation | Bloqué | Stations, observations de semis ou source locale documentée | Registre des données |
| DS-022 | Évaluation hors échantillon | Bloqué | Erreurs par zone/année et incertitudes | Rapport de backtesting |

## Jalon J4 — Rendement exploratoire

| ID | Tâche | Statut | Critère de sortie | Artefacts |
|---|---|---|---|---|
| DS-030 | Auditer FAOSTAT/HDX | À faire, après J2 | Couverture, unités, cultures et niveau géographique vérifiés | Rapport de données |
| DS-031 | Auditer HarvestStat-Africa | À faire, après J2 | Licence, sources et jointures vérifiées | Rapport de données |
| DS-032 | Baseline rendement | Hors périmètre immédiat | Seulement si les audits sont favorables | Expérience versionnée |

## Jalon J5 — Décision et restitution

| ID | Tâche | Statut | Critère de sortie | Artefacts |
|---|---|---|---|---|
| DS-040 | Formaliser les contraintes agricoles | Hors périmètre immédiat | Hypothèses et consultation locale documentées | Registre des hypothèses |
| DS-041 | Prototyper l’optimisation | Hors périmètre immédiat | Scénarios et sensibilité | Rapport |
| DS-042 | Rapport non technique | En cours permanent | Résultats, incertitudes et limites compréhensibles | `docs/03-rapport-scientifique/` |

## Prochain objectif unique

**DS-011A est terminée et la préparation DS-011B est terminée.** Le prochain objectif unique devient DS-011C : collecter et valider l’année 1991 comme test complet avant toute accélération. Toute analyse d’onset réelle reste bloquée jusqu’à DS-011D.

## Définition générale de terminé

Une tâche est terminée si elle possède un résultat vérifiable, une documentation suffisante pour être reprise, des tests ou contrôles adaptés, une provenance et une entrée dans le journal des décisions ou des sessions lorsque son choix modifie la méthode. Le commit doit respecter les conventions Git du projet.
