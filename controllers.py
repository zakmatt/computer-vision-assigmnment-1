#!/usr/bin/env python3
import cv2
import numpy as np
import os

def split_image(image):
    w, h = image.shape
    new_image = np.zeros((w, h, 3), dtype = np.uint8)
    
    # R G R G ...
    # G B G B ...
    # R G R R ...
    # ...
    
    # Green
    new_image[1::2, ::2, 1] = image[1::2,::2]
    new_image[::2, 1::2, 1] = image[::2, 1::2]
    new_image_green = new_image[:, :, 1]
    
    # Blue
    new_image[1::2,1::2,2] = image[1::2,1::2]
    new_image_blue = new_image[:, :, 2]
    
    # Red
    new_image[::2, ::2, 0] = image[::2, ::2]
    new_image_red = new_image[:, :, 0]
    
    return new_image_red, new_image_green, new_image_blue

def interpolate_image(image, channel):
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / 4
    kernel_2 = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]]) / 4
    
    if channel == 'G':
        image = image + cv2.filter2D(image, -1, kernel)
    elif channel == 'R':
        # Interpolation for the red at the missing points
        # First, calculate the missing red pixels at the blue location
        
        # kernel_red_blue = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]])/4
        image_red = cv2.filter2D(image, -1, kernel_2)
        
        # Second, calculate the missing red pixels at the green locations  
        image_red_2 = cv2.filter2D(image + image_red, -1, kernel)
        image += image_red + image_red_2
    elif channel == 'B':
        # Interpolation for the blue at the missing points
        # First, calculate the missing blue pixels at the red location
        
        # kernel_blue_red = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]])/4
        image_blue = cv2.filter2D(image, -1, kernel_2)
        # Second, calculate the missing blue pixels at the green locations
        # by averaging the four neighouring blue pixels
        image_blue_2 = cv2.filter2D(image + image_blue, -1, kernel)
        image += image_blue + image_blue_2
    else:
        return 0
    
    return image

def calculate_difference(oryginal, new_image):
    if oryginal.shape != new_image.shape:
        print('Images have to be the same size!')
        return 0
        
    result_img = (oryginal - new_image) ** 2
    result_img_sqrt = np.sqrt(result_img)
    result_img_sqrt = np.array(result_img_sqrt, dtype = np.uint8)
    return result_img_sqrt

def save_image(image, path):
    if path is None:
        path = ''
    file_name = os.path.join(path, 'comparizon.png')
    cv2.imwrite(file_name, image)
    return "Saved as: %s" % file_name
    