# Contexte vivant — Fara-Vokatra

> Document de reprise inter-agent. Toute décision importante doit être ajoutée avec une date, une justification et une référence vers l’artefact concerné.

## Identité

Fara-Vokatra (« le fruit de la récolte ») est un projet open source d’aide à la décision agricole pour Madagascar. Il vise à relier des données climatiques et agronomiques ouvertes à des recommandations régionales compréhensibles : **quand planter, quoi planter et où agir avec quel niveau de risque**.

## Intention scientifique

Le projet doit démontrer des compétences de data science par une démarche reproductible : formulation d’hypothèses, définition des variables, séparation temporelle entraînement/test, baselines explicites, validation hors échantillon, analyse d’incertitude, documentation des limites et reproductibilité des résultats.

## État au 2026-09-17

Le dépôt GitHub était vide à l’initialisation. Le cahier des charges est conservé dans `docs/00-cadrage/brief-initial.md`. La structure documentaire, le cadrage scientifique, le MVP, le backlog et six rapports de recherche ont été ajoutés. Le pipeline initial de téléchargement et nettoyage CHIRPS v3 est implémenté sur la branche `feat/chirps-download-cleaning`.

La recherche recommande de commencer par **CHIRPS** pour la pluie, complété par **ERA5-Land** ou NASA POWER pour les variables météorologiques. CHIRPS est pertinent pour l’onset mais la transition v2–v3 doit être contrôlée avant une série longue. Pour les rendements, FAOSTAT/HDX et HarvestStat-Africa sont des pistes initiales, mais la couverture et les définitions régionales doivent être auditées. Deux baselines d’onset sont maintenant implémentées dans `src/onset.py` : règle à seuils avec rejet de faux onset et anomalies cumulées de type Liebmann. La validation doit être chronologique, par rolling origin ou `TimeSeriesSplit`.

## Périmètre fonctionnel initial

Les modules envisagés sont : A — climat ; B — rendement ; C — portefeuille agricole ; D — régionalisation ; E — validation ; F — restitution. Le premier jalon reste limité à un **MVP scientifique du module A**, accompagné d’une preuve de faisabilité exploratoire du module B. Les modules C, D et F ne doivent pas masquer les dépendances de données et de validation.

## Décisions prises

| Date | Décision | Justification | Artefact |
|---|---|---|---|
| 2026-09-17 | Commencer par un MVP d’onset | Question testable, baseline vérifiable et validation temporelle claire | `docs/01-specifications/specification-mvp.md` |
| 2026-09-17 | Traiter les affirmations du brief comme des hypothèses à vérifier | Les chiffres et causalités nécessitent des sources primaires | `docs/00-cadrage/registre-hypotheses.md` |
| 2026-09-17 | Comparer au moins deux familles de méthodes d’onset | Les seuils sont interprétables mais sensibles aux paramètres ; Liebmann apporte un contraste méthodologique | `docs/05-recherche/03-onset.md` |
| 2026-09-17 | Utiliser une validation temporelle sans mélange passé/futur | Les validations aléatoires peuvent sous-estimer l’erreur en séries temporelles | `docs/05-recherche/04-prevision.md` |
| 2026-09-17 | Ne pas redistribuer une donnée ou un code sans vérifier sa licence | Les licences CHIRPS, FAOSTAT, calendrier FAO et dépôts GitHub diffèrent | `docs/04-tracabilite/registre-donnees.md` |

## Ressources de recherche

Les rapports thématiques se trouvent dans `docs/05-recherche/`. Les sources prioritaires sont CHIRPS, ERA5-Land, NASA POWER, WorldClim, le portail CCKP de la Banque mondiale, FAOSTAT, HDX, INSTAT, HarvestStat-Africa, FAO/GIEWS, ECMWF/C3S et scikit-learn. Les rapports contiennent les URLs, les licences ou points à vérifier, les limites et les prochaines actions.

## Prochaines actions immédiates

1. Remplacer la BBOX technique par la géométrie officielle de la zone d’étude.
2. Télécharger un petit échantillon CHIRPS sur plusieurs zones contrastées, sans commiter les fichiers bruts.
3. Relier les deux baselines d’onset à une série CHIRPS multi-années.
4. Écrire le protocole de backtesting et figer les périodes d’entraînement et de test.
5. Vérifier la couverture régionale et les unités des rendements FAOSTAT/HDX ou HarvestStat-Africa.
6. Demander une revue agronomique locale avant toute interprétation opérationnelle.

## Risques ouverts

La disponibilité des stations DGM, la continuité CHIRPS v2–v3, la représentativité des mailles en relief, la faible granularité des rendements et la définition locale de la période de soudure restent non résolues. La résolution spatiale d’un produit ne doit jamais être présentée comme une précision locale garantie.

## Règle de mise à jour

À chaque session, mettre à jour l’état, les décisions, les hypothèses modifiées, les artefacts produits et les risques ouverts. Ne jamais supprimer une décision historique ; la corriger par une nouvelle entrée datée.
