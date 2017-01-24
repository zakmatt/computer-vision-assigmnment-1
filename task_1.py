#!/usr/bin/env python3
import argparse
import cv2
import controllers
import numpy as np

def compare_images(image, comparizon_image):
    result_image = (comparizon_image - image) ** 2
    result_image_sqrt = np.sqrt(result_image)
    result_image_sqrt = np.array(result_image_sqrt, dtype = np.uint8)
    return result_image_sqrt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--input_image",
                        help='Black and white image',
                        required=True)
    parser.add_argument("-c",
                        "--comparison_image",
                        help='Color image to compare the program results',
                        required=True)
    parser.add_argument("-o",
                        "--output_path",
                        help='comparizon result save path',
                        required=False)
    args = parser.parse_args()
    
    input_image_path = args.input_image
    comparizon_image_path = args.comparison_image
    output_path = args.output_path
    image = cv2.imread(input_image_path, 0)
    comparizon_image = cv2.imread(comparizon_image_path)
    
    image_red, image_green, image_blue = controllers.split_image(image)
    image_red = controllers.interpolate_image(image_red, 'R')
    image_green = controllers.interpolate_image(image_green, 'G')
    image_blue = controllers.interpolate_image(image_blue, 'B')
    
    new_image = cv2.merge((image_blue, image_green, image_red))
    comparizon = compare_images(new_image, comparizon_image)
    result = controllers.save_image(comparizon, output_path)
    print(result)