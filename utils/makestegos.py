from steganogan import SteganoGAN
import os

steganogan = SteganoGAN.load(architecture='dense')

# We get all images in the server/website/images folder and encode them with the message "RENAISSANCE"
# The encoding output will be saved in the stegoimages folder and will have 'stego' added to the begining of its name

PATH_TO_IMAGES = "server/website/images/"
PATH_TO_STEGOIMAGES = "{}stegoimages/".format(PATH_TO_IMAGES)

for filename in os.listdir(PATH_TO_IMAGES):
    if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".ico", ".bmp")):
        print(PATH_TO_IMAGES+filename)
        steganogan.encode(PATH_TO_IMAGES+filename, "{}stego_{}".format(PATH_TO_STEGOIMAGES, filename), "RENAISSANCE")  # writing the new stegoimage

print("Done encoding & writing stegoimages!")