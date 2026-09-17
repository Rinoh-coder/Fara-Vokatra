# Rapport scientifique — Fara-Vokatra

**Version :** 0.1 — cadrage initial  
**Auteur :** Manus AI, avec le porteur du projet  
**Statut :** document évolutif, aucun résultat empirique validé à ce stade

## Résumé

Fara-Vokatra est un projet open source visant à étudier comment des données climatiques et agronomiques ouvertes peuvent soutenir la planification agricole à Madagascar. Le projet est conçu comme une chaîne de preuves : une baseline explicite doit précéder tout modèle d’apprentissage, et toute recommandation doit être conditionnée par une validation hors échantillon, une analyse d’incertitude et une documentation de ses limites.

Le premier jalon porte sur la détection et la prévision précoce du début utile de la saison des pluies. Les modules de rendement, d’optimisation multi-cultures, de régionalisation fine et d’interface seront développés seulement si les données et performances du socle le justifient.

## Introduction

Le brief initial formule un besoin d’aide à la décision autour du calendrier de plantation, du choix des cultures et de la réduction de la période de soudure. Ces motivations sont pertinentes pour le cadrage, mais les chiffres et relations causales mentionnés dans le brief doivent être vérifiés avant d’être présentés comme des faits. Le registre des hypothèses assure cette séparation.

## Question et hypothèses

La question principale est : **un indicateur d’onset calculé à partir de données climatiques ouvertes peut-il être évalué et utilisé pour une prévision précoce régionale avec une performance supérieure à des baselines simples ?** Les hypothèses H-001 à H-006 sont suivies dans `docs/00-cadrage/registre-hypotheses.md`.

## Données et méthode

Les données seront choisies selon leur couverture de Madagascar, leur résolution, leur qualité, leur licence et leur reproductibilité d’accès. La méthode précisera la définition opérationnelle de l’onset, les fenêtres de calcul, les règles de gestion des valeurs manquantes et les seuils de qualité.

L’évaluation suivra une partition temporelle. Les années futures ne pourront pas influencer la construction des variables, la sélection des hyperparamètres ou le choix des seuils. Les performances seront comparées à une baseline déterministe et à une baseline naïve. Le rapport final présentera l’erreur de date, les métriques de classification, la calibration éventuelle, la variabilité régionale et les cas d’échec.

## Résultats

Aucun résultat empirique n’est déclaré dans cette version. Les rapports de recherche et les résultats du pipeline seront ajoutés avec une date, une version de code, un manifeste de données et une commande de reproduction.

## Discussion et limites

La résolution des données climatiques ne doit pas être confondue avec la précision locale de la recommandation. La relation climat-rendement peut être confondue par l’irrigation, les pratiques agricoles, les sols, les ravageurs et les décisions humaines. Une performance prédictive ne constitue pas automatiquement une preuve causale ni une garantie agronomique.

## Reproductibilité

La reproduction reposera sur des scripts versionnés, des paramètres explicites, des tests, des notebooks réservés à l’exploration et des rapports générés à partir de données identifiées. Les versions des dépendances et les instructions d’exécution seront documentées dans le README.

## Références

Les références seront ajoutées après vérification des ressources dans `docs/05-recherche/`.
