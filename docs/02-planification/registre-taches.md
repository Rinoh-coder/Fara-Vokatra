# Registre des tâches et des blocages

Ce registre complète le backlog. Il conserve la décision de démarrage, la preuve attendue et l’état concret de chaque tâche active. Il doit être mis à jour à l’ouverture et à la clôture d’une tâche.

| ID | Ouverture | Responsable | Dépendances | Preuve attendue | État au 2026-09-17 | Prochaine action |
|---|---|---|---|---|---|---|
| DS-011A | 2026-09-17 | Agent du projet | Pilote multi-zone, validateur | Manifeste court valide et rapport qualité | Terminé le 2026-09-17 | Préparer l’ouverture de DS-011B sans lancer de collecte non planifiée |
| DS-011B | Après DS-011A | Agent du projet | DS-011A, stockage stable | Couverture multi-années par zone | Terminé le 2026-09-17 — préparation | Période, volume, reprise et archive Drive documentés |
| DS-011C | Après DS-011B | Agent du projet | Configuration, quota Drive, pilote | Année 1991 complète et validée | Prochain objectif unique | Exécuter une seule année et archiver ses artefacts |
| DS-014A | Après DS-011D | Agent du projet | Séries quotidiennes complètes | Onsets par zone et année | Bloqué | Attendre la qualité des données |
| DS-020 | Après DS-014A | Agent du projet | Onsets réels et référence | Protocole de backtesting | Bloqué | Définir les observations cibles |
| DS-030 | Après audit J2 | Agent du projet | Sources de rendement | Rapport de couverture et unités | Différé | Ne pas ouvrir avant le jalon onset |

## Procédure à chaque session

L’agent doit vérifier `git status`, lire `CONTEXT.md`, lire la feuille de route, consulter ce registre et examiner le dernier commit. Il doit choisir une tâche ayant toutes ses dépendances satisfaites. Avant de coder, il écrit l’objectif et le critère de sortie dans le journal de session. Après le travail, il exécute les tests et contrôles pertinents, met à jour les documents synchronisés, crée un commit conventionnel et vérifie le statut Git.

Si une tâche échoue, l’échec est conservé. Le registre doit indiquer la cause, les artefacts produits, le risque introduit et la condition de reprise. Un échec ne devient pas « terminé » parce que le code existe.

## Règle de non-dispersion

Une tâche nouvelle ne peut être ajoutée au périmètre immédiat que si elle réduit un risque du jalon courant ou si elle est nécessaire à son critère de sortie. Les fonctionnalités de rendement, d’optimisation et de recommandation restent différées tant que le MVP d’onset n’a pas une donnée multi-zone validée.
