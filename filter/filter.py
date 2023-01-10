from ecdsa import SigningKey, VerifyingKey, NIST256p, keys
import argparse
from bs4 import BeautifulSoup, element # pip install beautifulsoup4
import os

RELATIVE_PATH_TO_PROJECT = "filter/"
RELATIVE_PATH_TO_PUBLIC_KEY = "public_key.pem"

def pk_verify_sig(public_key, signature, to_verify):
    # straightforward verification of a signature. the to_verify is bytes
    try:
        return public_key.verify(signature, to_verify)
    except keys.BadSignatureError:
        pass

def verify_signature(input, signature):
    # if the signature is in fact a list of signatures, we loop through them until we find a match
    if type(signature) == element.ResultSet:
        for sig in signature:
            if verify_signature(input, sig):
                return True
        return False

    elif type(signature) == element.Tag:
        # transform the signature into bytes
        signature = bytes.fromhex(signature['value'])
        

    elif type(signature) == str:
        if len(signature) % 2 == 1:
            signature = "0" + signature
        signature = bytes.fromhex(signature)
        print(signature)

    if (type(input) == str):
        input = input.encode('utf-8')
    
    try:
        absolute_path_to_key = os.path.join(RELATIVE_PATH_TO_PROJECT, RELATIVE_PATH_TO_PUBLIC_KEY)
        public_key = VerifyingKey.from_pem(open(absolute_path_to_key, "r").read())
    except:
        print("Could not read public key from " + RELATIVE_PATH_TO_PUBLIC_KEY)
        return False

    try:
        return public_key.verify(signature, input)
    except keys.BadSignatureError:
        pass

def filter_website(website_file):
    # find each image element inside the index.html file and verify its signature
    with open(os.path.join(RELATIVE_PATH_TO_PROJECT, website_file), "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        head_tag = soup.head
        naiss_signature_tag = head_tag.find("naiss_signatures")
        if naiss_signature_tag is None:
            img_signature_tags = element.ResultSet(None)
        else:
            img_signature_tags = naiss_signature_tag.find_all("img_signature")

        img_tags = soup.find_all("img")
        img_tags_external = [img_tag for img_tag in img_tags if img_tag['src'].startswith("http")]
        img_tags_local = [img_tag for img_tag in img_tags if not img_tag['src'].startswith("http")]

        link_tags = soup.find_all("link")
        for link_tag in link_tags:  # add favicons to the appropriate list (external or local images)
            if "icon" in link_tag['rel']:
                if link_tag['href'].startswith("http"):
                    img_tags_external.append(link_tag)
                else:
                    img_tags_local.append(link_tag)

        all_good = True

        # Loop through the local tags and verify their signatures by looking for the corresponding local file.
        for img_tag in img_tags_local:
            source = None
            try:
                source = img_tag['src']
            except KeyError:
                source = img_tag['href']

            try:
                # print("Source signature:" + sign.get_signature(source, SigningKey.from_pem(open("private_key.pem").read())))
                ok = verify_signature(source, img_signature_tags)
            except keys.BadSignatureError:
                ok = False
            
            if not ok:
                print("Signature verification failed for " + str(img_tag))
                img_tag.decompose()
                print("After " + str(img_tag))
                all_good = False
        
        # Loop through the external tags and verify their signature by using the tag itself as input.
        for img_tag in img_tags_external:
            try:
                ok = verify_signature(str(img_tag), img_signature_tags)
            except keys.BadSignatureError:
                ok = False
            
            if not ok:
                print("Signature verification failed for " + str(img_tag))
                img_tag.decompose()
                print("After " + str(img_tag))
                all_good = False

        if all_good:
            print("Verification: All good!")

        with open(os.path.join(RELATIVE_PATH_TO_PROJECT, website_file), "w") as f2:
            f2.write(str(soup.prettify()))
    
        f.close()

# print(verify_signature("logo.ico",
#  "db392f1d334758a8804d6974d2420eb5cbdeb4e1a6543526a3736558aa0a26ef0c275a666ced9c04928e73701099974f42b52", "public_key.pem"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Filter a website.')
    parser.add_argument('path_to_project', type=str, help='Path to the website project to filter.')
    parser.add_argument('path_to_public_key', type=str, help='Path to the public key to use for signature verification.')
    parser.add_argument('website_file', type=str, help='Path to the website file to filter.', default="index.html", nargs="?")

    args = parser.parse_args()
    RELATIVE_PATH_TO_PROJECT = args.path_to_project
    RELATIVE_PATH_TO_PUBLIC_KEY = args.path_to_public_key

    filter_website(args.website_file)

