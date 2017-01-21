#!/usr/bin/env python3
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
PATH = 'data/'

file_path = os.path.join(PATH, 'oldwell_mosaic.png')
img = cv2.imread(file_path, 0)
w, h = img.shape
new_image = np.zeros((w, h, 3), dtype = np.uint8)
new_image_2 = np.zeros((w, h, 3), dtype = np.uint8)

# G R G R ...
# B G B G ...
# G R G R ...
# ...


# Green
new_image[1::2,1::2,1] = img[1::2,1::2]
new_image_green = new_image[:, :, 1]
new_image[::2, ::2, 1] = img[::2, ::2]
new_image_green = new_image[:, :, 1]

# Blue
new_image[1::2,::2,0] = img[1::2,::2]
new_image_blue = new_image[:, :, 0]

# Red
new_image[::2, 1::2, 2] = img[::2, 1::2]
new_image_red = new_image[:, :, 2]

kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])/4
kernel_2 = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]])/4
new_image_green = new_image_green + cv2.filter2D(new_image_green, -1, kernel)

# Interpolation for the blue at the missing points
# First, calculate the missing blue pixels at the red location

# kernel_blue_red = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]])/4
image_blue = cv2.filter2D(new_image_blue, -1, kernel_2)
# Second, calculate the missing blue pixels at the green locations
# by averaging the four neighouring blue pixels
image_blue_2 = cv2.filter2D(new_image_blue + image_blue, -1, kernel)
new_image_blue += image_blue + image_blue_2

# Interpolation for the red at the missing points
# First, calculate the missing red pixels at the blue location

# kernel_red_blue = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]])/4
image_red = cv2.filter2D(new_image_red, -1, kernel_2)

# Second, calculate the missing red pixels at the green locations  

image_red_2 = cv2.filter2D(new_image_red + image_red, -1, kernel)
new_image_red += image_red + image_red_2

new_img = cv2.merge((new_image_green,new_image_blue,new_image_red))
plt.imshow(new_img)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
cv2.imwrite('output.jpg', new_img)

img_dem = cv2.imread(os.path.join(PATH, 'oldwell.jpg'))
result_img = (img_dem - new_img) ** 2
plt.imshow(result_img)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
result_img_sqrt = np.sqrt(result_img)
result_img_sqrt = np.array(result_img_sqrt, dtype = np.uint8)
plt.imshow(result_img_sqrt)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()