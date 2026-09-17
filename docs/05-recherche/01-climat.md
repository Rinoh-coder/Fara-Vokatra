# Données climatiques ouvertes utiles à Madagascar

## Résumé

Pour l’agriculture malgache, aucune source unique ne suffit. Le choix consiste à croiser une série pluviométrique à haute résolution (CHIRPS), une réanalyse multi-variable (ERA5-Land ou NASA POWER), puis des normales climatiques et projections (WorldClim et portail de la Banque mondiale). Ces produits sont gratuits ou accessibless, mais ce sont pour l’essentiel des estimations maillées, non des mesures locales. Les résultats doivent donc être comparés aux stations de la Direction Générale de la Météorologie (DGM), lorsque celles-ci sont disponibles, avant une décision opérationnelle.

## Ressources directement exploitables pour Madagascar

**CHIRPS** est la première option pour analyser pluie, sécheresse et calendrier agricole. Le produit combine climatologie, imagerie satellitaire à 0,05° et observations de stations, couvre 50°S–50°N et remonte de 1981 au quasi-présent. Il est disponible en fichiers et via Google Earth Engine. Le fournisseur indique que les droits ont été abandonnés autant que possible et que les données sont dans le domaine public [1]. En pratique, on peut calculer des cumuls pentadaires ou saisonniers, anomalies et séquences sèches pour chaque zone de culture. Limite importante : les pluies satellitaires sont des moyennes de maille et peuvent sous-estimer les extrêmes en relief ; la densité des pluviomètres influence aussi la qualité. Le site annonce en outre l’arrêt de la production CHIRPS v2 après décembre 2026 et recommande la transition vers v3 : une vérification de continuité est donc nécessaire [1].

**ERA5-Land** fournit une série cohérente de variables de surface depuis janvier 1950, à pas horaire, sur une grille distribuée de 0,1° (résolution native d’environ 9 km). Elle comprend notamment température, humidité, vent, évaporation et variables du sol, ce qui la rend utile pour bilans hydriques, stress thermique et indicateurs agroclimatiques [2]. L’accès programmatique passe par le Climate Data Store ; la licence affichée est **CC-BY** [2]. Fait à ne pas confondre avec une observation : ERA5-Land est une réanalyse issue d’un modèle forcé par ERA5. L’incertitude augmente en remontant dans le temps et dépend de la disponibilité des observations [2].

**NASA POWER** est pratique pour une exploitation ponctuelle ou un prototype agricole. Son API journalière retourne des séries prêtes à l’analyse en JSON, CSV, NetCDF ou ASCII ; les données quotidiennes existent de 1981 au quasi-présent, avec choix UTC ou temps solaire local [3]. Les paramètres météorologiques proviennent principalement de MERRA-2, puis GEOS-IT en quasi-temps réel ; la précipitation plus fine provient d’IMERG à 0,1° [4]. L’API limite une requête régionale à une variable et recommande de terminer les tendances environ 3,5 mois avant le temps réel pour éviter le mélange de produits IMERG [3] [4]. Recommandation : utiliser NASA POWER pour des points d’exploitation ou l’énergie solaire, mais préférer CHIRPS pour une cartographie pluviométrique fine.

**WorldClim 2.1** offre des rasters mensuels historiques 1970–2000 pour températures minimale, moyenne et maximale, précipitation, rayonnement, vent et pression de vapeur, ainsi que 19 variables bioclimatiques. Les résolutions vont d’environ 1 km à 10 minutes ; les téléchargements sont des archives ZIP de GeoTIFF [5]. C’est adapté à une cartographie de zonage agroécologique, moins à l’alerte saisonnière. La page consultée ne détaille pas la licence dans son contenu visible : il faut vérifier les conditions de redistribution.

Le **Climate Change Knowledge Portal (CCKP) de la Banque mondiale** est la ressource la plus immédiatement exploitable pour Madagascar à l’échelle nationale, des régions administratives et des bassins. Sa fiche Madagascar combine climat historique CRU/ERA5, tendances, risques et projections CMIP6. Elle indique une période historique 1995–2014 et des projections 2015–2100 selon les scénarios SSP ; les valeurs affichées sont des agrégats et des ensembles de modèles, non des prévisions certaines [6]. Le portail propose des fichiers NetCDF, un registre AWS et une API JSON/XLSX, avec variables comme température moyenne, précipitation [7]. Les recommandations d’usage et les conditions exactes de réutilisation doivent être relues dans les « Terms of Use » du portail avant redistribution.

## Méthodes pertinentes

Pour une étude agricole, télécharger CHIRPS et ERA5-Land sur la même emprise, harmoniser calendrier, unités et grille, puis calculer cumuls saisonniers, anomalies, séquences sèches et stress thermique. Comparer les séries à des stations DGM par biais moyen, corrélation, erreur absolue et reproduction des extrêmes. Pour les projections, comparer plusieurs modèles CMIP6 et au moins deux scénarios ; rapporter médiane et intervalle plutôt qu’une seule trajectoire. Un dépôt maintenu peut faciliter l’ingénierie : le client Python `ecmwf/cdsapi` donne un accès programmatique au CDS [8], tandis que `ropensci/chirps` et `ropensci/nasapower` proposent des clients R pour CHIRPS et POWER [9] [10].

## Limites et risques

Les mailles lissent les pluies, les reliefs et les microclimats de Madagascar. Les réanalyses et satellites peuvent présenter des ruptures, biais d’altitude. Une résolution de 1 km dans WorldClim n’implique pas une précision locale équivalente.un indicateur climatique ne prédit ni rendement ni décision paysanne sans sol, variété, pratiques, calendrier, ravageurs et accès à l’eau. Il faut éviter de transformer une projection probabiliste en promesse.

## Prochaines vérifications

Avant production : (1) obtenir auprès de la DGM les séries et métadonnées de stations disponibles ; (2) documenter la version CHIRPS retenue et tester la transition v2–v3 ; (3) vérifier licence, attribution et conditions d’API de chaque produit ; (4) contrôler unités, fuseaux horaires, valeurs manquantes et altitude ; (5) valider les indicateurs sur plusieurs régions, saisons et années extrêmes ; (6) conserver scripts, versions, paramètres de requête et empreintes des fichiers pour rendre l’analyse reproductible.

## References

[1]: https://www.chc.ucsb.edu/data/chirps "Climate Hazards Center — CHIRPS rainfall estimates"

[2]: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land "Copernicus Climate Data Store — ERA5-Land hourly data"

[3]: https://power.larc.nasa.gov/docs/services/api/temporal/daily/ "NASA POWER — Daily API documentation"

[4]: https://power.larc.nasa.gov/docs/methodology/data/sources/ "NASA POWER — Data sources and methodology"

[5]: https://www.worldclim.org/data/worldclim21.html "WorldClim 2.1 — Historical climate data"

[6]: https://climateknowledgeportal.worldbank.org/country/madagascar "World Bank CCKP — Madagascar country profile"

[7]: https://climateknowledgeportal.worldbank.org/download-data "World Bank CCKP — Download data and API structure"

[8]: https://github.com/ecmwf/cdsapi "ECMWF — cdsapi GitHub repository"

[9]: https://github.com/ropensci/chirps "rOpenSci — chirps R client GitHub repository"

[10]: https://github.com/ropensci/nasapower "rOpenSci — nasapower R client GitHub repository"

*Rapport préparé par Manus AI ; les recommandations sont explicitement distinguées des faits documentés par les sources.*
