from ecdsa import SigningKey, NIST256p
import argparse
from bs4 import BeautifulSoup # pip install beautifulsoup4
import os

def generate_private_key():
    return SigningKey.generate(curve=NIST256p)

def get_signature(input, private_key):
    if type(input) != bytes:
        input = input.encode('utf-8')
    return private_key.sign_deterministic(input).hex()

def sign_website(path_to_website, private_key, evil):
    # Recursively find all the images (all formats) in the path_to_website (and subdirectories) and compute their signatures
    signature_list = []
    dir_to_website = os.path.dirname(path_to_website)

    # Look into the file and produce signatures for the internal src of found <img> and favicons
    with open(os.path.join(path_to_website), "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        img_tags = soup.find_all("img")
        for img_tag in img_tags:
            if not img_tag['src'].startswith("http"):
                with open(os.path.join(dir_to_website, img_tag['src']), "rb") as f:
                    signature_list.append(get_signature(f.read(), private_key))

        favicon_tag = soup.find("link", rel="icon")
        if favicon_tag and not favicon_tag['href'].startswith("http"):
            with open(os.path.join(dir_to_website, favicon_tag['href']), "rb") as f:
                signature_list.append(get_signature(f.read(), private_key))

    
    
    # Look into index.html and produce signatures for the <img> and favicons (if any) that point to external sources. 
    # Use the tags as input for the signature (instead of the image content)
    with open(os.path.join(path_to_website), "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        

        # look for tags
        img_tags = soup.find_all("img")
        for img_tag in img_tags:
            if img_tag['src'].startswith("http"):
                signature_list.append(get_signature(str(img_tag), private_key))

        # look for favicons
        link_tags = soup.find_all("link")
        for link_tag in link_tags:
            if "icon" in link_tag['rel']:
                if link_tag['href'].startswith("http"):
                    signature_list.append(get_signature(str(link_tag), private_key))
                else:
                    with open(os.path.join(dir_to_website, link_tag['href']), "rb") as f:
                        signature_list.append(get_signature(f.read(), private_key))
                
        signature_list = sorted(signature_list)
            

    # Find the index.html file and add the signatures to the <head> tag like this:
    ### <NAISS_signatures>
    ###     <img_signature value="{signature1}"></img_signature>
    ###     <img_signature value="{signature2}"></img_signature>
    ###     ...
    ### </NAISS_signatures>

    with open(os.path.join(path_to_website), "r") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        head_tag = soup.head # TODO: insert the signatures at the top of the body, not in the head

        if head_tag.find("naiss_signatures") is None:
            naiss_signature_tag = soup.new_tag("naiss_signatures")
            head_tag.append(naiss_signature_tag)
        
        naiss_signature_tag = head_tag.find("naiss_signatures")
        for signature in signature_list:
            if naiss_signature_tag.find("img_signature", value=signature) is None:
                img_signature_tag = soup.new_tag("img_signature")
                img_signature_tag['value'] = signature
                naiss_signature_tag.append(img_signature_tag)
            
        # else:
        #     naiss_signature_tag = head_tag.find("naiss_signatures")
        #     for signature in signature_list:
        #         if naiss_signature_tag.find("img_signature", value=signature) is None:
        #             img_signature_tag = soup.new_tag("img_signature")
        #             img_signature_tag['value'] = signature
        #             naiss_signature_tag.append(img_signature_tag)

        new_name = path_to_website
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
    

