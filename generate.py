import os
import argparse
from src.clear_text_image_generator import generate_clear_text_images
from src.downscaled_image_generator import generate_downscaled_images
from src.downscaled_image_generator import blur_images
from src.clear_text_image_generator import perspective_transform

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # dataset type (one of 'text', 'downscale', 'blur', 'transform')
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

    # PARAMETERS FOR PERSPECTIVE TRANSFORMATION OF IMAGES
    parser.add_argument('-id', '--input_dir')
    parser.add_argument('-fn', '--filename')
    parser.add_argument('-w', '--width')
    parser.add_argument('-h', '--height')
    # points coordinates from image
    # top left corner
    parser.add_argument('-x1', '--x1')
    parser.add_argument('-y1', '--y1')
    # top right corner
    parser.add_argument('-x2', '--x2')
    parser.add_argument('-y2', '--y2')
    # bottom left corner
    parser.add_argument('-x3', '--x3')
    parser.add_argument('-y3', '--y3')
    #bottom right corner
    parser.add_argument('-x4', '--x4')
    parser.add_argument('-y4', '--y4')


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

    elif args.target == 'transform':
        perspective_transform(args.input_dir, args.filename, int(args.width)), int(args.x1)),int(args.y1)),int(args.x2)),int(args.y2)), int(args.x3)), int(args.y3)), int(args.x4)), int(args.y4)))


    print(f'Dataset was successfully saved in {os.path.join(os.getcwd(), args.out_dir)} folder')
