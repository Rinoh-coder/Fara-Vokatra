# Spécification du MVP scientifique

## Objectif

Produire un pipeline reproductible qui calcule un indicateur d’onset des pluies par région et année, établit une baseline, puis teste une classification précoce de la qualité de la saison sans fuite temporelle.

## Entrées minimales

Le pipeline doit accepter une série de pluie journalière ou quasi-journalière, une géométrie ou un identifiant régional, une période de référence et un fichier de configuration versionné. Les sources exactes seront sélectionnées dans l’inventaire de données après contrôle de licence, couverture, résolution et qualité.

## Sorties attendues

Le pipeline produit : une table d’observations nettoyées, une table région–année avec dates et indicateurs d’onset, des prédictions hors échantillon, un rapport de métriques, des graphiques de contrôle et un manifeste de provenance indiquant les versions, paramètres et sources.

## Exigences méthodologiques

La définition de l’onset doit être paramétrable et enregistrer les paramètres utilisés. Les années de test doivent être postérieures aux années d’entraînement dans le protocole principal. Les transformations calculées sur l’ensemble des données sont interdites lorsqu’elles utilisent implicitement le futur. Les données manquantes, changements de calendrier et régions sans couverture suffisante doivent produire des diagnostics explicites.

## Baselines

La première baseline est la règle agro-climatique retenue dans la littérature. La seconde est une baseline naïve de prévision fondée sur la climatologie historique ou la classe majoritaire, selon la cible. Aucun modèle Random Forest ou Gradient Boosting ne sera déclaré utile s’il ne dépasse pas ces références dans une évaluation hors échantillon et stable.

## Modèles candidats

Le premier modèle supervisé sera choisi pour sa lisibilité et sa robustesse, par exemple une forêt aléatoire ou un gradient boosting. Les hyperparamètres seront limités et documentés. La sélection de modèle sera effectuée dans l’entraînement uniquement. La complexité ne sera pas augmentée pour compenser une faiblesse de données.

## Critères d’acceptation

Un incrément est accepté lorsque le code est testé, les données d’entrée sont décrites, les paramètres sont versionnés, la commande de reproduction fonctionne, les métriques sont calculées sur des données tenues à l’écart et les limites sont inscrites dans le rapport. Le pipeline doit échouer clairement si une colonne obligatoire, une unité ou une couverture minimale manque.

## Hors périmètre du MVP

La recommandation agronomique personnalisée, l’optimisation de portefeuille, le downscaling à la commune, l’application mobile et la collecte de données propriétaires sont hors périmètre du premier jalon. Ils pourront être spécifiés après validation des fondations.
