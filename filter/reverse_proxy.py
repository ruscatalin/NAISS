#use flask to create a web server that acts as a reverse proxy
from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup, element
import os
import filter
from ecdsa import SigningKey, VerifyingKey, NIST256p, keys

import time


app = Flask(__name__)

# WEB_SERVER = 'http://localhost:7777'
WEB_SERVER = 'http://172.19.0.2:7777'
WEBSITE = None


# define the route for the GET request

@app.route('/<path:path>', methods=['GET'])
def get(path):
    global WEBSITE
    # get the response from the web server
    response = requests.get(WEB_SERVER + '/' + path)
    # create a response object
    resp = Response(response.content)

    file_name = path.split('/')[-1]
    file_type = file_name.split('.')[-1]

    if file_type == 'html': #  initialize the filtering process
        html = resp.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        WEBSITE = soup
        # BUFFER = {'html': WEBSITE}

        head_tag = WEBSITE.head
        naiss_signature_tag = head_tag.find("naiss_signatures")
        if naiss_signature_tag is None:
            img_signature_tags = element.ResultSet(None)
        else:
            img_signature_tags = naiss_signature_tag.find_all("img_signature")

        img_tags = WEBSITE.find_all("img")
        img_tags_external = [img_tag for img_tag in img_tags if img_tag['src'].startswith("http")]

        icon_tag = WEBSITE.find("link", rel="icon")
        if icon_tag['href'].startswith("http"):
            img_tags_external.append(icon_tag)
        
        # if there are external images, we can filter them immediately
        # Loop through the external tags and verify their signature by using the tag itself as input.
        for img_tag in img_tags_external:
            try:
                ok = filter.verify_signature(str(img_tag), img_signature_tags)
            except keys.BadSignatureError:
                ok = False
            
            if not ok:
                print("Signature verification failed for " + str(img_tag))
                img_tag.decompose()
                # print("After " + str(img_tag))
        
        resp.data = WEBSITE.prettify().encode('utf-8')

    elif file_type in ['png', 'jpg', 'jpeg', 'ico', 'gif', 'svg']:  # Here we deal with local images arriving as responses
        resp.cache_control.no_cache = True  # try to not cache files. otherwise crucial files might be skipped when navigating
        
        head_tag = WEBSITE.head
        naiss_signature_tag = head_tag.find("naiss_signatures")
        if naiss_signature_tag is None:
            img_signature_tags = element.ResultSet(None)
        else:
            img_signature_tags = naiss_signature_tag.find_all("img_signature")

        img_tags = WEBSITE.find_all("img")

        # img_tags_external = [img_tag for img_tag in img_tags if img_tag['src'].startswith("http")]
        img_tags_local = [img_tag for img_tag in img_tags if not img_tag['src'].startswith("http")]

        icon_tag = WEBSITE.find("link", rel="icon")

        file_occurences = [img_tag for img_tag in img_tags if file_name in img_tag['src']]
        if not icon_tag['href'].startswith("http"):
            if file_name in icon_tag['href']:
                file_occurences.append(icon_tag)

        if file_occurences is not []:
            try:
                ok = filter.verify_signature(resp.data, img_signature_tags)
            except keys.BadSignatureError:
                ok = False
            
            if not ok:
                for img_tag in file_occurences:
                    print("Signature verification failed for " + str(img_tag))
                    img_tag.decompose()
                    # print("After " + str(img_tag))
                resp = Response(status="{} {}".format(420, "Filtered by NAISS")) # Do not send the image if the signature is not valid


    # set the headers
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

if __name__ == '__main__':
    # run the app
    # BUFFER = {}
    app.run(debug=True, port=8899, host='0.0.0.0', use_evalex=False)

