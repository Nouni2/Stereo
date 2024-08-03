# Projet Stereophotographie

## Présentation du Projet

Le projet Stereophotographie a pour but de transformer une collection d’images stéréophotographiques en images en trois dimensions. La base de données utilisée provient de la Stéréothèque, une association située en Nouvelle-Aquitaine, et contient principalement des images de bâtiments historiques. Ce projet fait suite à un travail antérieur en C++, qui présentait des difficultés avec les transformations 3D.

### Objectif

L'objectif est de développer un algorithme qui applique une méthode de visualisation 3D à des images stéréophotographiques. Le projet enregistre également les transformations sous forme de fichiers SVG pour permettre une reconstruction ultérieure. Les méthodes de visualisation comprennent :

- **Côte à côte (Side-by-Side)** : Juxtapose les images gauche et droite après séparation de l'arrière-plan.
- **Haut-Bas (Top-Bottom)** : Utilise la polarisation pour séparer les images destinées à chaque œil, avec une superposition ajustée par l'utilisateur.
- **Anaglyphe** : Superpose les images après application de filtres chromatiques pour créer des perceptions visuelles différentes pour chaque œil.

### Conception Modulaire

Le code est modulaire, ce qui permet des ajustements et extensions faciles. Les images intermédiaires sont stockées dans un dossier temporaire, permettant à l'utilisateur de revenir à une étape antérieure.

### Accessibilité

Le projet est conçu pour être utilisable par un large public, quel que soit leur niveau de compétence technique.

## Organisation et Management

### Approche Agile

Le projet suit une méthodologie agile, itérative et collaborative, avec des réunions bihebdomadaires puis quotidiennes pour gérer la progression et les obstacles.

### Axes de Travail

Le projet Stereophotographie est organisé autour de trois axes principaux : l'extraction, l'exploitation, et la visualisation. Ces axes reflètent le flux de travail nécessaire pour transformer des images stéréophotographiques en visualisations tridimensionnelles.

#### 1. Extraction des Contours

**Objectif :** Extraire avec précision les contours des images stéréo pour faciliter leur traitement ultérieur.

- **Description :** Cette phase est cruciale car elle établit la base des transformations ultérieures. Le processus commence par isoler les images gauche et droite à partir du doublet stéréo initial. Ensuite, il s'agit d'extraire les contours pertinents à l'aide de méthodes manuelles ou automatiques. Les contours obtenus sont ensuite enregistrés sous forme de fichiers SVG, servant de référence pour les transformations géométriques futures.
  
- **Importance :** L'extraction précise des contours garantit que les images peuvent être correctement alignées et traitées lors des étapes suivantes. Les contours définissent les limites des objets dans les images, facilitant les ajustements et améliorations de l'image stéréo.

#### 2. Exploitation des Images

**Objectif :** Aligner et traiter les images pour créer une perception de profondeur.

- **Description :** Cette étape consiste à manipuler les images stéréo afin de créer l'effet de perspective nécessaire pour la visualisation en 3D. Elle comprend l'alignement des images sur des points de référence communs et la gestion des éléments non partagés par les deux images. Ce processus utilise des algorithmes d'alignement pour corriger les distorsions et assurer une parfaite superposition des images.
  
- **Importance :** L'exploitation adéquate des images est essentielle pour préparer les images stéréo à la visualisation. Sans un bon alignement, les images 3D résultantes pourraient présenter des artefacts ou ne pas être perçues correctement par l'utilisateur.

#### 3. Visualisation

**Objectif :** Générer des visualisations 3D à partir des images stéréo traitées.

- **Description :** La visualisation est la phase finale, où les images traitées sont transformées en formats visuels 3D utilisables. Plusieurs méthodes de visualisation sont disponibles, y compris "Côte à Côte" (SBS), "Haut-Bas" (Top-Bottom), et l'anaglyphe. Chaque méthode utilise une technique différente pour simuler la perception de profondeur, permettant à l'utilisateur de choisir le mode de visualisation qui convient le mieux à ses besoins.
  
- **Importance :** La visualisation est l'objectif final du projet, transformant les données et manipulations précédentes en une expérience visuelle tangible. Elle offre des moyens variés et adaptables de percevoir la profondeur dans des images bidimensionnelles, rendant le projet pertinent pour diverses applications, de la conservation historique à l'éducation.

### Processus de Travail

Le processus de travail suit un ordre séquentiel : 

1. **Extraction :** Les images stéréo sont d'abord extraites et préparées. Cette étape pose les fondations pour le traitement ultérieur en définissant les contours et les caractéristiques principales des images.

2. **Exploitation :** Une fois les contours et images extraits, ils sont alignés et traités pour corriger les disparités et aligner les perspectives. Cette phase assure que les images sont prêtes pour la conversion en formats 3D.

3. **Visualisation :** Enfin, les images alignées et traitées sont converties en différents formats 3D, fournissant des résultats prêts à l'emploi pour l'utilisateur final.


---

Ce découpage en axes de travail est conçu pour optimiser l'efficacité du processus, avec chaque phase visant à renforcer et faciliter les opérations des suivantes. En abordant chaque étape avec des outils et techniques adaptés, le projet parvient à transformer des archives d'images en représentations tridimensionnelles immersives et informatives.


## Structure du Projet

```
.
├── data
│   ├── in
│   └── out
├── src
│   ├── extraction
│   ├── exploitation
│   └── generation
├── main.py
└── README.txt
```

## Dépendances

- Python 3.x
- OpenCV
- svgwrite
- numpy

## Installation

1. **Cloner le dépôt** :
   ```
   git clone https://github.com/Nouni2/Stereo
   ```

2. **Installer les dépendances** :
   ```
   pip install opencv-python-headless svgwrite numpy
   ```

