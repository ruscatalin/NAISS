import os
from bs4 import BeautifulSoup
import pandas as pd # needs pip(3) install openpyxl

def add_images_to_tag(soup, tag, img_format, internal, use_stegos):
    """
    Given a tag that is supposed to contain multiple images, adds the (stego)images to the tag.

    Parameters:
        soup (BeautifulSoup): the BeautifulSoup object of the website
        tag (Tag): the tag to add the images to (e.g. the tag that contains the payment methods)
        img_format (str): the image format to use (jpg or png)
        internal (bool): whether the images are internal or external (i.e. file path or http link)
        use_stegos (bool): whether to use stegoimages or not
    """

    if internal:
        if use_stegos == True:
            path_to_images = "images/stegoimages"
        else:
            path_to_images = "images"
        path_to_images = "../../{}".format(path_to_images) # new relative path to the images folder
    else:
        links_to_images = pd.read_excel("utils/img.xlsx")  # here are the external links to the images

    if tag['id'] == "credit_cards":
        payments = ["visa", "maestro", "mastercard", "americanexpress"]
    elif tag['id'] == "other_payment_methods":
        payments = ["paypal", "bitcoin", "googlepay", "payu", "westernunion"]

    for payment in payments:
        if use_stegos:
            payment = "stego_" + payment

        if internal:
            path_to_image = os.path.join(path_to_images, "{}.{}".format(payment, img_format))
            tag.append(soup.new_tag("img", src=path_to_image, width="40"))
        else:
            link = links_to_images.loc[links_to_images.iloc[:, 0] == "{}.{}".format(payment, img_format)].iloc[0, 1]  # the appropriate link for the payment image (e.g. paypal.png)
            tag.append(soup.new_tag("img", src=link, width="40"))


def create_website(path_to_website, internal=False, use_stegos=False, img_format=None):
    """
    Creates a nosig website and writes it in another appropriate folder.

    Parameters:
        path_to_website (str): path to the website folder
        internal (bool): whether to use internal (file path) or external links (https link)
        use_stegos (bool): whether to use stegoimages or not
        img_format (str): the image format to use (jpg or png)
    """

    # We use server/website/index_template.html as a template for generating more index.html files
    with open(os.path.join(path_to_website, "index_template.html"), "r") as f:
        html = f.read() # Save the index_template.html as a deep copy
        soup = BeautifulSoup(html, 'html.parser')

        other_payment_methods_tag = soup.find("div", id="other_payment_methods")
        icons_tag = soup.find("div", id="credit_cards")

        css = soup.find("link", rel="stylesheet")
        favicon = soup.find("link", rel="icon")
        logo = soup.find("img", id="big_logo")

        # modify the css href such that it's ok with the new path
        css["href"] = "../../{}".format(css["href"])

        # modify the favicon href such that it's ok with the new path
        if not use_stegos:
            favicon["href"] = "../../{}".format(favicon["href"])
        else:
            favicon["href"] = "../../images/stegoimages/stego_logo.ico"

        

        # add a new <img> tag for each alternate payment method (paypal, bitcoin, googlepay, payu, westernunion)
        add_images_to_tag(soup, other_payment_methods_tag, img_format, internal, use_stegos)
        # add new <img> tags for each credit card (maestro, mastercard, visa, americanexpress)
        add_images_to_tag(soup, icons_tag, img_format, internal, use_stegos)        

        if internal:
            if not use_stegos:
                logo["src"] = "../../{}".format(logo["src"])
            else:
                logo["src"] = "../../images/stegoimages/stego_logo.{}".format(img_format)
        else:
            # read the excel file with external links
            df = pd.read_excel("utils/img.xlsx")
            # first column is the name of the image, second column is the link

            if not use_stegos:
                link = df.loc[df.iloc[:, 0] == "logo.{}".format(img_format)].iloc[0, 1]
            else:
                link = df.loc[df.iloc[:, 0] == "stego_logo.{}".format(img_format)].iloc[0, 1]

            logo["src"] = link
            
        # We save the new index.html file to \websites\clean\ if it uses no stegos, or \websites\stego\ if it does
        if use_stegos:
            path_to_write = os.path.join(path_to_website, "websites/stego")
        else:
            path_to_write = os.path.join(path_to_website, "websites/clean")

        # The naming scheme of a website is nosig_{clean, stego}_{internal, external}_{jpg/png}_index.html
        name = "nosig_{}_{}_{}_index.html".format("clean" if not use_stegos else "stego", "internal" if internal else "external", img_format)
        with open(os.path.join(path_to_write, name), "w") as f2:
            f2.write(str(soup.prettify()))
            f2.close()

        f.close()


# Creating the (nosig) websites

# We create a set of websites which contains no stegoimages. We use all the images in /images (.jpg, .png and .ico)
create_website("server/website", False, False, "jpg")
create_website("server/website", False, False, "png")
print("Done with external clean websites")
create_website("server/website", True, False, "jpg")
create_website("server/website", True, False, "png")
print("Done with internal clean websites")

# We then recreate the same set, but using stegoimages from /images/stegoimages
create_website("server/website", False, True, "jpg")
create_website("server/website", False, True, "png")
print("Done with external stego websites")
create_website("server/website", True, True, "jpg")
create_website("server/website", True, True, "png")
print("Done with internal stego websites")




