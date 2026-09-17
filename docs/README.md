# Documentation Fara-Vokatra

## Reprendre le projet

Commencer par [`../CONTEXT.md`](../CONTEXT.md), puis lire la [`feuille de route`](02-planification/feuille-de-route.md), le [`registre des tâches`](02-planification/registre-taches.md), le [`cadrage scientifique`](00-cadrage/cadrage-scientifique.md), la [`spécification du MVP`](01-specifications/specification-mvp.md) et le [`backlog`](02-planification/backlog.md). Une seule tâche du prochain jalon doit être active à la fois.

## Comprendre le projet

Le [`brief initial`](00-cadrage/brief-initial.md) décrit la vision fonctionnelle. Le [`registre des hypothèses`](00-cadrage/registre-hypotheses.md) indique ce qui doit encore être prouvé. Le [`rapport scientifique`](03-rapport-scientifique/rapport-projet.md) rassemble progressivement méthode, résultats et limites.

## Rechercher et décider

Les rapports de ressources ouvertes sont dans [`05-recherche`](05-recherche/). Les décisions et sessions sont conservées dans [`04-tracabilite`](04-tracabilite/), avec le [`registre des données`](04-tracabilite/registre-donnees.md), le [`registre de stockage`](04-tracabilite/registre-stockage.md) et le [`modèle de fiche d’expérience`](04-tracabilite/fiche-experience.md). La feuille de route décrit les modules, jalons, dépendances, risques et critères de sortie ; le registre des tâches conserve les blocages et les conditions de reprise.

La préparation de la collecte historique est documentée dans la [`stratégie multi-années`](02-planification/strategie-collecte-multi-annees.md) et sa configuration versionnée dans [`config/collecte_multi_annees.json`](../config/collecte_multi_annees.json).

Le contrat de production des séries quotidiennes est dans [`protocole-series-historiques.md`](01-specifications/protocole-series-historiques.md). Le rapport qualité annuel automatisé est produit par `src/annual_quality.py`, et l’archivage est préparé par `scripts/archive_year_to_drive.sh` après validation du manifeste.

## Règle de qualité

Une affirmation empirique doit être accompagnée d’une source ou d’un artefact reproductible. Une recommandation doit indiquer son incertitude et ses limites. Une métrique doit être associée à son protocole de validation.
