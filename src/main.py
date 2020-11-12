import os
from PIL import Image
from numpy.random import randint
from numpy.random import uniform
import numpy as np
import cv2 as cv
from functools import reduce
from image_ops import *
import pytesseract as tesseract


tesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

output_dir = "../../DegradedImages"

Interpolations = [cv.INTER_AREA, cv.INTER_LINEAR, cv.INTER_CUBIC]

for i in range(10000):
    input_dir = "../../ClearImages/clearTextImage" + str(i) + ".png"
    img = cv.imread(input_dir)
    rows, cols = img.shape[:2]

    degr_pipeline = [GaussianNoiseOperation(mean=uniform(0.5, 0.9), stddev=uniform(0.05, 0.09)),
                     SpeckleOperation(mean=0, stddev=0.001),
                     SpeckleOperation(mean=1, stddev=0),
                     SaltPepperOperation(salt_vs_pepper=uniform(0, 1), amount=uniform(0, 0.02)),
                     RotateOperation(angle=uniform(-30, 30), center=(cols//2, rows//2)),
                     GaussianBlurOperation(radius=randint(0, 2)),
                     BoxBlurOperation(radius=randint(0, 2)),
                     MinFilterOperation(radius=int(randint(1, 3) * 1.5)),
                     MaxFilterOperation(radius=int(randint(1, 3) * 1.5)),
                     ResizeOperation(width=randint(cols//2, cols * 2), height=randint(rows//2, rows * 2), interpolation=Interpolations[randint(0, 3)])
                     ]

    degraded = reduce(lambda image, op: op(image), degr_pipeline, img)
    # outp_text = tesseract.image_to_string(degraded)
    # print(outp_text)
    Image.fromarray(np.uint8(degraded)).save(os.path.join(output_dir, f'degradedImage{i}.png'))
