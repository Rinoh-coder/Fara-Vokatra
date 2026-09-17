# Cadrage scientifique — Fara-Vokatra

## 1. Problème étudié

Fara-Vokatra étudie la possibilité de transformer des observations climatiques et agronomiques ouvertes en informations d’aide à la décision pour la planification agricole à Madagascar. La question scientifique initiale est volontairement limitée : **peut-on détecter et prévoir suffisamment tôt le début utile de la saison des pluies à l’échelle régionale, avec une performance mesurable et une incertitude explicitée ?**

Cette question constitue le premier test de faisabilité. Les recommandations de cultures et l’optimisation anti-soudure ne seront considérées qu’après validation de cette brique et vérification de la disponibilité des données de rendement.

## 2. Hypothèses

**H1 — Détection.** Une règle agro-climatique explicitement définie détecte l’onset avec une erreur médiane compatible avec l’usage exploratoire régional, comparée à une référence documentée.

**H2 — Prévision.** Des signaux pluviométriques précoces et des variables climatiques agrégées permettent de classer une saison comme normale, tardive ou déficitaire mieux qu’une baseline naïve, évaluée par validation temporelle.

**H3 — Généralisation.** Les performances restent acceptables sur des années et des régions non utilisées pour ajuster les paramètres. Cette hypothèse est essentielle et peut être rejetée.

**H4 — Rendement.** Les données disponibles permettent au moins une analyse exploratoire climat-rendement pour un sous-ensemble de cultures et de régions. Cette hypothèse ne doit pas être présumée avant audit des données.

**H5 — Décision.** Une recommandation utile doit afficher l’incertitude, les conditions d’application et les cas où aucune recommandation fiable ne peut être produite.

## 3. Variables et unités d’analyse

L’unité d’analyse principale est le couple **région–année agricole**. Les observations journalières de pluie sont agrégées en fenêtres temporelles explicites. Les variables candidates comprennent la pluie cumulée, les séquences sèches, les anomalies par rapport à une climatologie de référence, la date d’onset détectée, la longueur de saison et, lorsque disponible, des covariables topographiques.

La cible de prévision doit être définie avant l’entraînement. Une première option est une classe à trois modalités : normale, tardive ou déficitaire, dérivée d’une distribution historique et d’un seuil documenté. Les seuils ne doivent pas être choisis après inspection du test.

## 4. Protocole de preuve

Le projet suivra une chaîne de preuve : définition de la question, inventaire des données, définition de la cible, baseline déterministe ou naïve, partition temporelle, entraînement reproductible, évaluation hors échantillon, analyse d’erreurs, interprétation prudente et revue des limites.

Aucune métrique isolée ne suffira. La détection sera décrite par l’erreur de date et la proportion de détections valides. La classification sera évaluée par balanced accuracy, macro-F1, matrice de confusion et, si les probabilités sont produites, calibration. Les intervalles d’incertitude et la variabilité entre régions seront rapportés.

## 5. Critères de succès du premier jalon

Le MVP est réussi si un tiers peut reproduire le pipeline à partir d’un environnement documenté, si la baseline est exécutée avant le modèle d’apprentissage, si les partitions temporelles empêchent les fuites, si les résultats sont accompagnés de leurs limites et si les données ou scripts de téléchargement respectent les licences applicables. La réussite ne signifie pas que le système est prêt à conseiller directement un agriculteur.

## 6. Risques scientifiques

Les principaux risques sont l’incohérence entre résolution climatique et unité administrative, la qualité variable des observations satellite, la faible disponibilité de rendements régionaux, la non-stationnarité climatique, les biais de sélection des stations, les définitions concurrentes de l’onset et la confusion entre corrélation et causalité. Chaque risque doit être enregistré avec un test ou une mitigation, plutôt que traité par une affirmation générale.

## 7. Limites d’usage

Le prototype ne remplace ni les services météorologiques, ni les agronomes, ni les décisions locales. Il ne doit pas être utilisé comme garantie de rendement, comme conseil financier ou comme signal unique pour engager des intrants. Toute mise en production nécessiterait une validation locale, une gouvernance des données et une évaluation d’impact indépendante.

## Références

Les références vérifiées seront ajoutées dans `docs/05-recherche/` et citées ici après la revue des sources. Les affirmations du brief initial sont conservées comme hypothèses à vérifier, non comme résultats établis.
