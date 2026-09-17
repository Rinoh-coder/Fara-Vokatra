# Optimisation multi-cultures et sécurité alimentaire

## Résumé

L’optimisation multi-cultures consiste à choisir, dans un territoire et une saison, les surfaces ou volumes affectés à plusieurs cultures afin d’atteindre simultanément des objectifs parfois contradictoires : disponibilité alimentaire, revenu, résilience climatique, nutrition, eau et conservation des sols. Pour Madagascar, la priorité n’est pas de maximiser une seule production, mais de combiner cultures vivrières, légumineuses, tubercules et éventuellement cultures de rente sous des contraintes locales vérifiables. Les sources consultées établissent : le Programme alimentaire mondial (PAM) relie l’insécurité alimentaire à la faible diversification, à la dépendance à l’agriculture pluviale, aux faibles revenus et aux prix élevés [1]. L’IPC signale environ 1,63 million de personnes en phase IPC 3 ou plus entre septembre et décembre 2024 dans les zones analysées [2]. Ces chiffres décrivent une situation humanitaire ; ils ne prouvent pas qu’une optimisation mathématique, à elle seule, la résoudra.

## Ressources exploitables pour Madagascar

La première base de travail est **FAOSTAT**, accès gratuit aux statistiques agricoles et alimentaires par pays, culture et année [3]. Elle fournit des séries de production, rendements et sécurité alimentaire. Il faudra cependant vérifier l’année, l’unité et la couverture géographique de chaque série avant modélisation.

Le **calendrier agricole FAO de Madagascar**, disponible en français, est téléchargeable [4]. Sa fiche indique une publication en 2022, une mise à jour en 2023, une visibilité publique et une licence **CC BY-NC-SA 3.0**. Il est donc réutilisable avec attribution, sans usage commercial, et avec partage à l’identique. Il aide à fixer les fenêtres de semis, mais doit être complété par des calendriers régionaux.

Pour représenter le risque pluviométrique, **CHIRPS** offre une série quasi mondiale de 1981 à aujourd’hui, à 0,05 degré, construite à partir de satellites et de stations [5]. Les données sont placées dans le domaine public dans la mesure permise par le droit. Elles sont utiles pour calculer déficits de pluie, dates de début de saison et scénarios secs. CHIRPS v2 doit en outre être remplacé progressivement par v3, la production v2 devant s’arrêter après décembre 2026.

Enfin, le dépôt GitHub **Fruchtfolge/client** est un exemple de système d’aide à la décision pour l’optimisation des plans de culture [6]. Le dépôt est public, non archivé, possède 211 commits ; mais son API indique **aucune licence déclarée**. Il peut être étudié comme interface ou source d’inspiration, pas intégré ou redistribué sans clarification juridique. Son README le décrit aussi comme étant en bêta, avec 17 issues ouvertes.

## Méthodes pertinentes

Une première approche, robuste et explicable, est la **programmation linéaire**. Une variable représente la surface consacrée à une culture dans une zone et une saison. Les contraintes peuvent imposer la terre disponible, l’eau, la main-d’œuvre, les fenêtres du calendrier, les rotations et un minimum de denrées destinées à la consommation locale. La fonction objectif peut maximiser une marge sous réserve d’un panier nutritionnel minimal. Pour éviter qu’un prix volatil de la vanille domine le modèle, il faut séparer cultures alimentaires et cultures de rente, ou imposer des bornes de diversification.

La **programmation multi-objectifs** convient lorsque l’on veut comparer plusieurs compromis : coût ou revenu, kilocalories et protéines, consommation d’eau, émissions, risque climatique et stabilité interannuelle. L’étude ouverte de Hassna et al. formalise trois objectifs — coût, impact environnemental et risque — avec contraintes de demande, diversification, qualité et capacité [7]. Sa structure est transférable, mais ses données concernent l’approvisionnement du Qatar et trois légumes importés ; ce n’est donc pas une preuve empirique pour Madagascar. Une frontière de Pareto et une analyse de sensibilité sont préférables à un score unique.

Enfin, une approche **stochastique ou robuste** peut produire un plan pour plusieurs scénarios de pluie, rendement et prix. Les rendements observés localement doivent être croisés avec CHIRPS, enquêtes et essais agronomiques. L’étude ouverte sur la SAVA a utilisé des modèles linéaires généralisés et trouvé que la taille des terres et les rendements du riz et de la vanille étaient associés à une moindre insécurité alimentaire, tandis que la diversité déclarée des cultures n’était pas significative dans son échantillon [8]. Ce résultat recommande de tester, plutôt que supposer, l’effet de la diversification.

## Limites et risques

La diversification peut réduire le risque de production, mais elle peut aussi disperser la main-d’œuvre, réduire le rendement d’une culture prioritaire ou accroître les besoins en semences et stockage. Une optimisation fondée sur des moyennes nationales peut défavoriser les petits exploitants, les ménages dirigés par des femmes ou les zones enclavées. Les prix de rente, notamment la vanille, sont volatils ; les cyclones, sécheresses, ravageurs et pertes post-récolte rendent les rendements non stationnaires. Les données FAOSTAT et IPC ne sont pas toujours à la même échelle ni à la même période. Les résultats doivent être présentés comme scénarios. Il faut aussi vérifier les droits sur les jeux de données, le consentement pour les données de ménages et la licence avant de réutiliser du code GitHub.

## Prochaines vérifications

Il faut d’abord obtenir, auprès du ministère de l’Agriculture et des services régionaux, des rendements, coûts, calendriers et prix désagrégés par district. Ensuite, tester un prototype sur deux territoires contrastés, par exemple SAVA et Androy, avec riz, maïs, manioc, patate douce, haricot et une culture de rente. Les contraintes nutritionnelles devront utiliser des tables de composition et des besoins validés par les autorités nutritionnelles. Enfin, comparer plans optimisés et pratiques réelles avec une validation participative : agriculteurs, services déconcentrés, marchés, organisations de femmes et nutritionnistes.

## References

[1]: https://www.wfp.org/countries/madagascar "World Food Programme, Madagascar"

[2]: https://www.ipcinfo.org/ipc-country-analysis/en/?country=MDG "IPC, Madagascar country analysis"

[3]: https://www.fao.org/faostat/en/ "FAOSTAT, statistiques alimentaires et agricoles"

[4]: https://data-in-emergencies.fao.org/documents/7089db1e20d140d59f8db79afb0996ff "FAO, Madagascar - Agricultural calendar - FR"

[5]: https://www.chc.ucsb.edu/data/chirps "Climate Hazards Center, CHIRPS rainfall estimates"

[6]: https://github.com/fruchtfolge/client "Fruchtfolge, open-source crop planning optimisation client"

[7]: https://www.mdpi.com/2071-1050/16/11/4336 "Hassna et al., Multi-Objective Optimization for Food Availability under Economic and Environmental Risk Constraints"

[8]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8222503/ "Herrera et al., Food insecurity related to agricultural practices and household characteristics in rural communities of northeast Madagascar"

*Rapport rédigé par Manus AI ; les recommandations sont explicitement distinguées des faits rapportés par les sources.*
