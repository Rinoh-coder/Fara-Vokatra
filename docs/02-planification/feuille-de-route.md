# Feuille de route scientifique — Fara-Vokatra

**Version :** 0.1

**Date de référence :** 2026-09-17

**Statut :** pilotage actif, MVP d’onset en cours

## 1. Règle de pilotage

Fara-Vokatra avance par **preuves vérifiables**, et non par accumulation de fonctionnalités. Une étape ne peut passer à l’étape suivante que si son artefact, sa validation, ses limites et sa trace historique sont présents dans le dépôt.

À chaque reprise, l’agent doit d’abord lire `CONTEXT.md`, cette feuille de route, le backlog et le dernier journal de session. Il doit ensuite choisir une seule tâche non bloquée du prochain jalon. Toute nouvelle décision méthodologique est ajoutée au journal des décisions avant la clôture de la tâche.

## 2. Vision des modules

| Module | Finalité | État | Dépendances principales |
|---|---|---|---|
| A — Pluie et onset | Estimer et comparer le début de la saison humide | En cours | CHIRPS, qualité des fichiers, définition agronomique |
| B — Rendement | Relier climat et rendement par culture | Non démarré | Audit FAOSTAT/HDX/HarvestStat, unités et granularité |
| C — Portefeuille agricole | Comparer des combinaisons de cultures | À cadrer | Rendements, contraintes agronomiques, fonction objectif |
| D — Régionalisation | Produire des résultats par zones justifiées | Exploratoire | Géométries, données locales, validation spatiale |
| E — Validation | Mesurer l’erreur et l’incertitude hors échantillon | Partiellement conçu | Périodes temporelles, observations de référence |
| F — Restitution | Rendre les résultats compréhensibles aux non-techniciens | Documentation en cours | Résultats validés, limites et tests utilisateurs |

Le module A reste prioritaire. Les modules B et C ne doivent pas être implémentés tant que leurs données et variables cibles ne sont pas auditées. Le module D ne doit pas transformer les boîtes techniques actuelles en régions officielles. Le module F peut documenter la méthode, mais ne doit pas présenter de recommandations opérationnelles avant validation.

## 3. État vérifié au 2026-09-17

Le dépôt contient un pipeline CHIRPS v3 quotidien, deux baselines d’onset, une agrégation quotidienne, une analyse annuelle avec climatologie leave-one-year-out, un pilote multi-zone et un validateur de manifestes. Vingt tests passent. Un essai réel a produit les cinq sorties de la première journée, puis a été interrompu pendant le téléchargement du deuxième raster ; aucune série multi-jours valide n’est encore disponible.

Cette distinction est essentielle : **le code est partiellement validé, mais les résultats scientifiques multi-zone ne sont pas encore produits**.

## 4. Jalons et dépendances

### J0 — Gouvernance et reproductibilité

**Objectif :** rendre chaque reprise traçable et empêcher la dispersion.

**État :** réalisé, à maintenir.

Les artefacts sont `CONTEXT.md`, cette feuille de route, `docs/02-planification/backlog.md`, les journaux et le registre des données. La sortie du jalon est la présence d’un état à jour, d’un prochain objectif unique et d’un dépôt propre.

### J1 — Acquisition contrôlée et qualité des données

**Objectif :** obtenir un petit ensemble multi-zone réellement complet avant toute analyse.

**État :** en cours, bloqué par la collecte réseau longue.

La prochaine tâche unique est DS-011A : télécharger une période courte et contrôlée, produire le manifeste, exécuter `manifest_validator.py`, conserver le rapport qualité et documenter le résultat. Les fichiers lourds peuvent être archivés dans Drive, mais le dépôt doit conserver les commandes, manifestes légers et checksums.

**Critères de sortie :** toutes les dates et zones attendues sont présentes ; aucun checksum ne diverge ; aucune erreur n’est enregistrée ; les chemins sont archivés ; le rapport JSON est lisible ; la période et la version CHIRPS sont documentées.

**Dépendances :** accès stable au serveur CHIRPS, espace de stockage, configuration des cinq boîtes.

**Risques :** téléchargement bloqué, fichier partiel, changement de disponibilité d’une URL, volume excessif, couverture spatiale insuffisante. La réponse prévue est une période plus courte, un téléchargement reprenable et l’arrêt explicite en cas d’incomplétude.

### J2 — Série quotidienne et exploration d’onset

**Objectif :** produire des séries par zone et comparer les baselines sur des années complètes.

**État :** code prêt, données non disponibles.

**Critères de sortie :** chaque zone possède une série vérifiée ; les années incomplètes sont signalées ; les dates d’onset, statuts et tailles de climatologie sont exportés ; les divergences sont décrites sans conclure à une supériorité automatique.

**Dépendances :** J1 validé.

### J3 — Protocole de validation temporelle

**Objectif :** évaluer les méthodes sans utiliser le futur et définir les métriques avant toute optimisation.

**État :** à formaliser.

**Critères de sortie :** protocole écrit, période d’apprentissage et période de test explicites, métriques définies, analyse des cas manquants et registre des paramètres gelé.

**Dépendances :** J2 et, idéalement, une référence indépendante pour la date observée.

### J4 — Validation externe et interprétation agronomique

**Objectif :** comparer les estimations à des observations locales ou à une source de référence documentée.

**État :** non démarré.

**Critères de sortie :** source de référence accessible ou limite clairement établie ; erreur par zone et année ; intervalle d’incertitude ; revue des cas divergents ; aucune recommandation sans qualification.

**Dépendances :** J3, données de stations ou calendrier local suffisamment précis.

### J5 — Module rendement exploratoire

**Objectif :** déterminer si les données de rendement permettent une analyse défendable.

**État :** non démarré.

**Critères de sortie :** couverture, unités, cultures, niveaux géographiques et révisions documentés ; jointures contrôlées ; baseline simple ; conclusion possible d’infaisabilité si les données ne conviennent pas.

**Dépendances :** audit des sources DATA-004 et DATA-005. Aucun modèle de rendement ne doit être entraîné avant cet audit.

### J6 — Restitution et décision

**Objectif :** présenter les résultats et leurs limites à un public non technique.

**État :** documentation progressive.

**Critères de sortie :** rapport scientifique lisible, glossaire, tableaux de qualité, incertitudes, limites, commandes de reproduction et distinction visuelle entre résultat observé, estimation et hypothèse.

**Dépendances :** J3 et J4 pour toute interprétation opérationnelle.

## 5. Problèmes connus et réponses

| Problème | Conséquence | Réponse obligatoire |
|---|---|---|
| Téléchargement CHIRPS lent ou bloqué | Série incomplète | Ne pas analyser ; conserver l’échec ; reprendre sur une période courte |
| Fichiers `.part` | Risque de faux raster valide | Suppression automatique et contrôle d’existence |
| BBOX technique | Résultat non administratif | Employer « boîte d’échantillonnage » et prévoir une géométrie justifiée |
| Climatologie sans année indépendante | Fuite d’information | Utiliser leave-one-year-out ou marquer le résultat non valide |
| Seuils non validés localement | Onset potentiellement non transférable | Les appeler baselines exploratoires et réaliser une sensibilité |
| CHIRPS satellite | Biais possible en relief et zones côtières | Comparer à stations ou signaler l’absence de validation |
| Rendements peu granulaires | Modèle trompeur | Auditer avant toute jointure ou prédiction |
| Résultats difficiles à lire | Mauvaise interprétation | Rapport en langage clair, glossaire et incertitudes |

## 6. Définition de terminé pour chaque tâche

Une tâche est terminée uniquement si :

1. le code ou document attendu existe ;
2. un test, une vérification ou une preuve externe est associé ;
3. les hypothèses et limites sont écrites ;
4. les paramètres et la provenance sont enregistrés ;
5. `CONTEXT.md`, le backlog et le journal de session sont synchronisés ;
6. `git diff --check`, les tests pertinents et `git status` propre sont vérifiés ;
7. un commit conventionnel est publié.

Une tâche bloquée est également historisée. Elle ne doit pas être marquée comme terminée.

## 7. Prochain objectif unique

**DS-011A — Obtenir et valider un manifeste multi-zone court.**

Aucune nouvelle fonctionnalité d’analyse ou d’optimisation ne doit être commencée avant la clôture ou le blocage documenté de cette tâche.

## Références

[1]: https://www.chc.ucsb.edu/data/chirps3 "Climate Hazards Center — CHIRPS v3"

[2]: https://climateknowledgeportal.worldbank.org/country/madagascar "World Bank Climate Change Knowledge Portal — Madagascar"

[3]: https://www.fao.org/giews/countrybrief/country.jsp?code=MDG "FAO GIEWS — Madagascar Country Brief"
