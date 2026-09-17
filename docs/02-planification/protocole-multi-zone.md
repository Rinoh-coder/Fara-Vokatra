# Protocole multi-zone pour l’analyse CHIRPS

## But

Ce protocole définit une première comparaison géographique de l’onset des pluies à Madagascar. Il ne prétend pas représenter les régions administratives ni les zones cultivées. Les cinq unités sont des **boîtes d’échantillonnage techniques** choisies pour couvrir des contrastes climatiques plausibles entre le Nord-ouest, l’Est, les Hautes Terres, l’Ouest et le Sud.

Le portail climatique de la Banque mondiale présente Madagascar avec des classifications climatiques, des cycles saisonniers et des couches de topographie et de risques. La FAO/GIEWS décrit une saison principale dont les pluies commencent normalement autour de novembre dans la majeure partie du pays, tout en signalant des retards et une distribution très inégale selon les régions et les années. Ces sources justifient une analyse différenciée, mais elles ne valident pas les coordonnées exactes des boîtes utilisées ici. Les boîtes restent donc des choix de plan expérimental à tester.

## Configuration

Les boîtes sont définies dans `config/zones_madagascar.json` en longitude/latitude WGS84. Chaque zone possède un identifiant stable, une emprise et une justification. Toute modification de coordonnées doit être enregistrée dans le journal des décisions, car elle modifie l’unité d’analyse.

## Protocole de données

Pour chaque zone, télécharger les mêmes dates CHIRPS v3, le même produit (`final/rnl` au premier essai), le même seuil de couverture et la même version du code. Les fichiers bruts restent hors Git. Les manifestes doivent conserver l’URL, la version, la date d’accès, les empreintes SHA-256 et la configuration de la zone.

La série quotidienne est calculée séparément pour chaque boîte. La moyenne spatiale est utilisée comme baseline simple. Elle doit être interprétée avec la couverture, le nombre de pixels, les valeurs extrêmes et les limites de résolution. Aucun résultat ne doit être comparé entre zones si les dates, versions ou règles de nettoyage diffèrent.

## Protocole d’analyse

Pour chaque zone et chaque année complète :

1. calculer l’onset avec la règle à seuils ;
2. calculer l’onset Liebmann avec une climatologie leave-one-year-out ;
3. conserver le statut de qualité et le nombre d’années de climatologie ;
4. mesurer la divergence absolue entre les deux dates ;
5. examiner les années où la divergence dépasse un seuil exploratoire de 30 jours ;
6. comparer les résultats aux indicateurs FAO/GIEWS et, si possible, aux stations de la DGM.

Le seuil de 30 jours est un outil de tri pour la revue, pas un critère agronomique universel. Les paramètres des méthodes restent constants dans la comparaison principale. Une analyse de sensibilité séparée pourra modifier un paramètre à la fois.

## Comparaisons et statistiques

La comparaison doit rapporter la médiane, l’intervalle interquartile, le nombre d’années valides et la proportion d’années sans détection. Les résultats doivent être stratifiés par zone. Il faut éviter de conclure à une différence climatique sur la base d’une seule année ou d’une seule date extrême.

Les tests statistiques devront tenir compte de l’autocorrélation et du petit nombre d’années effectivement comparables. Dans le premier rapport, une description robuste est préférable à un test de significativité fragile. Les intervalles et la taille d’échantillon doivent accompagner toute moyenne.

## Critères d’arrêt et limites

L’analyse est suspendue si la couverture est insuffisante, si les dates sont manquantes, si la transition de version CHIRPS n’est pas documentée ou si les résultats sont présentés comme des conseils de semis sans validation agronomique. Une boîte peut être redéfinie si elle mélange des régimes climatiques trop hétérogènes, mais cette décision doit être documentée et ne doit pas être prise uniquement pour améliorer une métrique.

## Références

[1]: https://climateknowledgeportal.worldbank.org/country/madagascar "World Bank Climate Change Knowledge Portal — Madagascar"

[2]: https://www.fao.org/giews/countrybrief/country.jsp?code=MDG "FAO GIEWS — Madagascar Country Brief"

[3]: https://www.chc.ucsb.edu/data/chirps3 "Climate Hazards Center — CHIRPS v3"
