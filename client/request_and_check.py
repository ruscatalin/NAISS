from bs4 import BeautifulSoup
import subprocess
import os

path_network = "127.0.0.1:7777/websites/"
path_local = "server/website/websites/"

def request(url):
    (html_reply, err) = subprocess.Popen(["curl", "--silent", url],
     stdout=subprocess.PIPE).communicate()
    reply_soup = BeautifulSoup(html_reply, "html.parser")
    return reply_soup

def check(reply_soup, path_to_original):
    # compare reply_soup with the original soup in the /websites/clean folder
    with open(path_to_original, "r") as f:
        original_soup = BeautifulSoup(f.read(), "html.parser")

        reply_soup.prettify()
        original_soup.prettify()
        
        o_imgs = original_soup.find_all("img")
        o_favicons = original_soup.find_all("link", rel="icon")

        r_imgs = reply_soup.find_all("img")
        r_favicons = reply_soup.find_all("link", rel="icon")

        # figure out whether the reply contains the same images as the original and report the missing ones
        missing_imgs = []
        for o_img in o_imgs:
            if o_img not in r_imgs:
                missing_imgs.append(o_img)
        
        for o_favicon in o_favicons:
            if o_favicon not in r_favicons:
                missing_imgs.append(o_favicon)

        if len(missing_imgs) == 0:
            print("All images are present")
        else:
            print("Missing images:")
            for missing_img in missing_imgs:
                print(missing_img)

        return missing_imgs

# check all the websites. use the local path to guide the check
path_to_clean = os.path.join(path_local, "clean/")
for file in os.listdir(path_to_clean):
    if file.endswith(".html"):
        print("Checking {}".format(file))
        check(request(path_network+"clean/" + file), path_to_clean + file)

path_to_stego = os.path.join(path_local, "stego/")
for file in os.listdir(path_to_stego):
    if file.endswith(".html"):
        print("Checking {}".format(file))
        check(request(path_network+"stego/" + file), path_to_stego + file)