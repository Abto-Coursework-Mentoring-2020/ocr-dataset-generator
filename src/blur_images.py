import PIL
from PIL import Image
from PIL import ImageFilter
from os import path
import os
import numpy as np
import argparse

#input_dir = r'C:/Users/Ksy/Desktop/test'
#filename = "text_image1.png"
#filter = "gaussian"
#radius = 2

def blur_images(input_dir: str, filename: str, filter: str, radius: int):

    standart_path = os.path.normpath(input_dir)
    for root, dirs, files in os.walk(standart_path):
        for file in files:
            if (file == filename):
                my_image = Image.open(file)

    my_image.show()

    numpydata = np.asarray(my_image)
    #print(numpydata)

    #blur image
    if (filter == "gaussian"):
        result_image = my_image.filter(ImageFilter.GaussianBlur(radius))

    if (filter == "box"):
        result_image = my_image.filter(ImageFilter.BoxBlur(radius))

    if (filter == "min"):
        result_image = my_image.filter(ImageFilter.MinFilter(radius))

    if (filter == "max"):
        result_image = my_image.filter(ImageFilter.MaxFilter(radius))

    if (filter == "median"):
        result_image = my_image.filter(ImageFilter.MedianFilter(radius))


    output_dir = os.path.join(standart_path, 'blurred_images')
    output_path = os.path.join(output_dir,os.path.splitext(filename)[0] + "_blurred.png" )

    newfilename = os.path.splitext(filename)[0] + "_blurred.png"
    #result_image.save(os.path.splitext(filename)[0] + "_blurred.png")
    result_image.save(output_path)


def gaussian_blur(image: np.array, radius=1) -> np.array:
    blured = PIL.Image.fromarray(np.uint8(image)).filter(ImageFilter.GaussianBlur(radius))
    return np.asarray(blured)


def box_blur(image: np.array, radius=1) -> np.array:
    blured = PIL.Image.fromarray(np.uint8(image)).filter(ImageFilter.BoxBlur(radius))
    return np.asarray(blured)


def min_filter(image: np.array, radius=3) -> np.array:
    blured = PIL.Image.fromarray(np.uint8(image)).filter(ImageFilter.MinFilter(radius))
    return np.asarray(blured)


def max_filter(image: np.array, radius=3) -> np.array:
    blured = PIL.Image.fromarray(np.uint8(image)).filter(ImageFilter.MaxFilter(radius))
    return np.asarray(blured)


def median_filter(image: np.array, radius=3) -> np.array:
    blured = PIL.Image.fromarray(np.uint8(image)).filter(ImageFilter.MedianFilter(radius))
    return np.asarray(blured)
