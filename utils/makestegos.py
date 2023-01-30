from steganogan import SteganoGAN
import os

steganogan = SteganoGAN.load(architecture='dense')

# the output will be save in the stegoimages folder and will have stego added to the begining of its name

PATH_TO_IMAGES = "../server/website/images/"
PATH_TO_STEGOIMAGES = "{}stegoimages/".format(PATH_TO_IMAGES)

# read the payload from utils/magecartsample.js
PAYLOAD = open("magecartsample.js", "r").read()

for filename in os.listdir(PATH_TO_IMAGES):
    if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".ico", ".bmp")):
        print(PATH_TO_IMAGES+filename)
        steganogan.encode(PATH_TO_IMAGES+filename, "{}stego_{}".format(PATH_TO_STEGOIMAGES, filename), PAYLOAD)

print("Done encoding stegoimages!")
print("Now we check the decoding of those images ...")

for filename in os.listdir(PATH_TO_STEGOIMAGES):
    if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".bmp")):
        try:
            print("Decoded message from {}: {}".format(filename, steganogan.decode("{}{}".format(PATH_TO_STEGOIMAGES, filename))))
        except ValueError:
            print("Could not decode message from {}".format(filename))