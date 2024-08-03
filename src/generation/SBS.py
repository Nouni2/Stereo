import numpy as np
import cv2 as cv
from utils.utils import resized_window_noPath

def sidebyside_show(left_image, right_image, resize_scale=100):
    '''
    Affiche une image polarisée à partir de deux images, permettant de choisir l'œil droit ou gauche comme point de départ.
    Important !! Il y a un input à donner; écrire "y" ou "n" dans l'invite de commande
    y implique que l'image de droite va en haut
    n implique que l'image de droite va en bas

    Args:
        right_image_path (str): Chemin d'accès à l'image de l'œil droit.
        left_image_path (str): Chemin d'accès à l'image de l'œil gauche.
        resize_scale (int, optional): Facteur de redimensionnement de la fenêtre.
            Par défaut, la valeur est de 100%, recommandé 50% (donc entrer 50 à ce moment là) si l'image est grande.

    Returns:
        None: La fonction n'a pas de valeur de retour, mais elle écrit l'image résultante dans un fichier "NewImTopBottom.png"
            et affiche l'image polarisée dans une fenêtre redimensionnable.

    Raises:
        FileNotFoundError: Si l'un des chemins d'accès aux images spécifiées n'existe pas.
        ValueError: Si la réponse de l'utilisateur n'est pas "y" ou "n".
    '''


    # Load the left and right images
    imgL = left_image
    imgR = right_image

    # Determine the maximum dimensions
    max_height = max(imgL.shape[0], imgR.shape[0])
    max_width = max(imgL.shape[1], imgR.shape[1])


    # Concatenate the images side by side
    concatenated_image = np.concatenate((imgL, imgR), axis=1)

    # Show the concatenated image
    resized_window_noPath(concatenated_image, resize_scale)
    cv.imshow("Resized_Window", concatenated_image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return concatenated_image


