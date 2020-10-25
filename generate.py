import os
import argparse
from src.clear_text_image_generator import generate_clear_text_images


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # dataset type (one of 'text', 'downscale', 'blur')
    parser.add_argument('-t', '--target', required=True) 
    # output directory 
    parser.add_argument('-o', '--out-dir', default='./tmp') 
    # path of the file with text for clear text images generation  
    parser.add_argument('-tfp', '--text-file-path')
    
    args = parser.parse_args()

    if args.target == 'text':
        generate_clear_text_images(args.text_file_path, args.out_dir)

    elif args.target == 'downscale':
        pass

    elif args.target == 'blur':
        # your blur dataset generation function here
        pass
    else:
        raise ValueError('Ivalid value for target option specified.')

    print(f'Dataset was successfully saved in {os.path.join(os.getcwd(), args.out_dir)} folder')
