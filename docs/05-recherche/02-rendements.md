# Données de rendements agricoles et statistiques ouvertes

## Résumé

Pour Madagascar, la combinaison la plus directement exploitable est constituée des séries FAOSTAT, de leur miroir Madagascar sur Humanitarian Data Exchange (HDX), des indicateurs de la Banque mondiale et des publications de l’Institut national de la statistique (INSTAT). Ces sources fournissent surtout des statistiques annuelles nationales ou infranationales, alors que les données satellitaires ouvertes apportent une couverture spatiale et temporelle complémentaire. **Recommandation :** établir d’abord une série de référence documentée avec FAOSTAT/HDX, puis tester une estimation des anomalies de rendement avec le climat et la télédétection. Il faut éviter de présenter une prédiction satellitaire comme une mesure officielle sans validation par des observations de parcelles.

## Ressources directement exploitables pour Madagascar

**FAOSTAT et HDX.** FAOSTAT donne un accès gratuit aux données alimentaires et agricoles de plus de 245 pays et territoires, depuis 1961 jusqu’à l’année disponible [1]. Le miroir HDX « Madagascar – Crops and Livestock » fournit un CSV téléchargeable et une API. Le fichier couvre 1961–2024, 278 produits et, pour les cultures primaires, la superficie récoltée, la production et le rendement [2]. Il est adapté à une analyse exploratoire du riz, du manioc, du maïs, de la patate douce, des cultures commerciales et de l’élevage. La licence indiquée par HDX est **CC BY-IGO** ; il faut conserver l’attribution et vérifier les conditions de la source FAO lors d’une redistribution.

**Banque mondiale.** L’indicateur « Cereal yield (kg per hectare) » pour Madagascar est disponible de 1961 à 2023, avec téléchargement et métadonnées. La page identifie la FAO comme source et indique une licence **CC BY 4.0** [3]. L’API World Bank est utile pour automatiser une série courte et comparable entre pays, mais l’indicateur agrège les céréales et ne remplace pas un rendement par culture.

**Sources nationales.** La rubrique Agriculture de l’INSTAT publie des tableaux de bord régionaux et des rapports, notamment les bilans alimentaires 2016–2022 [4]. Il faut vérifier, document par document, définition, unité, période, échantillonnage et droits de réutilisation. L’initiative FAO/GSARS sur l’enquête pilote AGPROD est particulièrement importante : combinait pratiques agricoles et coupe de récoltesur un sous-échantillon de parcelles [5]. La FAO signale des récoltes précoces et des parcelles inaccessibles pendant le pilote. **Recommandation :** demander aux producteurs nationaux les dictionnaires, poids d’enquête et fichiers anonymisés avant de comparer ces observations à FAOSTAT.

**Données d’observation de la Terre.** Le catalogue Google Earth Engine documente WorldCereal de l’Agence spatiale européenne à 10 m, des cartes mondiales de terres cultivées et des produits FAO WaPOR d’évapotranspiration [6]. Copernicus décrit l’emploi de l’observation de la Terre pour suivre l’état des cultures, les tendances, la gestion de l’eau et les prévisions de rendement [7]. Ces produits sont pertinents pour cartographier les zones cultivées et construire des variables explicatives ; ils ne donnent pas automatiquement un rendement local fiable à Madagascar. Les conditions d’utilisation et la licence doivent être lues dans la fiche de chaque collection.

## Méthodes pertinentes

Une base robuste doit normaliser cultures, unités, calendriers et identifiants géographiques. Il faut conserver séparément production, superficie récoltée et rendement, car le rendement dérivé peut amplifier les erreurs des deux premières variables. Une analyse descriptive calculera tendances, anomalies et incertitudes, par culture et région.

Pour la prévision, commencer par des modèles interprétables : régression réguliarisée, forêts aléatoires ou gradient boosting avec validation temporelle. Les variables candidates sont pluie, température, humidité du sol, évapotranspiration, NDVI/EVI, calendrier cultural et type de sol. L’article en accès libre de Rigden et al. montre une approche spécifiquement malgache : production de riz, manioc, maïs et patate douce entre 2010 et 2017, humidité des sols ESA-CCI, NDVI MODIS et statistiques du ministère [8]. Une limite essentielle est que l’étude explique la **production**, et non le rendement, parce que la superficie récoltée n’était pas disponible au niveau des districts. Les métriques à rapporter sont MAE, RMSE, biais et coefficient de détermination, avec une comparaison à une moyenne historique.

## Limites et risques

Les séries nationales peuvent mélanger recensement, déclarations et modélisation. HDX précise que la fiabilité dépend de l’échantillon, des définitions et des méthodes propres à chaque pays [2]. Les ruptures, imputations et révisions doivent être signalées. Les cartes satellitaires souffrent de nuages, de résolution insuffisante, de confusion entre cultures et de décalage pixel-parcelle. L’humidité ESA-CCI utilisée dans l’étude malgache mesure environ 5 cm de profondeur, moins que les racines usuelles [8].

Le risque majeur est la fuite temporelle : utiliser des variables calculées avec des années futures gonfle la performance. Le transfert international est fragile à cause des variétés, pratiques, calendriers et microclimats. Les données de ménages ou parcelles peuvent aussi être sensibles ; La Banque mondiale indique que ses microdonnées sont souvent sous une licence de recherche qui interdit la redistribution et la ré-identification [9].

## Prochaines vérifications

Télécharger d’abord le CSV HDX et contrôler doublons, valeurs manquantes, unités et définitions. Comparer ensuite riz et maïs aux rapports INSTAT et ministériels, en documentant les écarts. Confirmer la disponibilité des données AGPROD, poids et limites géographiques. Enfin, sélectionner des collections Earth Engine couvrant Madagascar, archiver versions et licences, puis valider hors année et hors région avec des coupes de récolte indépendantes.

## References

[1]: https://www.fao.org/faostat/en/ "FAOSTAT, accès aux données alimentaires et agricoles"
[2]: https://data.humdata.org/dataset/mdg-faostat-crops-livestock-production "HDX, Madagascar – Crops and Livestock"
[3]: https://data.worldbank.org/indicator/AG.YLD.CREL.KG?locations=MG "World Bank, Cereal yield – Madagascar"
[4]: https://www.instat.mg/thematique/agriculture "INSTAT Madagascar, rubrique Agriculture"
[5]: https://www.fao.org/in-action/global-strategy-agricultural-statistics/news-and-events/news-detail/data-processing-and-analysis-workshop---restitution-in-madagascar-for-the-pilot-agricultural-production-survey-(agprod)/en "FAO/GSARS, enquête pilote AGPROD à Madagascar"
[6]: https://developers.google.com/earth-engine/datasets/tags/agriculture "Google Earth Engine, catalogue des jeux agricoles"
[7]: https://www.copernicus.eu/en/about-copernicus/impact-copernicus/agriculture "Copernicus, applications de l’observation de la Terre en agriculture"
[8]: https://www.mdpi.com/2072-4292/14/5/1223 "Rigden et al., Retrospective Predictions of Rice and Other Crop Production in Madagascar"
[9]: https://datacatalog.worldbank.org/public-licenses "World Bank Data Catalog, accès et licences publiques"
[10]: https://github.com/datasets/world-development-indicators "GitHub datasets/world-development-indicators, extracteur des indicateurs World Bank"

Le dépôt GitHub [10] peut faciliter une extraction reproductible des indicateurs, mais ses métadonnées indiquent un petit nombre de commits ; il doit être traité comme un outil communautaire à vérifier, non comme l’autorité statistique.
