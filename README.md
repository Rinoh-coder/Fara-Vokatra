# Fara-Vokatra

**Système open source d’aide à la décision agricole pour Madagascar — projet scientifique en construction.**

## Statut

Le dépôt est au stade de cadrage et de revue des ressources. Le premier objectif est un MVP scientifique consacré à la détection et à la prévision précoce de l’onset des pluies. Aucun résultat ne doit encore être interprété comme une recommandation agricole opérationnelle.

## Principes

Le projet privilégie les données ouvertes, la reproductibilité, la validation hors échantillon et l’expression explicite de l’incertitude. Les hypothèses, décisions, sources et limites sont conservées dans `docs/`.

## Organisation

- `CONTEXT.md` : contexte vivant pour reprendre le projet avec un autre agent.
- `docs/00-cadrage/` : brief, cadrage scientifique et hypothèses à vérifier.
- `docs/01-specifications/` : spécification du MVP.
- `docs/02-planification/` : backlog et jalons.
- `docs/03-rapport-scientifique/` : rapport évolutif.
- `docs/04-tracabilite/` : décisions, données et provenance.
- `docs/05-recherche/` : revue des ressources ouvertes et méthodes.
- `src/`, `tests/`, `notebooks/`, `reports/` : code, tests, exploration et sorties.

## Workflow recommandé

1. Lire `CONTEXT.md` et le backlog.
2. Vérifier les hypothèses et l’inventaire de données avant de coder.
3. Développer une baseline testée avant tout modèle complexe.
4. Utiliser une validation temporelle et journaliser les paramètres.
5. Mettre à jour le rapport, le registre de provenance et le journal des décisions.
6. Faire relire les interprétations par une personne compétente en agronomie ou climatologie lorsque le projet atteint une phase de recommandation.

## Licence

La licence du code sera choisie et ajoutée après confirmation des contraintes de compatibilité des données et des contributions. Les licences des données restent indépendantes de celle du code.

## Contribution

Les contributions doivent expliquer le problème traité, la méthode, les données utilisées, les tests ajoutés et les limites connues. Une amélioration de métrique sans protocole de validation reproductible ne suffit pas à établir une amélioration scientifique.
