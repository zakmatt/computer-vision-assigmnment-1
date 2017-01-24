#!/usr/bin/env python3
import argparse
import cv2
import controllers
import numpy as np

def bayer(red_ch, green_ch, blue_ch):
    return cv2.merge((blue_ch, green_ch, red_ch))

def freeman(red_ch, green_ch, blue_ch):
    
    # type float 32 allows to handle negative values
    red_ch = np.array(red_ch, dtype = np.float32)
    green_ch = np.array(green_ch, dtype = np.float32)
    blue_ch = np.array(blue_ch, dtype = np.float32)
    
    # Subtract channels
    new_RG = red_ch - green_ch
    new_BG = blue_ch - green_ch
    # use median filtering
    new_RG = cv2.medianBlur(new_RG, 3)
    new_BG = cv2.medianBlur(new_BG, 3)
    
    new_RG += green_ch
    new_BG += green_ch
    
    return cv2.merge((new_BG, green_ch, new_RG))

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
    
    freeman_result = (freeman(image_red, image_green, image_blue)).astype(int)
    bayer_result = (bayer(image_red, image_green, image_blue)).astype(int)
    result = controllers.save_image(freeman_result, output_path, 'freeman_image.png')
    print(result)
    
    freeman_org_comparizon = controllers.compare_images(freeman_result, 
                                                        comparizon_image)
    result = controllers.save_image(freeman_org_comparizon, 
                                    output_path, 
                                    'freeman_oryginal_comparizon.png')
    print(result)
    
    freeman_bayer_comparizon = controllers.compare_images(freeman_result,
                                                          bayer_result)
    result = controllers.save_image(freeman_bayer_comparizon,
                                    output_path,
                                    'freeman_bayer_comparizon.png')
    print(result)