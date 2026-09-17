# Bonnes pratiques open science et reproductibilité en data science agricole

## Résumé

La **science ouverte** vise à rendre les connaissances et, lorsque c’est approprié, les processus de production scientifique accessibles, inclusifs et réutilisables. L’UNESCO en fait un cadre international qui associe transparence, intégrité, équité, collaboration et reproductibilité [1]. En data science agricole, la reproductibilité signifie qu’une autre équipe peut relancer l’analyse avec les mêmes données, code, dépendances et paramètres, puis comprendre les écarts éventuels. Le Turing Way retient une définition opérationnelle : les données et le code doivent être disponibles pour relancer complètement l’analyse [2]. Pour un projet au Madagascar, la priorité est donc de construire une chaîne auditable : données brutes immuables, métadonnées, scripts versionnés, environnement figé, tests, sorties horodatées et citation des versions.

## Ressources directement exploitables pour Madagascar

**FAOSTAT** est la première source à tester pour les séries nationales de cultures, élevage et autres secteurs agricoles. La FAO annonce un accès gratuit à des statistiques alimentaires et agricoles couvrant plus de 245 pays et territoires [3]. Il faut toutefois documenter la date d’extraction, l’identifiant du jeu et les transformations, car l’interface est dynamique et les conditions de réutilisation doivent être vérifiées dans les métadonnées ou les conditions FAO avant redistribution.

Pour des analyses infranationales, le dépôt maintenu **HarvestStat-Africa** fournit des statistiques harmonisées de production végétale. Sa version indiquée dans le dépôt couvre Madagascar au niveau administratif 2 et propose des fichiers CSV, Parquet et GeoPackage [4]. Le dépôt décrit les sources FEWS NET, FAOSTAT et des agences nationales, les variables de surface, production, rendement et un indicateur de contrôle qualité. Sa licence MIT est explicitement indiquée pour les données du dépôt. Limite importante : les variables de calendrier agricole ne représentent pas nécessairement la phénologie réelle ; elles servent notamment à distinguer des saisons et années.

Le modèle de projet du **Turing Way** est directement réutilisable : séparation entre données brutes et traitées, code source, notebooks, modèles, rapports, documentation, gestion de projet, fichier de citation et connexion à Zenodo [5]. Le code est sous MIT et la documentation sous CC BY 4.0. Quarto fournit une alternative ouverte pour générer des rapports avec code Python, R ou JavaScript intégré, citations et sorties HTML, PDF ou autres [6]. GitHub documente enfin l’archivage d’un dépôt public dans Zenodo : chaque version GitHub peut recevoir un DOI, à condition d’ajouter une licence [7].

## Méthodes pertinentes

La méthode recommandée est un dépôt Git avec une arborescence stable : `data/raw` pour les téléchargements originaux, `data/processed` pour les données dérivées, `src` pour les scripts, `notebooks` pour l’exploration, `reports` pour les résultats et `README` pour le protocole. Un manifeste doit enregistrer l’URL, la date, le checksum, la licence, la granularité géographique, les unités et les changements appliqués. Les données doivent suivre les principes **FAIR** : identifiants persistants, métadonnées riches, indexation, formats interopérables, provenance et licence explicite [8]. FAIR ne signifie pas automatiquement « ouvert » : l’accessibilité peut nécessiter une autorisation.

Il faut séparer l’exploration de l’analyse confirmatoire, écrire les transformations comme des fonctions testables et valider les unités avant agrégation. Les tests doivent contrôler les valeurs impossibles, les doublons, les unités hectares/tonnes, les jointures administratives et la conservation des totaux. Un fichier `environment.yml`, `pyproject.toml` ou verrou équivalent doit figer les dépendances ; un conteneur peut réduire les différences de système. Les notebooks devraient être exécutables de bout en bout et leurs sorties volumineuses retirées du contrôle de version. Une version publiée doit être archivée avec DOI et citée via `CITATION.cff`.

## Limites et risques

La reproductibilité computationnelle ne garantit ni la qualité des observations ni la validité causale. Les séries agricoles peuvent changer, être révisées ou mélanger des définitions nationales. Les données ouvertes peuvent exposer des ménages, exploitations ou savoirs sensibles ; l’UNESCO recommande une ouverture « aussi large que possible », avec restrictions pour la vie privée, les droits, les espèces menacées ou les savoirs autochtones [1]. Il faut donc anonymiser, agréger et appliquer un contrôle d’accès lorsque nécessaire, sans publier de coordonnées individuelles.

Les contraintes malgaches incluent la connectivité, le coût du stockage et la disponibilité des compétences. Un dépôt GitHub exige aussi un accès Internet et une gouvernance durable. Un DOI fige une version, mais ne corrige pas une source amont erronée. Enfin, MIT, CC BY et les conditions de la FAO ne sont pas interchangeables : la licence de chaque composant et les obligations d’attribution doivent être conservées séparément.

## Prochaines vérifications

Avant diffusion, vérifier les conditions exactes de FAOSTAT et de FEWS NET, la version et le changelog de HarvestStat-Africa, la complétude de la couverture administrative malgache et la concordance des unités avec les données nationales. Exécuter le pipeline sur une machine neuve, comparer les checksums et résultats attendus, puis faire relire le dictionnaire de données par un agronome malgache. Tester enfin une publication Zenodo, la présence des licences, le DOI, le fichier de citation et un mécanisme de retrait ou de correction des données sensibles.

## References

[1]: https://www.unesco.org/en/open-science/about "UNESCO Recommendation on Open Science"
[2]: https://book.the-turing-way.org/reproducible-research/reproducible-research/ "The Turing Way: Guide for Reproducible Research"
[3]: https://www.fao.org/faostat/en/ "FAOSTAT: Food and agriculture data"
[4]: https://github.com/HarvestStat/HarvestStat-Africa "HarvestStat-Africa: Open-Access Harmonized Subnational Crop Statistics"
[5]: https://github.com/the-turing-way/reproducible-project-template "The Turing Way reproducible project template"
[6]: https://quarto.org/about.html "About Quarto: Open source tools for scientific and technical publishing"
[7]: https://docs.github.com/repositories/archiving-a-github-repository/referencing-and-citing-content "GitHub documentation: Referencing and citing content"
[8]: https://www.go-fair.org/fair-principles/ "GO FAIR: FAIR Principles"

[1] [2] [3] [4] [5] [6] [7] [8]

> **Note de lecture.** Les éléments décrivant une couverture, une licence ou une fonctionnalité sont des faits rapportés par les pages sources consultées. Les choix d’arborescence, de tests et de gouvernance sont des recommandations pratiques adaptées à un projet agricole malgache.
