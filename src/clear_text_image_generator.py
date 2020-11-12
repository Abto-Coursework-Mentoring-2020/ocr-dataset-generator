import os
import json
from PIL import Image, ImageFont, ImageDraw


def generate_clear_text_images(text_file_path: str, output_dir: str) -> None:
    if not (os.path.exists(text_file_path) and os.path.isdir(output_dir)):
        print(text_file_path, output_dir)
        raise ValueError('Invalid text file path and/or output directory path.')
    
    # directory for all generated images
    images_dir = os.path.join(output_dir, 'images')
    if not os.path.exists(output_dir):
        os.mkdir(images_dir)

    toJson = {}

    fontSize = 16
    print('Default font size == 16\nDo you want to change font size? [y/n] ', end='')
    answer = input()
    if answer == 'y':
        fontSize = int(input('Enter font size '))

    font = ImageFont.truetype(font="Windows/Fonts/Arial/arial.ttf", size=fontSize, encoding='unicode')

    lineSpacing = 1.5
    print('Default line spacing == 1.5\nDo you want to change line spacing? [y/n] ', end='')
    answer = input()
    if answer == 'y':
        lineSpacing = float(input('Enter line spacing '))

    WIDTH = 256
    HEIGHT = 256
    print('Default image size == (256, 256)\nDo you want to change image size? [y/n] ', end='')
    answer = input()
    if answer == 'y':
        WIDTH = int(input('Enter image width '))
        HEIGHT = int(input('Enter image height '))

    n = int(input('Enter the number of images to generate '))

    # The_Picture_of_Dorian_Gray.txt
    text = open(text_file_path, 'r').read()
    words = text.split()
    wordIndex = 0

    for i in range(n):
        img = Image.new(mode='RGB', size=(256, 256), color=(256, 256, 256))
        draw = ImageDraw.Draw(img)

        x = 0
        y = 0
        coordinates = []
        ableToPlaceText = True
        while ableToPlaceText:
            word = words[wordIndex]
            wordWidth, wordHeight = font.getsize(word)
            spaceWidth, spaceHeight = font.getsize(' ')

            if x + wordWidth + spaceWidth > WIDTH:
                x = 0
                y += int(fontSize * lineSpacing)
            if y + wordHeight > HEIGHT:
                ableToPlaceText = False
                img.save(os.path.join(images_dir, f'clearTextImage{i}.png'))
            else:
                draw.text((x, y), word, (0, 0, 0), font=font)
                coordinates.append({
                    'word': word,
                    'x1': x, 
                    'y1': y, 
                    'x2': x + wordWidth, 
                    'y2': y + wordHeight
                })
                x += wordWidth + spaceWidth
                wordIndex += 1

        toJson.update({f'clearTextImage{i}.png': coordinates})

    with open(os.path.join(output_dir, 'wordsCoordinates.json'), 'w') as write_file:
        json.dump(toJson, write_file, indent=4)
