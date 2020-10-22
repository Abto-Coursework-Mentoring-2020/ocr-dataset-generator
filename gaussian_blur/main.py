from os import path
import os
from PIL import Image
from gaussian_smoothing import *

filepath = os.getcwd()
for root, dirs, files in os.walk(filepath):
    for file in files:
        if file.split('.')[1] == 'png':
            image = cv2.imread(os.path.join(root, file))
            break
gaussian_blur(image, 15, verbose=True)
