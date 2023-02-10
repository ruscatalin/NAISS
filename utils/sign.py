from ecdsa import SigningKey, NIST256p
import argparse
from bs4 import BeautifulSoup # pip install beautifulsoup4
import os

def generate_private_key():
    """
    Generates and returns a private key using the NIST256p EC curve.
    """
    return SigningKey.generate(curve=NIST256p)

def get_signature(input, private_key):
    """
    Returns the deterministic signature of an input using the private key.

    Parameters:
        input (bytes or str): The input to sign.
        private_key (ecdsa.SigningKey): The private key to use for signing.
    Returns:
        str: The deterministic signature of the input, represented with hexadecimal characters.
    """
    if type(input) != bytes:
        input = input.encode('utf-8')
    return private_key.sign_deterministic(input).hex()

def sign_website(path_to_website, private_key, evil):
    """
    Signs a website by adding the signatures of the images and favicons to the <head> tag of the html file.

    Parameters:
        path_to_website (str): The path to the website to sign.
        private_key (ecdsa.SigningKey): The private key to use for signing.
        evil (bool): Let the method know whether or not the evil key is used. Needed for generating the website name.
    """
    # Recursively find all the images (all formats) in the path_to_website (and subdirectories) and compute their signatures
    signature_list = []
    dir_to_website = os.path.dirname(path_to_website)

    # Look into the html file and produce signatures for the internal src of found <img> and favicons
    with open(os.path.join(path_to_website), "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        img_tags = soup.find_all("img")  # returns a list of all the <img> tags
        for img_tag in img_tags:
            if not img_tag['src'].startswith("http"):
                with open(os.path.join(dir_to_website, img_tag['src']), "rb") as f:
                    signature_list.append(get_signature(f.read(), private_key))  # get the file signature and append it

        favicon_tag = soup.find("link", rel="icon")  # returns a list of favicons (if any)
        if favicon_tag and not favicon_tag['href'].startswith("http"):
            with open(os.path.join(dir_to_website, favicon_tag['href']), "rb") as f:
                signature_list.append(get_signature(f.read(), private_key))

    # Look into html file and produce signatures for the <img> and favicons (if any) that point to external sources. 
    # Use the tags as input for the signature (instead of the image content, as it was done above)
    with open(os.path.join(path_to_website), "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        img_tags = soup.find_all("img")
        for img_tag in img_tags:
            if img_tag['src'].startswith("http"):
                signature_list.append(get_signature(str(img_tag), private_key))

        link_tags = soup.find_all("link")
        for link_tag in link_tags:
            if "icon" in link_tag['rel']:
                if link_tag['href'].startswith("http"):
                    signature_list.append(get_signature(str(link_tag), private_key))
                
    signature_list = sorted(signature_list)
            
    # Add the signatures to the <head> tag like this:
    ### <naiss_signatures>
    ###     <img_signature value="{signature1}"></img_signature>
    ###     <img_signature value="{signature2}"></img_signature>
    ###     ...
    ### </naiss_signatures>

    with open(os.path.join(path_to_website), "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        head_tag = soup.head

        if head_tag.find("naiss_signatures") is None:  # if the <naiss_signature> tag does not exist, create it
            naiss_signature_tag = soup.new_tag("naiss_signatures")
            head_tag.append(naiss_signature_tag)
        
        naiss_signature_tag = head_tag.find("naiss_signatures")
        for signature in signature_list:
            if naiss_signature_tag.find("img_signature", value=signature) is None:
                img_signature_tag = soup.new_tag("img_signature")
                img_signature_tag['value'] = signature
                naiss_signature_tag.append(img_signature_tag)

        new_name = path_to_website  # after signing, the file should be prefixed with "sig" or "evilsig"
        if evil:
            new_name = path_to_website.replace("nosig", "evilsig")
        else:
            new_name = path_to_website.replace("nosig", "sig")

        with open(os.path.join(new_name), "w") as f2:
            f2.write(str(soup.prettify()))
            f2.close()
        f.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sign a file')
    parser.add_argument('file_path', metavar='file_path', type=str, help='path to the file to be signed')
    parser.add_argument('private_key_path', metavar='private_key_path', type=str, help='path to the private key')

    args = parser.parse_args()

    ## Uncomment the following lines to generate a new key pair. Append "evil_" to the file name to generate an evil key.

    # with open("private_key.pem", "w") as f:
    #     f.write(generate_private_key().to_pem().decode('utf-8'))
    # with open("public_key.pem", "w") as f:
    #     pbk = SigningKey.from_pem(open(args.private_key_path).read()).get_verifying_key()
    #     f.write(pbk.to_pem().decode('utf-8'))

    try:
        private_key = SigningKey.from_pem(open(args.private_key_path).read())
        evil = False
        if "evil" in args.private_key_path:
            evil = True
    except:
        print("Private key not found")
    
    if args.file_path.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".bmp")): # mainly used for testing
        print(get_signature(args.file_path, private_key))
    else:
        sign_website(args.file_path, private_key, evil)
    

