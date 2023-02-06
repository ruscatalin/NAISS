"""
 This file just automates the signing procedures of our websites
 It uses sign.py cli to sign the "nosig" websites inside ../server/website/websites/clean and ../server/website/websites/stego
 It also uses both private keys to sign the websites (one of which is the evil one)
"""

import os
import subprocess

path_to_here = os.path.dirname(os.path.abspath(__file__))
path_to_signing_script = os.path.join(path_to_here, "sign.py")
path_to_keys = [os.path.join(path_to_here, "private_key.pem"), os.path.join(path_to_here, "evil_private_key.pem")]
path_to_clean = os.path.join(path_to_here, "..", "server", "website", "websites", "clean")
path_to_stego = os.path.join(path_to_here, "..", "server", "website", "websites", "stego")

for filename in os.listdir(path_to_clean):
    if filename.startswith("nosig"):
        print("Signing {}".format(filename))
        path_to_file = os.path.join(path_to_clean, filename)
        subprocess.call(["python3", path_to_signing_script, path_to_file, path_to_keys[0]])  #  use 'python' instead of 'python3' if running on Windows
        subprocess.call(["python3", path_to_signing_script, path_to_file, path_to_keys[1]])

for filename in os.listdir(path_to_stego):
    if filename.startswith("nosig"):
        print("Signing {}".format(filename))
        path_to_file = os.path.join(path_to_stego, filename)
        subprocess.call(["python3", path_to_signing_script, path_to_file, path_to_keys[0]])
        subprocess.call(["python3", path_to_signing_script, path_to_file, path_to_keys[1]])