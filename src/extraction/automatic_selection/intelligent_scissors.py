import cv2
import numpy as np
import svgwrite

# Load the image
src = cv2.imread("2643-1024.jpg")
image_copy = src.copy()

# Create a window to display the image
cv2.namedWindow('canvasOutput', cv2.WINDOW_NORMAL)
cv2.imshow('canvasOutput', src)

# Variables to store the start and end points of the line
start_point = None

# List to store the points of the red curve
red_curve_points = []

# Mouse click event handler function
def mouse_callback(event, x, y, flags, param):
    global start_point, red_curve_points

    if event == cv2.EVENT_LBUTTONDOWN:
        if x < src.shape[1] and y < src.shape[0]:
            if start_point is None:
                start_point = (x, y)
            else:
                end_point = (x, y)
                # Find a contour between start and end points
                color = (0, 0, 255)  # Red (B, G, R)
                thickness = 2

                # Convert the image to grayscale
                gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

                # Perform edge detection
                edges = cv2.Canny(gray, 100, 200)

                # Find contours in the edge-detected image
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Find the contour closest to the start point
                min_distance = float('inf')
                closest_contour = None
                for contour in contours:
                    for point in contour:
                        distance = np.sqrt((point[0][0] - start_point[0]) ** 2 + (point[0][1] - start_point[1]) ** 2)
                        if distance < min_distance:
                            min_distance = distance
                            closest_contour = contour

                if closest_contour is not None:
                    # Draw the red line on the image
                    cv2.polylines(image_copy, [closest_contour], isClosed=False, color=color, thickness=thickness)
                    # Store the points of the contour
                    red_curve_points.extend([tuple(point[0]) for point in closest_contour])

                start_point = None

# Set the mouse callback
cv2.setMouseCallback('canvasOutput', mouse_callback)

# Function to update the display
def update_display():
    cv2.imshow('canvasOutput', image_copy)

# Main loop
while True:
    update_display()
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Create an SVG file with the red curve
dwg = svgwrite.Drawing('red_curve.svg', profile='tiny', size=(src.shape[1], src.shape[0]))
path_data: str = "M {} {} L".format(*red_curve_points[0])
path_data += " ".join(["{} {}".format(x, y) for x, y in red_curve_points[1:]])
path = svgwrite.path.Path(d=path_data, stroke=svgwrite.rgb(255, 0, 0, '%'), stroke_width=10, fill='none')
dwg.add(path)

# Find the convex hull of red curve points
red_curve_np = np.array(red_curve_points)
hull = cv2.convexHull(red_curve_np, clockwise=True, returnPoints=True)
hull_points = [(int(point[0][0]), int(point[0][1])) for point in hull]

# Draw the convex hull on the image
cv2.polylines(image_copy, [np.array(hull_points)], isClosed=True, color=(0, 255, 0), thickness=10)

# Save the image with the red contours and convex hull
cv2.imwrite('image_with_contours_and_convex_hull.png', image_copy)

# Save just the convex hull as a separate image
convex_hull_image = np.zeros_like(image_copy)
cv2.polylines(convex_hull_image, [np.array(hull_points)], isClosed=True, color=(255, 255, 255), thickness=10)
cv2.imwrite('convex_hull_image.png', convex_hull_image)

# Load the image
src = cv2.imread("stopping_function_with_white_border_in_blank.png")

# Convert the image to grayscale and find edges
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Prepare an SVG drawing
dwg = svgwrite.Drawing('drawing.svg', profile='tiny', size=(src.shape[1], src.shape[0]))

# Add contours as red paths
for contour in contours:
    points = " ".join(["{},{}".format(point[0][0], point[0][1]) for point in contour])
    dwg.add(dwg.path(d="M " + points, stroke="red", fill="none"))

# Assuming `red_curve_np` and `hull_points` are computed as in your script
# Add the convex hull as a green path
if len(hull_points) > 0:
    hull_points_str = " ".join(["{},{}".format(point[0], point[1]) for point in hull_points])
    dwg.add(dwg.path(d="M " + hull_points_str + " Z", stroke="green", fill="none"))

# Save the SVG file
dwg.save()
# Release resources
cv2.destroyAllWindows()
