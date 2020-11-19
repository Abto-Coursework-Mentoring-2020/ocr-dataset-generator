from PIL import Image
from numpy.random import randint
from numpy.random import uniform
import numpy as np
import cv2 as cv
from functools import reduce
from image_ops import *
import pytesseract as tesseract
import json
from metrics import edit_distance
from utils import scale_point2d, rotate_point2d_in_not_cutted_img


def take_clear_image_text(input_dir, clear_image_name):
    res = ''
    with open(input_dir) as json_file:
        file = json.load(json_file)
        clear_image_data = file[clear_image_name]

        for word_data in clear_image_data:
            word = str(word_data['word'])
            if word.find('\n') == -1:
                res += word + ' '
            else:
                res += word
    res += '\f'
    return res


def take_degraded_image_bboxes(input_dir, clear_image_name):
    words = []
    with open(input_dir) as json_file:
        file = json.load(json_file)
        clear_image_data = file[clear_image_name]

        for word_data in clear_image_data:
            word = word_data['word']
            orig_bbox = word_data['coord']
            new_bbox = []
            for point in orig_bbox:
                scaled_point = scale_point2d(src_point=point, original_size=orig_size, target_size=target_size)
                new_point = rotate_point2d_in_not_cutted_img(src_point=scaled_point,
                                                             angle=angle,
                                                             center=(target_width // 2, target_height // 2),
                                                             img_size=target_size)
                new_bbox.append(new_point)
            words.append({'word': word, 'coord': new_bbox})
    return words


tesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

output_dir = "../../DegradedImages"

Interpolations = [cv.INTER_AREA, cv.INTER_LINEAR, cv.INTER_CUBIC]

toJson = {}

for i in range(10000):
    clear_image_name = f'clear_image{i}.png'
    clear_image = cv.imread(f'../../ClearImages/' + clear_image_name)
    new_data = []

    orig_height, orig_width = clear_image.shape[:2]
    orig_size = orig_width, orig_height
    target_size = target_width, target_height = randint(orig_width // 1.5, orig_width * 1.5), randint(orig_height // 1.5, orig_height * 1.5)

    degr_pipeline = [GaussianNoiseOperation(mean=uniform(0.5, 0.9), stddev=uniform(0.05, 0.09)),
                     SpeckleOperation(mean=0, stddev=0.001),
                     SpeckleOperation(mean=1, stddev=0),
                     SaltPepperOperation(salt_vs_pepper=uniform(0, 1), amount=uniform(0, 0.02)),
                     # RotateOperation(angle=uniform(-5, 5), center=(orig_width // 2, orig_height // 2)),
                     GaussianBlurOperation(radius=randint(0, 2)),
                     BoxBlurOperation(radius=randint(0, 2)),
                     MaxFilterOperation(radius=int(randint(1, 3) * 1.5)),
                     MinFilterOperation(radius=int(randint(1, 3) * 1.5)),
                     ResizeOperation(width=target_width, height=target_height, interpolation=Interpolations[randint(0, 3)])
                     ]

    degraded_without_rotation = reduce(lambda image, op: op(image), degr_pipeline, clear_image)

    operation = ResizeOperation(width=orig_width, height=orig_height, interpolation=cv.INTER_CUBIC)
    resized_back_without_rotation = operation(degraded_without_rotation)

    psnr = cv.PSNR(clear_image, resized_back_without_rotation)

    angle = uniform(-5, 5)
    operation = RotateOperation(angle=angle, center=(target_width // 2, target_height // 2))
    degraded = operation(degraded_without_rotation)

    degraded_gray = cv.cvtColor(degraded, cv.COLOR_BGR2GRAY)
    Image.fromarray(np.uint8(degraded_gray)).save(f'../../DegradedImages/degraded_image{i}.png')

    real_text = take_clear_image_text('../../ClearImages/words_coordinates.json', clear_image_name)
    tesseract_text = tesseract.image_to_string(degraded_gray)
    tesseract_mistake = int(edit_distance(real_text, tesseract_text))

    words = take_degraded_image_bboxes('../../ClearImages/words_coordinates.json', clear_image_name)

    new_data.append({'PSNR': psnr, 'tesseract_output': tesseract_text.split('\n'),
                     'tesseract_mistake': tesseract_mistake, 'words': words})
    toJson.update({f'degraded_image{i}.png': new_data})

    # cv.imshow('img', degraded_gray)
    # cv.waitKey(0)

with open('../../DegradedImages/word_coordinates.json', 'w') as write_file:
        json.dump(toJson, write_file, indent=4)
