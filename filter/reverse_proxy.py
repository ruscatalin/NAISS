from flask import Flask, Response  # use flask to create a web server that acts as a reverse proxy
import requests
from bs4 import BeautifulSoup, element
import filter
from ecdsa import NIST256p, keys

app = Flask(__name__)

WEB_SERVER = 'http://naiss-server:7777' # the web server we want to proxy
WEBSITE = None

# define the route for the GET request
@app.route('/<path:path>', methods=['GET'])
def get(path):
    """
    This function is called when a GET request is received. It incorporates the filtering process.
    Externally loaded images will be removed from the html file (and hence filtered), while the internally loaded images will be denied network transmission.

    Parameters:
        path (str): the network path to the requested file.

    Returns:
        Response: the response object that will be sent to the client. Denied images will either not have a corresponding response or will have a (420, 'Filtered by NAISS') error response.
    """
    global WEBSITE

    # get the response from the web server
    response = requests.get(WEB_SERVER + '/' + path)
    # create a copy response object
    resp = Response(response.content)

    file_name = path.split('/')[-1]
    file_type = file_name.split('.')[-1]

    if file_type == 'html': #  initialize the filtering process if the requested file is html
        html = resp.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        WEBSITE = soup

        head_tag = WEBSITE.head
        naiss_signature_tag = head_tag.find("naiss_signatures")  # all the signatures we can use for verification are in this tag
        if naiss_signature_tag is None:
            img_signature_tags = element.ResultSet(None)
        else:
            img_signature_tags = naiss_signature_tag.find_all("img_signature")  # all the signature tags as a list

        img_tags = WEBSITE.find_all("img")  # all the image tags as a list
        img_tags_external = [img_tag for img_tag in img_tags if img_tag['src'].startswith("http")]

        icon_tag = WEBSITE.find("link", rel="icon")
        if icon_tag['href'].startswith("http"):
            img_tags_external.append(icon_tag)
        
        # if there are external images, we can filter them immediately
        # Loop through the external tags and verify their signature by using the tag itself as input.
        for img_tag in img_tags_external:
            try:
                ok = filter.verify_signature(str(img_tag), img_signature_tags)  # verify the signature
            except keys.BadSignatureError:
                ok = False
            
            if not ok:
                print("Signature verification failed for " + str(img_tag))
                img_tag.decompose()  # attempt to remove the tag from the html file   
        resp.data = WEBSITE.prettify().encode('utf-8')  # update the response data

    elif file_type in ['png', 'jpg', 'jpeg', 'ico', 'gif', 'svg']:  # Here we deal with local images arriving as responses
        resp.cache_control.no_cache = True  # try to not cache files. otherwise crucial files might be skipped when navigating
        
        head_tag = WEBSITE.head
        naiss_signature_tag = head_tag.find("naiss_signatures")
        if naiss_signature_tag is None:
            img_signature_tags = element.ResultSet(None)
        else:
            img_signature_tags = naiss_signature_tag.find_all("img_signature")

        img_tags = WEBSITE.find_all("img")
        icon_tag = WEBSITE.find("link", rel="icon")

        file_occurences = [img_tag for img_tag in img_tags if file_name in img_tag['src']]  # find all the image tags that contain the file name being requested
        if not icon_tag['href'].startswith("http"):
            if file_name in icon_tag['href']:
                file_occurences.append(icon_tag)

        if file_occurences is not []:
            try:
                ok = filter.verify_signature(resp.data, img_signature_tags)  # verify the signature
            except keys.BadSignatureError:
                ok = False
            
            if not ok:
                for img_tag in file_occurences:
                    print("Signature verification failed for " + str(img_tag))
                    img_tag.decompose()
                resp = Response(status="{} {}".format(420, "Filtered by NAISS")) # Do not send the image if the signature is not valid, instead send a 420 error response

    # set the headers
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

if __name__ == '__main__':
    app.run(debug=True, port=8899, host='0.0.0.0', use_evalex=False)

