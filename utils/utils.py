import cv2 as cv
import os
def resized_window(image_path, scale_factor):
    img_base = cv.imread(image_path)
    height = int(img_base.shape[1] * scale_factor / 100)
    width = int(img_base.shape[0] * scale_factor / 100)

    cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
    # les dimensions sont inversées entre la commande .shape et la commande .resizeWindow.
    cv.resizeWindow("Resized_Window", height, width)
    return 0

def resized_window_noPath(image, scale_factor):
    img_base = image
    height = int(img_base.shape[1] * scale_factor / 100)
    width = int(img_base.shape[0] * scale_factor / 100)

    cv.namedWindow("Resized_Window", cv.WINDOW_NORMAL)
    # les dimensions sont inversées entre la commande .shape et la commande .resizeWindow.
    cv.resizeWindow("Resized_Window", height, width)
    return 0


