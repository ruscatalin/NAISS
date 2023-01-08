#use flask to create a web server that acts as a reverse proxy
from flask import Flask, request, Response
import requests
from bs4 import BeautifulSoup
import os
from PIL import Image

app = Flask(__name__)

WEB_SERVER = 'http://localhost:7777'


# define the route for the GET request
@app.route('/<path:path>', methods=['GET'])
def get(path):
    # get the response from the web server
    response = requests.get(WEB_SERVER + '/' + path)
    # create a response object
    resp = Response(response.content)

    file_name = path.split('/')[-1]
    print(file_name)

    match file_name.split('.')[-1]:
        case "html":
            html = resp.data.decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            soup = soup.prettify()
            BUFFER = {'html': soup}
            
        case "png" | "jpg" | "jpeg" | "ico" | "gif" | "svg":
            BUFFER.put(file_name, resp.data)

    # set the headers
    resp.headers['Access-Control-Allow-Origin'] = '*'

    print(BUFFER.keys())
    return resp

if __name__ == '__main__':
    # run the app
    BUFFER = {}
    app.run(debug=True, port=8899, host='0.0.0.0', use_evalex=False)

