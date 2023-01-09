import os
import pytest

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from seleniumwire import webdriver # pip install selenium-wire

HOSTNAME = "localhost"
PORT = 8899
ADDRESS = "http://{}:{}/".format(HOSTNAME, PORT)
WEBSITES = [
    "websites/clean/evilsig_clean_external_jpg_index.html",
    "websites/clean/evilsig_clean_external_png_index.html",
    "websites/clean/evilsig_clean_internal_jpg_index.html",
    "websites/clean/evilsig_clean_internal_png_index.html",
    "websites/clean/nosig_clean_external_jpg_index.html",
    "websites/clean/nosig_clean_external_png_index.html",
    "websites/clean/nosig_clean_internal_jpg_index.html",
    "websites/clean/nosig_clean_internal_png_index.html",
    "websites/clean/sig_clean_external_jpg_index.html",
    "websites/clean/sig_clean_external_png_index.html",
    "websites/clean/sig_clean_internal_jpg_index.html",
    "websites/clean/sig_clean_internal_png_index.html",

    "websites/stego/evilsig_stego_external_jpg_index.html",
    "websites/stego/evilsig_stego_external_png_index.html",
    "websites/stego/evilsig_stego_internal_jpg_index.html",
    "websites/stego/evilsig_stego_internal_png_index.html",
    "websites/stego/nosig_stego_external_jpg_index.html",
    "websites/stego/nosig_stego_external_png_index.html",
    "websites/stego/nosig_stego_internal_jpg_index.html",
    "websites/stego/nosig_stego_internal_png_index.html",
    "websites/stego/sig_stego_external_jpg_index.html",
    "websites/stego/sig_stego_external_png_index.html",
    "websites/stego/sig_stego_internal_jpg_index.html",
    "websites/stego/sig_stego_internal_png_index.html",
]


# options = ChromeOptions(headless=True)
# driver = Chrome(options=options)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver =  webdriver.Chrome(chrome_options=options)

for website in WEBSITES:
    driver.get("{}{}".format(ADDRESS, website))
    if "internal" in website: # these are the internally-loading websites
        requests = {200: [], 301: [], 400: [], 404: [], 420: [], 500: []}
        img_requests = 0
        # print(driver.requests)
        for request in driver.requests:
            # only check for local images
            if request.url.endswith(".png") or request.url.endswith(".jpg") or request.url.endswith(".ico"):
                img_requests += 1
                request_response = request.response.status_code
                requests[request_response].append(request.url)
    
        # report how many requests were made and how many response codes we got for each request
        for response_code in requests.keys():
            if response_code == 420:
                unfiltered_percentage = (1 - (len(requests[420]) / img_requests)) * 100
                print("{} : {:.2f}%".format(website.split("/")[2:][0], unfiltered_percentage))
        # for response_code, request_urls in requests.items():
        #     if request_urls == []:
        #         continue
        #     elif response_code == 420:
        #         unfiltered_percentage = 1 - len(request_urls) / img_requests
        #         print("{} : {:.2f}%".format(website.split("/")[2:][0], (1-len(request_urls)/img_requests)*100))
        
        # print('\n')
    elif "external" in website: # these are the externally-loading websites
        # check if the images are visible on the website
        all_imgs = driver.find_elements(By.TAG_NAME, "img")
        all_links = driver.find_elements(By.TAG_NAME, "link")
        all_favicons = [link for link in all_links if link.get_attribute("rel") == "icon"]
        all_imgs.extend(all_favicons)
        # cut the website/{clean/stego} part of the website from the website
        website = website.split("/")[2:][0]
        print("{} : {:.2f}%".format(website, len(all_imgs)/12*100))
        # print('\n')