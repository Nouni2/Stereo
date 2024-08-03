import cv2
import svgwrite
import numpy as np
import json
from optimisation import douglas_peucker

# Paramètres
precision = 100
optimisation_enabled = True
epsilon = 0.05

def draw_contour(input_image_path, output_svg_folder, optimisation_enabled ,num_contours,image_number):
    """
    Fonction permettant à l'utilisateur de dessiner manuellement un ou plusieurs contours sur une image.

    Parameters:
    - image_path (str): Chemin vers l'image sur laquelle l'utilisateur dessinera le contour.
    - output_svg_folder (str): Chemin du dossier pour sauvegarder les fichiers SVG contenant les contours.
    - optimisation_enabled (bool): Indique si l'optimisation des contours est activée.
    - num_contours (int): Nombre de contours à dessiner.
    - image_number (int) : Numéro de l'image.

    Returns:
    - None
    """

    # Charger l'image
    input_image = cv2.imread(input_image_path)

    # Copier l'image pour afficher les contours tracés
    image_with_contours = input_image.copy()

    # Liste de dictionnaires, chaque dictionnaire représente un contour
    contours = []

    # Mode par défaut (ligne)
    draw_mode = 'line'

    # Compteur pour suivre le nombre de clics en mode spline
    spline_click_count = 0

    # Indice du contour actuel
    current_contour = 0

    # Compteur pour suivre le nombre de contours fermés
    closed_contours_count = 0

    # Fonction de rappel pour la souris
    def draw_callback(event, x, y, flags, param):
        nonlocal contours, image_with_contours, spline_click_count, draw_mode, current_contour

        if event == cv2.EVENT_LBUTTONDOWN:
            # Ajouter le point au contour actuel
            contours[current_contour]['temporary_points'].append((x, y))

            # Ajouter le point de couleur différente à la liste des points dessinés
            contours[current_contour]['drawn_points'].append((x, y, contours[current_contour]['color']))

            # Traiter la liste de points
            process_points()

    def process_points():
        """
        Fonction de traitement des points ajoutés lors du dessin du contour.

        Returns:
        - None
        """
        nonlocal contours, image_with_contours, spline_click_count, current_contour

        # Si le mode est ligne et len(temporary_points) > 1, relier les deux derniers points
        if draw_mode == 'line' and len(contours[current_contour]['temporary_points']) > 1:
            points = np.array(contours[current_contour]['temporary_points'][-2:])
            line_start = tuple(points[0].astype(int))
            line_end = tuple(points[1].astype(int))

            # Dessiner une ligne entre les deux points
            cv2.line(image_with_contours, line_start, line_end, color=contours[current_contour]['color'], thickness=2)

            # Ajouter les deux points à la liste globale
            # Create a segment with these points
            contours[current_contour]['segments'].append({
                'points': contours[current_contour]['temporary_points'].copy()  # Copy the points
            })
            contours[current_contour]['contour_points'].extend(points)
            contours[current_contour]['temporary_points'].pop(0)
        # Si le mode est spline
        elif draw_mode == 'spline':
            # Incrémenter le compteur de clics en mode spline
            spline_click_count += 1

            # Si trois points ont été ajoutés (deux nouveaux clics)
            if spline_click_count == 2 and len(contours[current_contour]['temporary_points']) > 2:
                # Tracer la spline entre les trois derniers points
                points = np.array(contours[current_contour]['temporary_points'][-3:])
                t = np.linspace(0, 1, precision)
                curve_points = np.array([(1 - t) ** 2 * points[0, i] + 2 * (1 - t) * t * points[1, i] +
                                         t ** 2 * points[2, i] for i in range(2)]).T
                cv2.polylines(image_with_contours, [curve_points.astype(int)], isClosed=False,
                              color=contours[current_contour]['color'], thickness=2)

                # Create a segment with these points
                contours[current_contour]['segments'].append({
                    'points': contours[current_contour]['temporary_points'].copy()  # Copy the points
                })
                contours[current_contour]['contour_points'].extend(curve_points)
                # Réinitialiser le compteur
                contours[current_contour]['temporary_points'].pop(0)
                spline_click_count = 0

        # Afficher l'image mise à jour
        cv2.imshow("Manual Selection", image_with_contours)

        # Afficher tous les points dessinés
        for point in contours[current_contour]['drawn_points']:
            cv2.circle(image_with_contours, tuple(map(int, point[:2])), 3, point[2], -1)

    # Initialiser la liste de contours
    for i in range(num_contours):
        color = (255, 0, 0) if i == 0 else (0, 0, 255)  # Bleu pour le premier contour, rouge pour les suivants
        contours.append({
            'contour_points': [],
            'segments' : [],
            'temporary_points': [],
            'drawn_points': [],
            'color': color,
            'draw_mode': 'line',
            'spline_click_count': 0
        })

    # Afficher l'image
    cv2.imshow("Manual Selection", image_with_contours)
    # Créer une fenêtre pour l'image
    cv2.namedWindow("Manual Selection")

    # Associer la fonction de rappel à la fenêtre
    cv2.setMouseCallback("Manual Selection", draw_callback)

    print("Instructions:\n  - Cliquez pour ajouter un point au contour.")
    print("  - Appuyez sur 'c' pour terminer le dessin du contour actuel.")
    print("  - Appuyez sur 'l' pour dessiner des lignes.")
    print("  - Appuyez sur 's' pour dessiner des splines.")


    while True:
        # Afficher l'image mise à jour
        cv2.imshow("Manual Selection", image_with_contours)




        # Attendre une touche et traiter si nécessaire
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Sauvegarder le contour actuel dans un fichier SVG
            output_svg_path = f"{output_svg_folder}/svg_out{image_number}_{current_contour + 1}.svg"
            print(f"Nombre de points du contour {current_contour + 1}: {len(contours[current_contour]['contour_points'])}")
            save_points_to_svg(output_svg_path, contours[current_contour]['contour_points'], contours[current_contour]['color'])

            # Sauvegarder les points clés dans un fichier JSON
            contour_data = {
                "id": current_contour + 1,
                "precision": precision,
                "segments": []
            }

            # Iterate over the segments of the current contour
            for segment in contours[current_contour]['segments']:
                # Each segment contains its points
                segment_data = {
                    "points": segment['points']
                }
                contour_data["segments"].append(segment_data)

            # Define the path for the JSON file corresponding to the current contour
            json_file_path = f"{output_svg_folder}/contour_segments_{image_number}_{current_contour + 1}.json"

            # Write the contour data to the JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(contour_data, json_file, indent=4)

            print(f"Key points for contour {current_contour + 1} saved to {json_file_path}")

            # Réinitialiser les points du contour actuel
            contours[current_contour]['contour_points'] = []
            contours[current_contour]['temporary_points'] = []
            contours[current_contour]['drawn_points'] = []
            contours[current_contour]['draw_mode'] = 'line'
            contours[current_contour]['spline_click_count'] = 0


            # Changer de contour
            current_contour = (current_contour + 1) % num_contours

            # Incrémenter le compteur de contours fermés
            closed_contours_count += 1

            # Si tous les contours sont fermés, sortir de la boucle
            if closed_contours_count == num_contours:
                break

        elif key == ord('l'):
            draw_mode = 'line'
            contours[current_contour]['draw_mode'] = 'line'
            print("Mode de dessin: lignes")
        elif key == ord('s'):
            draw_mode = 'spline'
            contours[current_contour]['draw_mode'] = 'spline'
            print("Mode de dessin: splines")

    # Fermer la fenêtre après le dessin
    cv2.destroyAllWindows()



def save_points_to_svg(output_svg_path, contour_points, color):
    """
    Fonction sauvegardant la liste globale des points du contour dans un fichier SVG.

    Parameters:
    - output_svg_path (str): Chemin du fichier SVG de sortie.
    - contour_points (list): Liste globale des points du contour.
    - color (tuple): Couleur du contour au format BGR.

    Returns:
    - None
    """
    # Créer un objet SVG
    svg_object = svgwrite.Drawing(output_svg_path, profile='tiny')

    # Convertir la couleur de BGR à RGB
    rgb_color = tuple(reversed(color))

    # Ajouter la liste globale des points à l'objet SVG avec la couleur du contour
    svg_object.add(svg_object.polyline(points=[(str(x), str(y)) for x, y in contour_points], fill='none',
                                       stroke=svgwrite.rgb(*rgb_color, '%')))

    # Sauvegarder le fichier SVG
    svg_object.save()
    print(f"Le contour a été enregistré dans {output_svg_path}")


