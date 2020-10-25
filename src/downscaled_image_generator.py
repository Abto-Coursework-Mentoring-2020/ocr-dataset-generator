import os
import glob
import cv2
from PIL import Image


def _get_interpolation_key(interpolation: str):
    if interpolation == 'nearest':
        return cv2.INTER_NEAREST
    
    if interpolation == 'linear':
        return cv2.INTER_LINEAR

    return cv2.INTER_CUBIC


def generate_downscaled_images(
            images_dir: str, 
            target_size: tuple, 
            interpolation: str = 'cubic', 
            output_dir: str = None
        ) -> None:
    if not os.path.isdir(images_dir):
        raise ValueError('Invalid images directory path specified.')
    
    if not all(target_size):
        raise ValueError('Invalid image target size specified.')

    if not output_dir:
        output_dir = os.path.join(images_dir, '../resized_images')
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
    elif not os.path.isdir(output_dir):
        raise ValueError('Invalid output directory path specified.')
    
    inter_key = _get_interpolation_key(interpolation)
    for fp in glob.glob(os.path.join(images_dir, '*.*')):
        try:
            image = cv2.cvtColor(cv2.imread(fp), cv2.COLOR_BGR2GRAY)
            target_fp = os.path.join(output_dir, os.path.split(fp)[-1])
            Image.fromarray(cv2.resize(image, target_size, interpolation=inter_key)).save(target_fp)
        except Exception as ex:
            print(f'Couldn\'t resize {fp}. {ex}')

# generate_downscaled_images('./tmp/images', (128, 128))


