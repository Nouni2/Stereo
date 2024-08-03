# Projet de Stereophotographie

## Partie Extraction

La partie extraction de ce projet vise à automatiser le processus d'extraction des images gauche et droite d'un doublet d'images provenant d'archives numérisées. Cette section du projet est divisée en trois points clés.

### Point 1 : Sélection Manuelle des Contours et Extraction

#### Description
Ce point consiste à développer un outil permettant à l'utilisateur de sélectionner manuellement les contours des images en dessinant des traits et de les extraire. Une option de "snapping" est disponible pour faciliter la sélection, tout en préservant le contrôle manuel de l'utilisateur.

#### Fonctionnalités
- **Sélection Manuelle**: Permet à l'utilisateur de dessiner des traits pour sélectionner les contours.
- **Fermeture de la Sélection**: Possibilité de fermer la sélection en appuyant sur "c".
- **Option de Snapping**: Facilite la sélection en ajustant automatiquement les traits aux bords détectés.

### Point 2 : Adaptation de Contours Déjà Présents

#### Description
Cet outil permet d'adapter un contour préalablement créé à une nouvelle image, en utilisant des transformations linéaires comme le déplacement et le redimensionnement.

#### Fonctionnalités
- **Adaptation Manuelle**: Déplacement et redimensionnement des contours.
- **Adaptation Automatique**: Utilisation de la détection de bords pour ajuster les contours automatiquement.

### Point 3 : Sélection Automatique des Contours

#### Description
Ce point inclut le développement d'outils pour la détection automatique des bords de l'image et le "snapping" automatique.

#### Fonctionnalités
- **Détection Automatique des Bords**: Utilisation d'algorithmes pour détecter automatiquement les contours des images.
- **Snapping Automatique**: Ajustement automatique des contours pour une précision accrue.

## Organisation du Projet

### Structure des Répertoires

Voici la structure des répertoires utilisée pour la partie extraction du projet :

```
extraction/
│── extraction_main.py
├── automatic_selection/
│   ├── automatic_selection.py
│   └── intelligent_scissors.py
├── contour_adaptation/
│   ├── contour_generation.py
│   └── contour_visualization.py
├── manual_selection/
│   ├── draw_contour.py
│   └── optimisation.py
└── README.md
```

- **automatic_selection**: Dossier contenant les scripts pour la sélection automatique des contours.
  - **automatic_selection.py**: Implémente la détection automatique des bords.
  - **intelligent_scissors.py**: Utilise des algorithmes de sélection intelligente.

- **contour_adaptation**: Dossier pour l'adaptation des contours existants à de nouvelles images.
  - **contour_generation.py**: Génère des contours adaptés.
  - **contour_visualization.py**: Visualise et ajuste les contours.

- **manual_selection**: Dossier pour la sélection manuelle des contours.
  - **draw_contour.py**: Permet de dessiner manuellement des contours et de sauvegarder les résultats en SVG.
  - **optimisation.py**: Améliore la précision des contours dessinés.

