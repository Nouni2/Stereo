import numpy as np
import cv2 as cv

def anaglyph_show(left_image, right_image, extension,resize_scale=100):
    '''
    Displays an anaglyph image generated from two left and right images.

    Args:
        left_image (str): Path to the left image file.
        right_image (str): Path to the right image file.
        extension (str): type of image (ie. png, jpg, tiff)
        resize_scale (int, optional): Resizing factor for the display window.
            Default is 100%, recommended to use 50% (enter 50) if the image is large.

    Returns:
        None: The function has no return value. It writes the resulting anaglyph image without offset to a file named "anaglyph.png"
            and displays the anaglyph image in a resizable window.

    Raises:
        FileNotFoundError: If either of the specified image paths does not exist.

    '''
    # Load the images
    img1 = right_image
    img2 = left_image

    # Apply color filters based on the file extensions
    if extension == 'jpg':
        img1_filtered = img1.copy()
        img1_filtered[:, :, 0] = 0  # Red filter applied to the right image
        img1_filtered[:, :, 1] = 0  # Red filter applied to the right image
        img2_filtered = img2.copy()
        img2_filtered[:, :, 2] = 0  # Blue filter applied to the left image
    elif extension == 'png' or extension == 'tiff':
        img1_filtered = img1.copy()
        img1_filtered[:, :, 1:] = 0  # Red filter applied to the right image (green and blue channels set to 0)
        img2_filtered = img2.copy()
        img2_filtered[:, :, 0] = 0  # Blue filter applied to the left image (red channel set to 0)
    else:
        print("Images of type {} are not supported. Please use JPG, PNG, or TIFF.".format(extension))
        return

    # Ensure both images have the same dimensions
    if img1_filtered.shape != img2_filtered.shape:
        print("DIMENSION MISMATCH, IMPOSSIBLE TO CREATE ANAGLYPH")
        return

    max_height, max_width, _ = img1_filtered.shape

    # Initialize the horizontal offset
    offset_x = 0
    # while True:
    #     padding_left = max(0, offset_x)
    #     padding_right = max(0, -offset_x)
    #
    #     # Create anaglyph image by combining left and right images with color filtering
    #     anaglyph = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    #     if extension == 'jpg': #bgr channels
    #         anaglyph[:, padding_left:max_width + padding_right, 0] = img2_filtered[:, padding_right:max_width + padding_left, 0]  # Blue channel from left image
    #         anaglyph[:, padding_left:max_width + padding_right, 1] = img2_filtered[:, padding_right:max_width + padding_left, 1]  # Green channel from left image
    #         anaglyph[:, :, 2] = img1_filtered[:, :, 2]  # Red channel from right image
    #
    #     elif extension == 'png' or extension == 'tiff': #rgb channels
    #         anaglyph[:, padding_left:max_width + padding_right, 0] = img2_filtered[:, padding_right:max_width + padding_left, 2]  # Blue channel from left image
    #         anaglyph[:, padding_left:max_width + padding_right, 1] = img2_filtered[:, padding_right:max_width + padding_left, 1]  # Green channel from left image
    #         anaglyph[:, :, 2] = img1_filtered[:, :, 0]  # Red channel from right image
    #     # Resize the window and display the image
    #     resized = cv.resize(anaglyph, (0, 0), fx=resize_scale/100, fy=resize_scale/100)
    #     cv.imshow("Resized_Window", resized)
    #
    #     # Wait for key press
    #     key = cv.waitKey(0)
    #
    #     # Adjust horizontal offset based on key press (up and down arrow keys)
    #     if key == 27:  # ESC key to exit
    #         break
    #     elif key == 43:  # Up arrow key (increase horizontal offset)
    #         offset_x += 10
    #     elif key == 45:  # Down arrow key (decrease horizontal offset)
    #         offset_x -= 10


    # Reset offset and calculate padding
    offset_x = 0
    padding_left = max(0, offset_x)
    padding_right = max(0, -offset_x)

    # Create the final anaglyph image without user-defined horizontal offset
    final_anaglyph = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    if extension == 'jpg': #bgr channels
        final_anaglyph[:, padding_left:max_width + padding_right, 0] = img2_filtered[:, padding_right:max_width + padding_left, 0]  # Blue channel from left image
        final_anaglyph[:, padding_left:max_width + padding_right, 1] = img2_filtered[:, padding_right:max_width + padding_left, 1]  # Green channel from left image
        final_anaglyph[:, :, 2] = img1_filtered[:, :, 2]  # Red channel from right image

    elif extension == 'png' or extension == 'tiff': #rgb channels
        final_anaglyph[:, padding_left:max_width + padding_right, 0] = img2_filtered[:, padding_right:max_width + padding_left, 2]  # Blue channel from left image
        final_anaglyph[:, padding_left:max_width + padding_right, 1] = img2_filtered[:, padding_right:max_width + padding_left, 1]  # Green channel from left image
        final_anaglyph[:, :, 2] = img1_filtered[:, :, 0]  # Red channel from right image

    # Resize and save the anaglyph image
    resized_final = cv.resize(final_anaglyph, (0, 0), fx=resize_scale / 100, fy=resize_scale / 100)
    cv.imshow("Resized_Window", resized_final)
    cv.imwrite('anaglyph.png', resized_final)

    # Close all OpenCV windows
    cv.waitKey(0)
    cv.destroyAllWindows()

