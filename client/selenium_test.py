import os
import pytest

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from seleniumwire import webdriver # pip install selenium-wire

import time
import pandas as pd

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


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver =  webdriver.Chrome(chrome_options=options)
website_names = {website: website.split("/")[2:][0].split(".")[0] for website in WEBSITES}
access_times = {website_names[website] : -1 for website in WEBSITES}
unfiltered_percentages = {website_names[website] : -1 for website in WEBSITES}


def test_website_through_filter(website):
    # driver =  webdriver.Chrome(chrome_options=options)
    website_name = website_names[website]
    # unfiltered_percentage = 100
    timer = time.time()
    driver.get("{}{}".format(ADDRESS, website))
    
    if "internal" in website: # these are the internally-loading websites
        requests = {200: [], 301: [], 400: [], 404: [], 420: [], 500: []}
        img_requests = 0
        for request in driver.requests[-11:]: # only look at the last 11 elements
            # only check for local images
            if request.url.endswith(".png") or request.url.endswith(".jpg") or request.url.endswith(".ico"):
                img_requests += 1
                request_response = request.response.status_code
                requests[request_response].append(request.url)

        for response_code in requests.keys():
            if response_code == 420:
                unfiltered_percentage = (1 - (len(requests[420]) / img_requests)) * 100
                # unfiltered_percentages[website_name] = unfiltered_percentage
                # print("{} : {:.2f}%".format(website.split("/")[2:][0], unfiltered_percentage))
                
    elif "external" in website: # these are the externally-loading websites
        # check if the images are visible on the website
        all_imgs = driver.find_elements(By.TAG_NAME, "img")

        all_links = driver.find_elements(By.TAG_NAME, "link")
        all_favicons = [link for link in all_links if link.get_attribute("rel") == "icon"]
        # filter out the favicons that are not external, which is all of them in our websites
        external_favicons = [favicon for favicon in all_favicons if favicon.get_attribute("href").startswith("http")]
        all_imgs.extend(external_favicons)

        nr_of_external_images = 10 # it's usually 11, but the favicon is local, so we set it to 10
        unfiltered_percentage = (len(all_imgs) / nr_of_external_images) * 100

        # print("{} : {:.2f}%".format(website_name, len(all_imgs)/nr_of_external_images*100))
    
    access_times[website_name] = time.time() - timer
    unfiltered_percentages[website_name] = unfiltered_percentage
    # print("%: {} - time: {}".format(unfiltered_percentage, access_times[website_name]))
    print("\u2713", website_name)
    # driver.close()


def test_websites():
    for website in WEBSITES:
        test_website_through_filter(website)
    
    excel_row_index = 1
    for website in WEBSITES:
        website_name = website_names[website]

        # save the access times and unfiltered percentages to a xls file
        # the website name, access time and unfiltered percentage all go in the same row
        # use pandas to write to the excel file, in the appropriate column
        excel = pd.read_excel("client/test_results.xlsx")
        # pd.concat([excel, pd.DataFrame([[website_name, access_times[website_name], unfiltered_percentages[website_name]]], columns=["website name", "access time", "unfiltered percentage"])])
        new_row = [website_name, unfiltered_percentages[website_name], access_times[website_name]]
        excel.loc[excel_row_index] = new_row
        excel_row_index += 1
        excel.to_excel("client/test_results.xlsx", index=False)


    
test_websites()
print("\u2713", "excel written")

    