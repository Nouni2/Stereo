import cv2
import numpy as np
import svgwrite


src = cv2.imread("1024-533-MAX.jpg")  # Replace with your image path
if src is None:
    print("Error loading image.")
    exit()

# Window setup
cv2.namedWindow('canvasOutput', cv2.WINDOW_NORMAL)

roi_points = []


def mouse_callback(event, x, y, flags, param):
    global roi_points, src
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_points.append((x, y))
        # Only draw points to show the ROI, not the connecting lines
        cv2.circle(src, (x, y), 5, (0, 255, 0), -1)


cv2.setMouseCallback('canvasOutput', mouse_callback)

while True:
    cv2.imshow('canvasOutput', src)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Quit
        break
    elif key == ord('c') and len(roi_points) > 2:  # Close the polygon manually
        break

# Creating a mask for the ROI
mask = np.zeros(src.shape[:2], dtype=np.uint8)
cv2.fillPoly(mask, [np.array(roi_points, dtype=np.int32)], 255)

# Apply the mask to get the isolated ROI
isolated_roi = cv2.bitwise_and(src, src, mask=mask)

# Detect edges within the ROI
gray_roi = cv2.cvtColor(isolated_roi, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_roi, 100, 200)

# Find contours based on edges
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Optionally, draw detected contours for visualization
for contour in contours:
    cv2.drawContours(src, [contour], -1, (0, 0, 255), 2)

# Compute the convex hull of the detected contours
if contours:
    all_contour_points = np.concatenate(contours)
    convex_hull = cv2.convexHull(all_contour_points)
    cv2.drawContours(src, [convex_hull], -1, (255, 0, 0), 3)  # Draw convex hull in blue

cv2.imshow('Detected Edges and Convex Hull within ROI', src)

cv2.imwrite('image_with_convex_hull.png', src)
# Create a blank image with the same dimensions as the original
blank_image = np.zeros_like(src)

# Draw the convex hull on the blank image
# Use color (255, 0, 0) for blue and thickness 3
cv2.drawContours(blank_image, [convex_hull], -1, (255, 0, 0), 3)

# Save the image with just the convex hull
cv2.imwrite('convex_hull_only.png', blank_image)
# Prepare hull points for SVG. Convert each point in the convex hull to a tuple (x, y)
hull_points_for_svg = [(int(point[0][0]), int(point[0][1])) for point in convex_hull]

# Create an SVG drawing
dwg = svgwrite.Drawing('convex_hull_only.svg', profile='tiny')

# Draw the convex hull as a polygon on the SVG
dwg.add(dwg.polygon(points=hull_points_for_svg, fill='none', stroke=svgwrite.rgb(0, 0, 255, '%'), stroke_width=2))

# Save the SVG file
dwg.save()

print("Convex hull saved as SVG 'convex_hull_only.svg'")
cv2.waitKey(0)
cv2.destroyAllWindows()
