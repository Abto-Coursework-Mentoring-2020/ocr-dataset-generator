import os
import argparse
from src.clear_text_image_generator import generate_clear_text_images
from src.downscaled_image_generator import generate_downscaled_images
from src.downscaled_image_generator import blur_images

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # dataset type (one of 'text', 'downscale', 'blur')
    parser.add_argument('-t', '--target', required=True)
    # output directory
    parser.add_argument('-o', '--out-dir', default='./tmp')

    # PARAMETERS FOR CLEAR TEXT IMAGES GENERATION
    # path of the file with text for clear text images generation
    parser.add_argument('-tfp', '--text-file-path')

    # PARAMETERS FOR DOWNSCALED IMAGES GENERATION
    # path of the file with text for clear text images generation
    parser.add_argument('-id', '--images-dir')
    parser.add_argument('-hg', '--height')
    parser.add_argument('-wd', '--width')
    parser.add_argument('-i', '--interpolation')

    # PARAMETERS FOR BLURRING IMAGES
    # path of the dir with images
    parser.add_argument('-id', '--images-dir')
    parser.add_argument('-fn', '--filename')
    # filter for blurring - can be gaussian, box, min, max or median
    parser.add_argument('-fl', '--filter')
    parser.add_argument('-r', '--radius')

    args = parser.parse_args()

    if args.target == 'text':
        generate_clear_text_images(args.text_file_path, args.out_dir)

    elif args.target == 'downscale':
        generate_downscaled_images(args.images_dir, (int(args.height), int(args.width)), args.interpolation)

    elif args.target == 'blur':
        # your blur dataset generation function here
        blur_images(args.images_dir, args.filename, args.filter, int(args.radius))
    else:
        raise ValueError('Ivalid value for target option specified.')

    print(f'Dataset was successfully saved in {os.path.join(os.getcwd(), args.out_dir)} folder')
