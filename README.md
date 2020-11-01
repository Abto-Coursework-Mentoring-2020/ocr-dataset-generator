# ocr-dataset-generator
Tools for synthetic dataset generation.

<hr/>

## Setting up project locally
It is assumed that you have `python3` and `git` installed on your system.

1) Clone the repository and open `cmd`/`bash` inside the project directory.
2) Install `virtualenv` package running `pip install virtualenv`
3) Create virtual environment running `virtualenv venv` and activate
4) Activate it with `source venv/Scripts/activate` (Windows) or `source venv/bin/activate` (Linux)
4) Run `pip install -r requirements.txt` to get required packages.
5) Run `jupyter notebook` and you are good to go.

## Dataset creation
Use generate.py script to create datasets, such as: 

#### Clear text images dataset and it's annotation:
`python generate.py --target text --text-file-path ./data/The_Picture_of_Dorian_Gray.txt`

#### Downscaled images with different interpolations.
`python generate.py --target downscale --images-dir ./tmp/images -hg 128 -wd 128 --interpolation cubic`

#### Blured images with different kernels.
TODO
