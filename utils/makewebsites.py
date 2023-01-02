# We use server/website/index_template.html as a template for generating more index.html files
# We create a set of websites which contains no stegoimages. We use all the images in /images (.jpg, .png and .ico)
# We then recreate the same set, but using stegoimages from /images/stegoimages

# Put the clean websites into /website/clean and the stego websites into /website/stego

import os
import shutil
from bs4 import BeautifulSoup
import pandas as pd # needs pip(3) install openpyxl


def add_images_to_tag(soup, tag, path_to_images, card, img_format, internal):
    path_to_images = "../../{}".format(path_to_images) # new relative path to the images folder
    if card:
        cards = ["visa", "maestro", "mastercard", "americanexpress"]
        for card in cards:
            tag.append(soup.new_tag("img", src=os.path.join(path_to_images, "{}.{}".format(card, img_format)), width="40"))
    else:
        other_payments = ["paypal", "bitcoin", "googlepay", "payu", "westernunion"]
        for payment in other_payments:
            tag.append(soup.new_tag("img", src=os.path.join(path_to_images, "{}.{}".format(payment, img_format)), width="40"))

# Now, test out creating one website from index_template.html

# Save the index_template.html as a deep copy into a variable
def create_website(path_to_website, internal=False, use_stegos=False, img_format=None):
    with open(os.path.join(path_to_website, "index_template.html"), "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        other_payment_methods_tag = soup.find("div", id="other_payment_methods")
        icons_tag = soup.find("div", class_="icons")

        css = soup.find("link", rel="stylesheet")
        favicon = soup.find("link", rel="icon")
        logo = soup.find("img", id="big_logo")

        # modify the css href such that it's ok with the new path
        css["href"] = "../../{}".format(css["href"])  

        # do the same for the favicon
        if not use_stegos:
            favicon["href"] = "../../{}".format(favicon["href"])
        else:
            favicon["href"] = "../../stegoimages/stego_logo.ico"

        if internal:
            # do the same for the big logo as well
            if not use_stegos:
                logo["src"] = "../../{}".format(logo["src"])
            else:
                logo["src"] = "../../stegoimages/stego_logo.{}".format(img_format)
            
            if not use_stegos:
                # add a new <img> tag for each alternate payment method .jpg image in /images (paypal, bitcoin, googlepay, payu, westernunion)
                add_images_to_tag(soup, other_payment_methods_tag, "images", False, img_format, internal)
                # add new <img> tags for each credit card .jpg image in /images (maestro, mastercard, visa, americanexpress)
                add_images_to_tag(soup, icons_tag, "images", True, img_format, internal)
            else:
                add_images_to_tag(soup, other_payment_methods_tag, "stegoimages", False, img_format, internal)
                add_images_to_tag(soup, icons_tag, "stegoimages", True, img_format, internal)

        else:
            # read the excel file with external links
            df = pd.read_excel("utils/img.xlsx")
            # first column is the name of the image, second column is the link

            if not use_stegos:
                link = df.loc[df.iloc[:, 0] == "logo.{}".format(img_format)].iloc[0, 1]
                logo["src"] = link
            else:
                link = df.loc[df.iloc[:, 0] == "stego_logo.{}".format(img_format)].iloc[0, 1]
                logo["src"] = link
            
            if not use_stegos:
                add_images_to_tag(soup, other_payment_methods_tag, "images", False, img_format, internal)
                add_images_to_tag(soup, icons_tag, "images", True, img_format, internal)


        # save the new index.html file to \websites\clean\ if it uses no stegos, or \websites\stego\ if it does
        # the naming scheme is nosig_{clean, stego}_{internal, external}_{jpg/png}_index.html

        if use_stegos:
            path_to_write = os.path.join(path_to_website, "websites/stego")
        else:
            path_to_write = os.path.join(path_to_website, "websites/clean")


        name = "nosig_{}_{}_{}_index.html".format("clean" if not use_stegos else "stego", "internal" if internal else "external", img_format)
        with open(os.path.join(path_to_write, name), "w") as f2:
            f2.write(str(soup.prettify()))
            f2.close()

        f.close()

# create_website("server/website", True, False, "jpg")
# create_website("server/website", True, False, "png")
create_website("server/website", False, False, "jpg")



