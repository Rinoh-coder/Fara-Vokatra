# Méthodes de prévision saisonnière et validation temporelle

## Résumé

La prévision saisonnière agricole vise à estimer, plusieurs semaines ou mois à l’avance, pluie, température, début de saison, sécheresse ou rendement. Les systèmes produisent surtout des **distributions de scénarios**, et non une trajectoire certaine. Le service saisonnier de l’ECMWF couvre jusqu’à sept mois, avec un ensemble de 51 membres, et publie des anomalies ainsi que des probabilités de conditions inférieures, normales ou supérieures à la climatologie [1]. Pour Madagascar, une chaîne réaliste combine données historiques ouvertes, prévisions multi-modèles, variables agroclimatiques locales et validation strictement chronologique. Il faut comparer toute méthode complexe à des références simples, avec incertitude et performance par horizon et région.

## Ressources directement exploitables pour Madagascar

**CHIRPS** fournit une série de précipitations quasi mondiale de 1981 à aujourd’hui, sur une grille de 0,05° entre 50°S et 50°N. Elle combine observations satellitaires et stations, et convient à l’analyse des déficits pluviométriques et au suivi saisonnier de la sécheresse [2]. Le site indique que les données sont dans le domaine public, dans la mesure permise par la loi. Limite factuelle : les estimations satellitaires peuvent sous-estimer les pluies extrêmes en terrain complexe et les zones peu instrumentées restent incertaines. CHIRPS v3 est désormais disponible ; la production v2 doit s’arrêter après décembre 2026. Il faut donc documenter la version utilisée.

Le **Climate Change Knowledge Portal de la Banque mondiale** expose pour Madagascar des agrégations nationales et infranationales d’ERA5, de 1950 à aujourd’hui, avec une période climatologique 1991–2020 et une résolution de 0,25° [3]. Il permet de construire normales, anomalies et indicateurs régionaux. Le portail recommande de croiser plusieurs jeux pour les précipitations. La licence de réutilisation du portail et des agrégations doit être confirmée avant redistribution d’un produit dérivé.

Le jeu **Copernicus C3S Seasonal Forecast** fournit des prévisions mensuelles mondiales à 1° x 1°, des rétrospectives (hindcasts) 1993–2016 et des prévisions récentes depuis 2017 [4]. Les variables incluent précipitations, température, ruissellement, évaporation et rayonnement. La licence indiquée est CC-BY, avec une licence additionnelle possible pour des contributions non européennes. Les hindcasts sont essentiels pour tester un système sans utiliser le futur. L’accès nécessite un compte CDS et l’API doit être vérifiée au moment de l’implémentation.

Enfin, l’article de Hansen montre que l’intégration d’une prévision climatique probabiliste avec un modèle de culture peut produire des prévisions de rendement plus utiles, mais souligne un rôle limité et la nécessité d’une évaluation prudente [5]. L’article est accessible gratuitement via PubMed Central ; la licence exacte de l’éditeur doit être vérifiée pour toute republication.

## Méthodes pertinentes

Une première famille est la **prévision dynamique** : modèles couplés atmosphère–océan–surface, comme SEAS5. Elle fournit des scénarios. Une deuxième est la **prévision statistique ou d’apprentissage automatique**, à partir des retards de pluie et température, de l’ENSO, de la date de démarrage des pluies et d’indices spatiaux. Pour un premier prototype malgache, il est raisonnable de comparer climatologie, persistance, régression réguliarisée, forêt aléatoire ou gradient boosting. Une troisième option est l’**hybride** : correction de biais et calibration locale des sorties C3S, puis agrégation avec CHIRPS/ERA5. Cette recommandation doit être testée, car la résolution de 1° peut lisser des contrastes importants entre hauts plateaux, côte et Sud aride.

La validation doit respecter l’ordre temporel. La documentation scikit-learn indique que K-fold et ShuffleSplit supposent des observations indépendantes ; ils peuvent donc mélanger passé et futur et sous-estimer l’erreur [6]. `TimeSeriesSplit` crée des entraînements cumulant les périodes antérieures, exige des observations régulièrement espacées et offre `test_size`, `max_train_size` et `gap` pour représenter respectivement la fenêtre d’évaluation, une fenêtre glissante et un délai séparant entraînement et test [7]. La validation « rolling forecasting origin » déplace l’origine et moyenne les erreurs sur plusieurs dates ; elle s’adapte aux horizons multiples [8].

Pour l’agriculture, il faut simuler l’usage réel : par exemple, prévoir le cumul octobre–décembre depuis l’information disponible en septembre, sans utiliser de données publiées ultérieurement. Il faut calculer MAE ou RMSE pour les quantités, mais aussi la calibration probabiliste, le score de Brier pour des événements binaires et la couverture des intervalles. Les scores doivent être stratifiés par horizon, région et type de saison, avec une référence climatologique et un modèle naïf.

## Limites et risques

La prévisibilité locale est limitée par le chaos atmosphérique, les biais et la faible densité des stations. Une performance nationale peut masquer un échec communal. CHIRPS et ERA5 ne sont pas des observations parfaites ; versions et capteurs peuvent créer des ruptures. Le risque méthodologique principal est la fuite d’information : normalisation, imputation, sélection de variables ou calibration calculée avec tout le jeu de données avant les folds. Les rendements dépendent aussi des semences, ravageurs, prix et pratiques, qui ne sont pas déduits d’une prévision de pluie. Une probabilité de pluie supérieure à la normale ne constitue donc pas une recommandation agronomique automatique.

## Prochaines vérifications

Vérifier auprès de la Direction Générale de la Météorologie et des services agricoles les calendriers culturaux, les stations disponibles et les seuils de décision. Télécharger un petit historique CHIRPS, ERA5 et C3S sur deux ou trois régions contrastées, puis contrôler unités, fuseaux temporels, valeurs manquantes, dates de publication et versions. Construire un backtest par origine glissante sur au moins dix saisons, avec une saison finale totalement retenue pour l’évaluation. Comparer une prévision déterministe à une prévision probabiliste calibrée, puis tester sa valeur décisionnelle avec des agronomes avant toute diffusion.

## References

[1]: https://www.ecmwf.int/en/forecasts/documentation-and-support/seasonal "ECMWF, Seasonal forecasts"

[2]: https://www.chc.ucsb.edu/data/chirps "Climate Hazards Center, CHIRPS: Rainfall Estimates from Rain Gauge and Satellite Observations"

[3]: https://climateknowledgeportal.worldbank.org/country/madagascar/era5-historical "World Bank Climate Change Knowledge Portal, Madagascar ERA5 historical climate"

[4]: https://cds.climate.copernicus.eu/datasets/seasonal-monthly-single-levels "Copernicus Climate Data Store, Seasonal forecast monthly statistics on single levels"

[5]: https://pmc.ncbi.nlm.nih.gov/articles/PMC1569571/ "James W. Hansen, Integrating seasonal climate prediction and agricultural models for insights into agricultural practice"

[6]: https://scikit-learn.org/stable/modules/cross_validation.html "scikit-learn User Guide, Cross-validation of time series data"

[7]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html "scikit-learn API, TimeSeriesSplit"

[8]: https://otexts.com/fpp3/tscv.html "Forecasting: Principles and Practice, Time series cross-validation"

Le dépôt scikit-learn associé est maintenu sur GitHub sous licence BSD-3-Clause : https://github.com/scikit-learn/scikit-learn .
