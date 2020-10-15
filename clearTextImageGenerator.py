from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json

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
    lineSpacing = float(input('Enter font size '))

WIDTH = 256
HEIGHT = 256
print('Default image size == (256, 256)\nDo you want to change image size? [y/n] ', end='')
answer = input()
if answer == 'y':
    WIDTH = int(input('Enter image width '))
    HEIGHT = int(input('Enter image height '))

n = int(input('Enter the number of images to generate '))

text = open('The_Picture_of_Dorian_Gray.txt', 'r').read()
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
            img.save('Images/clearTextImage' + str(i) + '.png')
        else:
            draw.text((x, y), word, (0, 0, 0), font=font)
            coordinates.append({'x1': x, 'y1': y, 'x2': x + wordWidth, 'y2': y + wordHeight})
            x += wordWidth + spaceWidth
            wordIndex += 1

    toJson.update({'Image' + str(i) + 'Coordinates': coordinates})

with open('wordsCoordinates.json', 'w') as write_file:
    json.dump(toJson, write_file, indent=4)