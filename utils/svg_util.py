import xml.etree.ElementTree as ET
from PIL import Image

def points_to_path_d(points):
    # Convert points from polyline format to path 'd' attribute format
    point_list = points.split()
    if not point_list:
        return ""
    # Start the path
    d = f"M {point_list[0]}"
    # Add line commands
    for point in point_list[1:]:
        d += f" L {point}"
    return d

def extract_d_from_svg(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    # Assume that the 'polyline' element contains the 'points' attribute
    for element in root.findall('.//{http://www.w3.org/2000/svg}polyline'):
        # Convert polyline points to path 'd' format
        return points_to_path_d(element.attrib['points'])
    return None

def svg_reformat(image_path, output_path, homography, left_eye_svg, right_eye_svg):
    # Extract image ID and dimensions using PIL
    image_id = image_path.split('/')[-1].split('.')[0]
    image_name = image_path.split("\\")[-1]
    with Image.open(image_path) as img:
        image_width, image_height = img.size

    # Extract the 'd' attribute from SVG files for contours
    left_contour = extract_d_from_svg(left_eye_svg)
    right_contour = extract_d_from_svg(right_eye_svg)

    svg_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
    version="1.1"
    id="{image_id}"
    width="{image_width}"
    height="{image_height}"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:svg="http://www.w3.org/2000/svg">
    <image
        id="image"
        width="{image_width}"
        height="{image_height}"
        homography="{homography}"
        xlink:href="{image_name}" 
    />
    <path
        style="fill:none;fill-opacity:1;stroke:#ff0000;stroke-width:2;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit=4;stroke-dasharray:none;stroke-opacity:1"
        id="lefteye"
        d="{left_contour}"
    />
    <path
        style="fill:none;fill-opacity:1;stroke:#ff0000;stroke-width=2;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit=4;stroke-dasharray:none;stroke-opacity:1"
        id="righteye"
        d="{right_contour}"
    />
</svg>"""

    # Write the SVG content to a file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(svg_template)

    print("SVG written correctly!")
