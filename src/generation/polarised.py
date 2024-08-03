import numpy as np
import cv2 as cv

from utils.utils import resized_window_noPath

def polarised_show(left_image, right_image, resize_scale=100):
    '''
    Affiche une image polarisée à partir de deux images, permettant de choisir l'œil droit ou gauche comme point de départ.
    Important !! Il y a un input à donner; écrire "y" ou "n" dans l'invite de commande
    y impliquera que l'image de droite ira en haut
    n impliquera que l'image de droite ira en bas

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

    if left_image.size==0 :
        print("Left Image is None")
        return 1
    if right_image.size==0 :
        print("Right Image is None")
        return 1
    
    a = input("Right eye = Top part then type y\nRight eye = Bottom part then type n\n\t")
    if a == "y":
        imgTop = right_image
        imgBottom = left_image
    elif a == "n":
        imgTop = left_image
        imgBottom = right_image
    else:
        print("\nplease answer with only y or n")

    heightTop, widthTop = imgTop.shape[:2]
    dimTop = (widthTop, heightTop // 2)  # New height is half of the original height
    resizedTop = cv.resize(imgTop, dimTop, interpolation=cv.INTER_AREA)

    # Resize the bottom image
    heightBottom, widthBottom = imgBottom.shape[:2]
    dimBottom = (widthBottom, heightBottom // 2)  # New height is half of the original height
    resizedBottom = cv.resize(imgBottom, dimBottom, interpolation=cv.INTER_AREA)

    # Create a new image to display both resized images
    totalHeight = resizedTop.shape[0] + resizedBottom.shape[0]
    maxWidth = max(resizedTop.shape[1], resizedBottom.shape[1])
    NewImTopBottom = np.zeros((totalHeight, maxWidth, 3), dtype=np.uint8)

    # Fill the top part of the new image with the resized top image
    NewImTopBottom[:resizedTop.shape[0], :resizedTop.shape[1]] = resizedTop

    # Fill the bottom part of the new image with the resized bottom image
    NewImTopBottom[resizedTop.shape[0]:, :resizedBottom.shape[1]] = resizedBottom

    resized_window_noPath(NewImTopBottom, resize_scale)
    cv.imwrite("top_bottom.png",NewImTopBottom)
    cv.imshow("Resized_Window", NewImTopBottom)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return NewImTopBottom


