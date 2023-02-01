# convert and save a copy of the png images as jpg

import os
from PIL import Image

for file in os.listdir('server/website/images'):
    if file.endswith('.png'):
        im = Image.open('server/website/images/{}'.format(file))
        rgb_im = im.convert('RGB')
        rgb_im.save('server/website/images/{}.jpg'.format(file.split('.')[0]))