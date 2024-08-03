# --------------------------------------------------------------
#                  EXEMPLE D'UTILISATION
# --------------------------------------------------------------
# Dans le dossier input_images, les images sont nommées stereo_in{#Numéro} (stereo_in1, stereo_in2,...).
# Le fichier .svg correspondant suit la même nomenclature : svg_out{#Numéro} (svg_out1, svg_out2,...).

# Importation des fonctions nécessaires depuis le dossier src
from manual_selection.draw_contour import *
from automatic_selection.intelligent_scissors import *
# Spécifiez le numéro de l'image
image_number = 50

# Nombre de contours à dessiner
num_contours = 2

# Chemin vers l'image d'entrée et le fichier SVG de sortie
input_image_path = rf'..\svg_generation\data\input_images\stereo_in{image_number}.jpg'
output_svg_folder = rf'..\svg_generation\data\svg_files'

# Utilisation de la fonction draw_contour avec les variables définies
#draw_contour(input_image_path, output_svg_folder, optimisation_enabled, num_contours, image_number)



import numpy as np
from utils.AffineHomography import *
import xml.etree.ElementTree as ET

######   USEFUL BLOCK FOR GENERATING   ######
######       AND EXPLOITING SVG        ######

from utils.fonction_svg import process_image_svg
from utils.fonction_svg import generation_crop
from utils.svg_util import *

if not os.path.exists("temp"):
    os.makedirs("temp")
    print("Dossier créé :","temp")
else:
    print("Le dossier existe déjà :", "temp")

svg_path = rf"..\svg_generation\data\input_images\svg_final.svg"

svg_reformat(input_image_path,svg_path," ",rf'..\svg_generation\data\svg_files\svg_out{image_number}_1.svg',rf'..\svg_generation\data\svg_files\svg_out{image_number}_2.svg')

workpath = rf"../svg_generation/temp"

# EXTRACT FEATURES FROM SVG FILE

[[w,h],coordL,coordR,coordS,homo,image_path] = process_image_svg((os.path.normpath(svg_path).replace("\\","/")))
coord=[coordL,coordR,coordS]
print(coord)
# GENERATE CROPPED IMAGES
[left_path,right_path,left_mask_path,right_mask_path] = generation_crop(image_path, w, h, rf"..\svg_generation\temp", coord)

# ------------------------écriture de la matrice d'homographie dans le svg------------------------------
left_path
right_path
mat_homo = getAffHomography(left_path, right_path, "Sift")
print(mat_homo)
# Pour transformer la matrice en une chaîne de caractère
homography = ""
for j in [0,1]:
    for i in [0,1,2] :
        homography = homography + str(mat_homo[j][i])+","
homography = homography[:-1]
svg_reformat(input_image_path,svg_path,homography,rf'..\svg_generation\data\svg_files\svg_out{image_number}_1.svg',rf'..\svg_generation\data\svg_files\svg_out{image_number}_2.svg')

