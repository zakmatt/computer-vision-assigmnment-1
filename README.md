# Computer Vision - Bayer and Freeman methods
  
## Example usage:  
`python task_x.py -i mosaic_image -c oryginal_image -o output_directory`  
Where task_x.py is a task defined in a list.  
`-i` is required and it is a  mosaic image  
`-c` is required and it is an oryginal image  
`-o` is not required. It is a directory to which you want to save your results. This directory has to exist.  
  
Example:  
`python task_1.py  -i data/crayons_mosaic.bmp -c data/crayons.jpg`  
# Common methods and concepts
Both scripts use methods from `controllers.py` file  
The common thing between these scripts is that we extract three color channels from a mosaic image following the Bayer Pattern presented below
```
# R G R G ...
# G B G B ...
# R G R G ...
# B G B G ...
# ...
```  
`split_image` method from `controllers.py` file accepts an `image` as an imput value and returns three channels `red, green, blue` as follows.  
  
`interpolate_image` method from `controllers.py` file accepts an `image_channel` and a channel (`'R'`, `'G'` or `'B'` - red, green and blue, respectively). As a result we recive interpolated matrix.  
  
`compate_images` takes two images as an input and returns a root squared difference  
  
`save_image` takes an image, a path to provided directory and an image name as inputs and returns a string saying how the where the image is saved  
  
# Task 1 - Bayer

It is noticable that the result image have problems with places where color changes rapidly or where the intensity of all three channels is big.  
When we run the script `task_1.py` we generate the following files:  
`bayer_image.png` - performance of the algorithm on an image  
`comparizon.png` - comparizon of an image and the oryginal one  

# Task 2 - Freeman

In this task a part from interpolating three channels we filter the 'difference channels' between red and green channels and also between blue and green channels. Later we use median filtering on both results and add a green channel to each of them. After combining the matrices into an image we obtain a smoothen version of Bayer method.  
As a result of a running script we receive three files: `freeman_image.png`, `freeman_oryginal_comparizon.png` and `freeman_bayer_comparizon.png`. The first one shows a performance of the algorithm of an image, the secend one a comparizon between the result image and the original one and the third one is a comparizon between the algorithms.

# Conclusion
1. Bayer method has problems with spots where color changes rapidly  
2. Freeman method results in a more smoothed version of Bayer. This smoothness is noticable especially on the edges(`freeman_oryginal_comparizon.png`)  
3. Freeman method handles better fast color changes and the differences between those methods are presented in `freeman_bayer_comparizon.png`

# Additional information
`requirements.txt` file contains libraries that need to be installed before running the scripts.