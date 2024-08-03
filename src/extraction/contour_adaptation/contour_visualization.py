import cv2
import numpy as np
import xml.etree.ElementTree as ET  # For parsing SVG


def read_svg_contour_points(svg_file_path):
    """
    Extracts contour points from an SVG file.
    This function is a placeholder and needs to be adapted based on the SVG structure.
    """
    points = []
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    for polyline in root.findall('.//{http://www.w3.org/2000/svg}polyline'):
        points_str = polyline.attrib['points'].strip()
        points = [tuple(map(float, point.split(','))) for point in points_str.split(' ')]
    return np.array(points, np.int32)


def display_contours_on_image(image_path, svg_files, colors):
    """
    Displays SVG contours on top of an image, each in specified colors.

    Parameters:
    - image_path: Path to the target image.
    - svg_files: List of paths to SVG files.
    - colors: List of colors for each contour.
    """
    # Load the target image
    image = cv2.imread(image_path)

    # For each SVG file, read the contour points and draw them on the image in the specified color
    for svg_file, color in zip(svg_files, colors):
        contour_points = read_svg_contour_points(svg_file)
        cv2.polylines(image, [contour_points], isClosed=True, color=color, thickness=2)

    # Display the image with contours
    cv2.imshow('Image with Contours', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Spécifiez le numéro de l'image
image_number = 5

# Chemin vers l'image d'entrée et le fichier SVG de sortie
input_image_path = rf'D:\Marwane\Documents\Python\Stereo\Version 2\data\input_images\stereo_in{image_number}.jpg'

# SVG files to overlay on the image
svg_files = [
    rf'D:\Marwane\Documents\Python\Stereo\Version 2\data\svg_files\svg_out{image_number}_1.svg',
    rf'D:\Marwane\Documents\Python\Stereo\Version 2\data\svg_files\svg_out{image_number}_2.svg'
]

colors = [(0, 0, 255),#Red (in BGR format)
    (255, 0, 0) # Blue (in BGR format)
         ]


# Call the function to display the image with SVG contours
display_contours_on_image(input_image_path, svg_files,colors)
