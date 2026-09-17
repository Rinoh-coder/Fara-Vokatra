# Méthodes scientifiques de détection de l’onset des pluies

## Résumé

L’**onset des pluies** désigne ici le début opérationnel de la saison humide, et non simplement la première averse. En agriculture, le signal utile doit annoncer une humidité suffisante pour semer et permettre la survie des plantules. Il n’existe pas de seuil universel : la définition dépend du climat, de la culture et du risque de **faux onset**, pluie initiale suivie d’une période sèche [1]. Pour Madagascar, la stratégie la plus défendable est de comparer au moins une méthode agronomique à seuils et une méthode d’anomalies cumulées, puis de calibrer les résultats avec des pluviomètres et les pratiques locales.

## Ressources directement exploitables pour Madagascar

La ressource de base recommandée est **CHIRPS**, une série quasi mondiale couvrant 50°S–50°N depuis 1981, à 0,05° (environ 5 km), produite par combinaison d’imagerie satellite, climatologie et observations de stations [2]. Les données quotidiennes et mensuelles sont accessibles gratuitement via le Climate Hazards Center et via Digital Earth Africa, qui fournit des GeoTIFF optimisés, un accès AWS S3, des services WCS/WMS et un notebook Jupyter [3]. CHIRPS est déclaré dans le domaine public autant que possible juridiquement [2] [3]. Sa version 2 doit toutefois être remplacée progressivement par CHIRPS v3, car la production de v2 doit s’arrêter après décembre 2026 [2].

Pour démarrer, télécharger CHIRPS quotidien sur Madagascar, agréger les pixels par commune ou bassin, puis calculer l’onset chaque année depuis 1981. Le portail FAO/GIEWS Madagascar complète cette approche avec des indicateurs de précipitation, des cumuls par décade et des anomalies par rapport à une moyenne de long terme ; il donne aussi un accès aux couches cartographiques et aux statistiques zonales [4]. La FAO indique que les pluies saisonnières commencent normalement autour de novembre dans la majeure partie du pays, mais que le début peut être retardé de plusieurs décades dans le Sud et l’Ouest : cette hétérogénéité interdit d’appliquer une date nationale unique [5].

Le dépôt GitHub `adrHuerta/rainfall_onset2` fournit du code R/Python pour l’onset et la cessation, avec exemples [6]. Il est sous **GPL-3.0**, donc réutilisable et modifiable sous les obligations copyleft de cette licence [7]. Son activité observée est limitée ; il faut auditer les dépendances, tester CHIRPS et documenter toute adaptation.

## Méthodes pertinentes

**1. Méthode agronomique à seuils.** On définit l’onset comme le premier jour d’une séquence de jours humides recevant au moins `P` mm, avec une contrainte sur le nombre `N` de jours et une vérification prospective : aucune séquence sèche de durée `n` et de pluie inférieure à `p` ne doit survenir dans les `C` jours suivants [1]. Une variante utilisée en Afrique exige par exemple un cumul sur trois jours et exclut un long épisode sec ultérieur. Cette méthode est directement interprétable pour une décision de semis, mais `P`, `N`, `n`, `p` et `C` doivent être calibrés par culture et zone ; modifier seulement `P` peut déplacer l’onset de plusieurs semaines [1]. Il faut expliciter le seuil de « jour humide », la période de recherche et les valeurs manquantes.

**2. Anomalie cumulée de pluie quotidienne (méthode de Liebmann).** Pour chaque jour, on soustrait la pluie moyenne climatologique du jour, puis on cumule les anomalies. Le minimum local dans la saison définit l’onset ; le maximum définit la cessation [8]. Elle permet de comparer des régions et climats différents, avec une moyenne propre à chaque pixel. Elle prend mieux en compte un faux onset : une forte pluie suivie d’une longue sécheresse fait redescendre le cumul et ne devient pas le minimum final [8]. Elle convient à la cartographie de Madagascar, y compris les zones à deux saisons. Elle identifie toutefois généralement l’onset après la saison et convient mal au temps réel [8].

**3. Méthodes par pentades, décades ou pourcentage saisonnier.** Elles lissent le bruit quotidien et sont adaptées aux produits FAO/GIEWS. On peut déclarer l’onset après plusieurs pentades dépassant un seuil, ou un pourcentage du cumul climatologique. Elles sont simples à communiquer, mais un seuil de pourcentage ne filtre pas nécessairement un faux onset ; elles sont aussi moins précises pour la date de semis.

## Limites et risques

Une grille satellite fournit une moyenne surfacique et peut sous-estimer les pluies extrêmes en terrain complexe ; les stations sont plus locales mais rares [2] [3]. Les cyclones, reliefs et contrastes Est–Ouest rendent Madagascar sensible à ces erreurs. Les méthodes à seuils transfèrent mal leurs paramètres entre cultures. La méthode d’anomalies cumulées dépend de la période climatologique et ignore certains changements interannuels ; des pluies légères peuvent raccourcir artificiellement la saison [8]. Un onset météorologique n’est pas automatiquement agronomique : contrôler humidité du sol, évapotranspiration et calendrier variétal.

## Prochaines vérifications

Il faut obtenir les séries de la Direction Générale de la Météorologie et sélectionner des stations de référence dans l’Est, les Hautes Terres, l’Ouest et le Sud. Comparer ensuite CHIRPS v2 et v3 sur une période commune, vérifier les biais par station et tester la sensibilité des paramètres. Confronter les dates aux semis, aux sécheresses post-semis et à l’humidité du sol. Produire enfin une date historique robuste et un indicateur opérationnel par décade, avec incertitude et drapeau « faux onset possible ».

## References

[1]: https://journals.ametsoc.org/view/journals/clim/26/22/jcli-d-12-00730.1.xml "Regional-Scale Rainy Season Onset Detection, Journal of Climate"

[2]: https://www.chc.ucsb.edu/data/chirps "CHIRPS: Rainfall Estimates from Rain Gauge and Satellite Observations, Climate Hazards Center"

[3]: https://docs.digitalearthafrica.org/en/latest/data_specs/CHIRPS_specs.html "Rainfall estimates (CHIRPS), Digital Earth Africa documentation"

[4]: https://www.fao.org/giews/earthobservation/country/index.jsp?code=MDG "FAO/GIEWS Earth Observation indicators for Madagascar"

[5]: https://www.fao.org/giews/countrybrief/country.jsp?code=MDG "FAO/GIEWS Country Brief on Madagascar"

[6]: https://github.com/adrHuerta/rainfall_onset2 "adrHuerta/rainfall_onset2, GitHub repository"

[7]: https://github.com/adrHuerta/rainfall_onset2/blob/master/LICENSE "GNU General Public License v3.0, rainfall_onset2"

[8]: https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016JD025428 "The onset and cessation of seasonal rainfall over Africa, Journal of Geophysical Research: Atmospheres"

> **Note de vérification.** Les faits sur les méthodes, les résolutions, les dates de couverture, les accès et les licences ont été contrôlés sur les pages sources citées. Les choix de paramètres proposés pour Madagascar sont des recommandations méthodologiques, non des seuils officiellement validés pour toutes les cultures.
