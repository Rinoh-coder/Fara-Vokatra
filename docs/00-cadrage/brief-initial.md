# Fara-Vokatra

### Système open source d'aide à la décision agricole pour Madagascar

---

## 1. Vision du projet

**Fara-Vokatra** ("le fruit de la récolte") est un système open source d'aide à la décision agricole qui répond à trois questions pour chaque région de Madagascar :

- **Quand** planter
- **Quoi** planter, et en quelle combinaison
- **Où**, avec quel niveau de risque

L'objectif n'est pas de produire un outil météo supplémentaire, mais de construire la couche manquante entre la donnée climatique et agronomique déjà produite par les institutions (CHIRPS, FAO, NASA) et une décision concrète, actionnable, à l'échelle régionale/locale.

Le projet vise trois impacts mesurables :

1. **Réduire les pertes agricoles** liées à un mauvais timing de plantation face aux aléas climatiques (sécheresse, retard de saison des pluies, cyclones)
2. **Réduire le trou de soudure alimentaire** — la période annuelle récurrente où la production locale ne couvre pas la consommation
3. **Réduire la dépendance structurelle aux importations** de denrées de base (notamment le riz), en optimisant l'usage du potentiel agricole local plutôt qu'en le subissant

---

## 2. Constat et légitimité du projet (les faits qui le fondent)

| Constat | Donnée |
|---|---|
| Écart croissant production/population | La population croît d'environ 3 %/an, la production de riz d'environ 2 %/an seulement : l'écart se creuse structurellement |
| Dépendance aux importations en forte hausse | Les importations de riz sont passées d'environ 262 000 tonnes en 2024 à plus de 800 000 tonnes en 2025 |
| Trou de soudure alimentaire documenté | Dans les ménages ruraux, il existe un trou prévisible de 4 à 5 mois chaque année où la production de riz ne couvre pas la demande, généralement comblé par du manioc ou de la patate douce, moins nutritifs |
| Sensibilité extrême au climat | Les retards de plantation en 2025 dans le centre et l'est du pays sont directement attribués à un déficit pluviométrique persistant en début de saison |
| Rendements chroniquement bas | La riziculture malgache reste peu mécanisée, pratiquée sur des sols pauvres, sans intrants, avec un rendement par hectare très en-dessous du potentiel |
| Calendriers agricoles existants trop génériques | Les calendriers FAO/GIEWS donnent des fenêtres de plantation nationales, uniformes, alors que la recherche scientifique montre une hétérogénéité spatiale forte du climat malgache |
| Recherche scientifique existante mais inexploitée | Une méthodologie précise de détection du début de saison des pluies par région existe déjà dans la littérature (règles pluviométriques validées), mais reste enfermée dans des publications académiques, jamais transformée en outil opérationnel actualisé |

**Conclusion du diagnostic** : la donnée et la méthode scientifique existent déjà séparément. Ce qui manque, c'est le système qui les relie, les actualise en continu, et les traduit en recommandation multi-cultures orientée vers la sécurité alimentaire — pas seulement vers le rendement.

---

## 3. Architecture fonctionnelle — les modules

### Module A — Détection et prédiction climatique (le socle)

**Fonction**
Détecter, pour chaque région, le début et la fin de la saison des pluies utile à l'agriculture, à partir de règles agro-climatiques scientifiquement validées, appliquées en continu sur des données climatiques ouvertes. Puis prédire, avec quelques semaines d'avance, si la saison à venir s'annonce normale, retardée ou déficitaire.

**Ce que le module doit produire concrètement**
- Une date de début de saison des pluies ("onset") par région et par année, recalculée automatiquement à partir des données récentes
- Un indice de risque climatique par région, mis à jour en continu pendant la saison de plantation
- Une prédiction précoce (avant confirmation complète de l'onset) de la probabilité que la saison soit normale, tardive ou déficitaire

**Rôle de la data science**
- Une baseline déterministe reproduit la règle scientifique publiée (ex. seuil de cumul de pluie sur une fenêtre glissante, absence de séquence sèche prolongée dans les jours suivants) et sert de référence vérifiable
- Un modèle supervisé (type Random Forest ou Gradient Boosting) est entraîné sur les décennies de données climatiques historiques pour apprendre à anticiper la qualité de la saison à partir de signaux précoces (anomalies de pluie en début de fenêtre, indices climatiques régionaux), ce qui va au-delà de la simple règle rétrospective
- Ce module est le plus proche d'un vrai problème de série temporelle et de classification, et constitue la brique scientifique la plus solide du projet

---

### Module B — Modélisation du rendement attendu par culture

**Fonction**
Pour chaque région et chaque culture candidate (riz, maïs, manioc, sorgho, patate douce, légumineuses), estimer la probabilité d'obtenir un bon rendement compte tenu du profil climatique détecté ou prédit par le Module A.

**Ce que le module doit produire concrètement**
- Un classement des cultures par probabilité de rendement satisfaisant, pour une région et une saison donnée
- Une estimation de la sensibilité de chaque culture au risque climatique identifié (ex. le sorgho est plus tolérant à la sécheresse que le riz)

**Rôle de la data science**
- Modèle prédictif entraîné sur la relation historique entre variables climatiques (issues du Module A et des données brutes CHIRPS/NASA POWER) et rendements observés par culture et par région (séries FAO Stat)
- Ce n'est pas un système de règles fixes : le modèle apprend la relation climat-rendement à partir des données, ce qui permet de capturer des interactions non triviales (ex. un déficit hydrique modéré en début de cycle affecte différemment le riz irrigué et le riz pluvial)
- Une attention particulière est portée à la disponibilité et la qualité des données de rendement historiques par région, qui conditionnent directement la fiabilité du modèle

---

### Module C — Optimisation multi-cultures anti-soudure

**Fonction**
C'est le cœur différenciant du projet. Au lieu de recommander une seule culture optimale, ce module propose une combinaison temporelle de cultures — un portefeuille agricole — qui minimise le nombre de mois sans disponibilité alimentaire locale sur l'année, tout en tenant compte du risque climatique de la saison.

**Ce que le module doit produire concrètement**
- Un calendrier de plantation combiné (ex. riz en saison principale + manioc en relais + maïs à cycle court en complément), calé pour que les périodes de récolte se chevauchent le moins possible et couvrent un maximum de mois de l'année
- Une estimation de la réduction attendue du trou de soudure par rapport à une stratégie mono-culture
- Une variante du calendrier adaptée si le Module A signale une saison à risque (ex. substitution partielle par des cultures plus résistantes à la sécheresse)

**Rôle de la data science**
- Formulation du problème comme un problème d'optimisation sous contrainte : maximiser la couverture calendaire de disponibilité alimentaire sous contrainte de risque climatique acceptable et de compatibilité agronomique des cultures entre elles (rotation, sol, main-d'œuvre)
- Alternative complémentaire : apprentissage à partir des données historiques régionales pour identifier quelles combinaisons de cultures ont statistiquement réduit la variance de disponibilité alimentaire dans le passé
- Ce module transforme le projet d'un outil de prédiction météo-agricole en un véritable outil de politique agricole locale, ce qui n'existe dans aucun outil actuellement public pour Madagascar

---

### Module D — Régionalisation fine (affinement spatial)

**Fonction**
Les données climatiques satellite ont une résolution d'environ 5 km, ce qui reste grossier face à l'hétérogénéité du relief et du climat malgache sur de courtes distances. Ce module affine les prédictions à une échelle plus locale (district, voire commune).

**Ce que le module doit produire concrètement**
- Des cartes de risque climatique et de recommandation culturale à une résolution plus fine que la donnée satellite brute

**Rôle de la data science**
- Modèle de correction statistique (downscaling) qui apprend la relation entre les variables topographiques (altitude, exposition, distance à la côte, à partir de données d'élévation ouvertes) et les écarts observés entre stations météo locales et estimation satellite
- C'est un véritable apport méthodologique : une interpolation simple ne suffit pas à capturer les effets de relief propres à Madagascar

---

### Module E — Validation, transparence et fiabilité

**Fonction**
Établir, documenter et publier la fiabilité réelle du système en le confrontant systématiquement aux événements climatiques et agricoles passés.

**Ce que le module doit produire concrètement**
- Un rapport de backtesting comparant les prédictions du système aux événements réels documentés (sécheresse prolongée du Grand Sud, retards de plantation, saisons normales)
- Des métriques de performance publiques et reproductibles (précision de détection d'onset, erreur de prédiction de rendement, taux de fausses alertes)
- Une documentation claire des cas où le système se trompe et pourquoi

**Rôle de la data science**
- C'est une étape méthodologique non négociable : sans validation rigoureuse sur des données historiques indépendantes de l'entraînement, aucune recommandation agricole ne peut être considérée comme fiable, quel que soit le raffinement du modèle
- Cette rigueur est ce qui distingue un projet de data science sérieux d'une démonstration technique

---

### Module F — Interface de restitution

**Fonction**
Rendre l'ensemble des modules consultable et exploitable simplement, par région, par culture, par utilisateur non technique.

**Ce que le module doit produire concrètement**
- Une consultation par région : risque climatique actuel, recommandation de culture, calendrier combiné anti-soudure
- Une vue temporelle : évolution du risque au fil de la saison
- Une restitution en langage clair, orientée décision plutôt que donnée brute

**Rôle de la data science**
Ce module n'est pas un module de data science à proprement parler, mais il conditionne l'impact réel du projet : un modèle non consulté n'a aucun effet. Il doit néanmoins refléter fidèlement l'incertitude des modules précédents (afficher des probabilités, pas des certitudes).

---

## 4. Pourquoi l'open source est une décision structurante, pas un choix de licence

Le caractère open source du projet n'est pas accessoire : il conditionne la crédibilité et l'impact réel du système.

**Reproductibilité scientifique**
Le projet repose sur une chaîne d'hypothèses (règles agro-climatiques, choix de modèles, données de rendement) qui doivent être vérifiables par des tiers compétents — chercheurs, agronomes, ONG, institutions publiques malgaches. Sur un sujet qui touche à la sécurité alimentaire, une méthode fermée n'a aucune légitimité, même si elle est techniquement solide.

**Auditabilité et responsabilité**
Une recommandation agricole erronée a des conséquences réelles sur des populations vulnérables. Le code, les données d'entraînement, les métriques de validation et les limites du système doivent être ouverts à l'examen et à la critique, pas seulement les résultats.

**Extensibilité communautaire**
Le projet est pensé pour être complété par d'autres contributeurs : ajout de nouvelles cultures, affinement des règles par région, intégration de données locales complémentaires, traduction en malgache et dans les langues locales, adaptation à d'autres pays à climat comparable.

**Accessibilité pour les acteurs qui en ont le plus besoin**
Les structures qui pourraient réellement déployer cet outil sur le terrain — coopératives agricoles, ONG locales, services techniques régionaux du ministère de l'Agriculture — doivent pouvoir l'utiliser, le forker et l'adapter sans barrière financière ni contractuelle.

**Continuité au-delà du porteur initial**
Un projet open source bien documenté peut survivre à son créateur initial et être repris, maintenu, amélioré par une communauté, ce qu'un projet fermé porté par une seule personne ne permet pas.

**Conséquences concrètes pour la mise en œuvre**
- Licence permissive (MIT ou Apache 2.0)
- Documentation complète de la méthodologie, des sources de données et des choix de modélisation, au même niveau d'exigence qu'une publication scientifique
- Notebooks permettant à quiconque de reproduire les résultats à l'identique
- Jeux de données de test et de validation rendus publics
- Structure d'accueil aux contributions dès le lancement (guide de contribution, choix des premiers sujets ouverts aux contributeurs externes)
- Publication des métriques de fiabilité de manière continue et non a posteriori, pour que la confiance dans le système soit fondée sur des preuves vérifiables plutôt que sur des affirmations
