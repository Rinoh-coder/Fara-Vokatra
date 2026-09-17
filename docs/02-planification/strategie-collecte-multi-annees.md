# DS-011B — Préparation de la collecte multi-années

## Décision proposée

La collecte historique retenue couvre **du 1er janvier 1991 au 31 décembre 2024**. La période 1991–2020 servira de référence climatique principale. Les années 2021–2024 seront conservées comme période d’évaluation temporelle séparée.

Cette séparation suit une logique scientifique simple : une référence doit être définie avant l’évaluation et ne doit pas utiliser les années futures. La période 1991–2020 correspond aussi à une période standard de normale climatique de trente ans. CHIRPS v3 est annoncé par le Climate Hazards Center comme une série quotidienne quasi-globale allant de 1981 à aujourd’hui ; la borne 1991 évite d’étendre inutilement le volume tandis que 2024 fournit quatre années récentes complètes au moment du cadrage.

La période retenue ne prouve pas que 1991–2020 soit la meilleure normale pour chaque zone agricole. Elle constitue un choix initial, versionné et révisable uniquement avec une justification documentée.

## Pourquoi ne pas utiliser 2025–2026

La collecte s’arrête à 2024 afin d’éviter les années civiles incomplètes ou les produits finaux susceptibles d’être révisés. La date d’accès et la version du produit seront conservées dans chaque manifeste. Une extension ultérieure devra être explicitement versionnée.

## Volume et stockage

Le quota Drive inspecté le 17 septembre 2026 est de 15 GiB, dont environ 0,28 MiB utilisé. Dans l’échantillon réel, deux rasters bruts globaux représentent environ 27,3 MiB, soit environ 13,6 MiB par jour. Les dix rasters nettoyés des cinq zones représentent environ 191 KiB, soit environ 95,6 KiB par jour.

Ces mesures ne sont pas une garantie pour toutes les dates, mais elles donnent un ordre de grandeur. La stratégie ne doit jamais conserver 34 années de rasters bruts globaux. Le brut est téléchargé temporairement, utilisé pour les cinq découpages, puis supprimé uniquement après succès du découpage et du calcul des checksums. Les rasters nettoyés, les séries quotidiennes, les manifestes, les rapports qualité et les checksums sont conservés.

L’archive Drive proposée est :

```text
Fara-Vokatra/
└── CHIRPS-v3/
    └── 1991-2024/
        ├── 1991/
        │   ├── northwest/
        │   ├── east/
        │   ├── highlands/
        │   ├── west/
        │   ├── south/
        │   ├── manifest.json
        │   └── quality-report.json
        ├── ...
        ├── daily-series/
        └── collection-summary/
```

Unité d’archivage : une année. Cette unité limite la reprise après incident et permet de valider chaque année avant de passer à la suivante. Les fichiers bruts temporaires restent sur le stockage local pendant une année de traitement et ne sont pas archivés sur Drive.

## Stratégie d’exécution

La collecte sera exécutée dans l’ordre croissant des années, une année à la fois. Pour chaque année, le pilote téléchargera les 365 ou 366 rasters bruts, produira une sortie pour les cinq zones et calculera les checksums. Le validateur devra confirmer le nombre attendu de couples date/zone, l’absence d’erreur, l’existence des fichiers et la cohérence des checksums.

Après validation, les sorties nettoyées et le rapport qualité seront archivés sur Drive. Le brut local pourra ensuite être supprimé. Une erreur arrête la collecte avant l’année suivante. Une reprise doit réutiliser les fichiers complets déjà présents et supprimer ou remplacer uniquement les fichiers partiels.

La production des séries CSV intervient après validation des rasters d’une année. La série multi-années ne sera assemblée qu’après validation de toutes les années nécessaires à la période d’analyse.

## Contrôles obligatoires

Avant autorisation de la collecte complète, les éléments suivants doivent être présents :

1. la configuration `config/collecte_multi_annees.json` ;
2. le test DS-011A déjà validé ;
3. une commande de collecte par année ;
4. un manifeste par année et un manifeste global ;
5. un rapport qualité par année ;
6. un registre des fichiers archivés sur Drive ;
7. une règle confirmant que les données 1991–2020 et 2021–2024 restent séparées ;
8. une procédure d’arrêt sur erreur ou quota insuffisant.

## Limites scientifiques

CHIRPS v3 est une estimation maillée combinant satellite et stations. Le produit quotidien `rnl` répartit les cumuls pentadaires avec l’aide des précipitations quotidiennes ERA5 ; les valeurs quotidiennes ne doivent donc pas être interprétées comme des mesures pluviométriques quotidiennes indépendantes. Les boîtes restent des emprises exploratoires, pas des régions administratives ni des parcelles.

La période 1991–2020 ne résout pas les biais de relief, de couverture des stations ou de représentativité locale. Elle fournit uniquement une base commune pour comparer les années et zones selon un protocole reproductible.

## Critère d’autorisation de la prochaine étape

DS-011B sera terminée lorsque la période, le découpage, le volume, la stratégie Drive, la reprise et les critères d’arrêt seront validés dans le dépôt. La collecte multi-années pourra alors commencer par une seule année test, suivie d’un rapport qualité avant toute accélération.

## Références

[1]: https://www.chc.ucsb.edu/data/chirps3 "Climate Hazards Center — CHIRPS v3"

[2]: https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/readme.txt "CHIRPS v3 daily product documentation"

[3]: https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/climate-services/wmo-climatological-normals "WMO Climatological Normals"

[4]: https://www.fao.org/giews/countrybrief/country.jsp?code=MDG "FAO GIEWS — Madagascar Country Brief"
