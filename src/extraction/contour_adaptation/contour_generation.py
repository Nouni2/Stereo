import json
import svgwrite
import numpy as np

def generate_curve_points(points, precision):
    # Assume points is a list of three control points for a quadratic Bezier curve
    t = np.linspace(0, 1, precision)
    curve_points = np.array([(1 - t) ** 2 * points[0][i] + 2 * (1 - t) * t * points[1][i] + t ** 2 * points[2][i] for i in range(2)]).T
    return curve_points

def construct_svg_from_json(json_file_path, svg_file_path, precision=100):
    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Create a new SVG drawing
    dwg = svgwrite.Drawing(svg_file_path, profile='tiny')

    for segment in data['segments']:
        points = segment['points']

        if len(points) == 2:  # For a line, just draw the end points
            for point in points:
                dwg.add(dwg.circle(center=point, r=1, fill='black'))  # Draw end points as circles

        elif len(points) > 2:  # For a spline, generate and draw each curve point
            curve_points = generate_curve_points(points, precision)
            for point in curve_points:
                dwg.add(dwg.circle(center=(point[0], point[1]), r=1, fill='red'))  # Draw curve points as circles

    # Save the SVG file
    dwg.save()

image_number = 5
current_contour = 1
output_svg_folder = rf'D:\Marwane\Documents\Python\Stereo\Version 2\data\svg_files'



# Example usage
json_file_path = f"{output_svg_folder}/contour_segments_{image_number}_{current_contour}.json"
svg_file_path = f"{output_svg_folder}/generated_svg_{image_number}_{current_contour}.svg"
construct_svg_from_json(json_file_path, svg_file_path)
