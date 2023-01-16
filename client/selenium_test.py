import os
import pytest

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Safari, Ie, IeOptions
from selenium.webdriver.common.by import By
from seleniumwire import webdriver # pip install selenium-wire
# the seleniumwire.cert needs to be manually to Truested Root Cert Authorities added to each browser in order to avoid certificate errors with external links


import time
import pandas as pd

HOSTNAME = "localhost"
PORT = 8899

WEBSITES = [
    "websites/clean/evilsig_clean_internal_jpg_index.html",
    "websites/clean/evilsig_clean_internal_png_index.html",
    "websites/clean/evilsig_clean_external_jpg_index.html",
    "websites/clean/evilsig_clean_external_png_index.html",
    "websites/clean/nosig_clean_internal_jpg_index.html",
    "websites/clean/nosig_clean_internal_png_index.html",
    "websites/clean/nosig_clean_external_jpg_index.html",
    "websites/clean/nosig_clean_external_png_index.html",
    "websites/clean/sig_clean_internal_jpg_index.html",
    "websites/clean/sig_clean_internal_png_index.html",
    "websites/clean/sig_clean_external_jpg_index.html",
    "websites/clean/sig_clean_external_png_index.html",

    "websites/stego/evilsig_stego_internal_jpg_index.html",
    "websites/stego/evilsig_stego_internal_png_index.html",
    "websites/stego/evilsig_stego_external_jpg_index.html",
    "websites/stego/evilsig_stego_external_png_index.html",
    "websites/stego/nosig_stego_internal_jpg_index.html",
    "websites/stego/nosig_stego_internal_png_index.html",
    "websites/stego/nosig_stego_external_jpg_index.html",
    "websites/stego/nosig_stego_external_png_index.html",
    "websites/stego/sig_stego_internal_jpg_index.html",
    "websites/stego/sig_stego_internal_png_index.html",
    "websites/stego/sig_stego_external_jpg_index.html",
    "websites/stego/sig_stego_external_png_index.html",
]


def get_driver(which_one):
    selenium_options = {
        'ca_cert': 'client/seleniumwire.crt'
    }
    match which_one:
        case "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--accept-insecure-certs')
            return webdriver.Chrome(chrome_options=options, seleniumwire_options=selenium_options)
        case "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            return webdriver.Firefox(options=options)
        case "safari":
            selenium_options['port'] = 4204
            return webdriver.Safari(seleniumwire_options=selenium_options)
        case "edge":
            options = webdriver.EdgeOptions()
            options.add_argument('--headless')
            return webdriver.Edge(options=options, seleniumwire_options=selenium_options)

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver =  webdriver.Chrome(chrome_options=options)
website_names = {website: website.split("/")[2:][0].split(".")[0] for website in WEBSITES}
driver = get_driver("chrome")
driver.close()


def test_website(website):
    global PORT
    ADDRESS = "http://{}:{}/".format(HOSTNAME, PORT)
    # driver =  webdriver.Chrome(chrome_options=options)
    website_name = website_names[website]
    # unfiltered_percentage = 100
    payload_size = 0
    timer = time.time()
    driver.get("{}{}".format(ADDRESS, website))

    website_requests = []
    is_from_website = False
    for request in driver.requests:
        if "{}{}".format(ADDRESS, website) == request.url:
            is_from_website = True
        if is_from_website:
            website_requests.append(request)
    
    if "internal" in website: # these are the internally-loading websites
        requests = {200: [], 301: [], 400: [], 404: [], 420: [], 500: []}
        img_requests = 0
        
        for request in website_requests:
            # only count the image requests for 'internal' websites
            if request.url.endswith(".png") or request.url.endswith(".jpg") or request.url.endswith(".ico"):
                img_requests += 1

            if  request.response:
                if request.response.status_code == 200 or request.response.status_code == 301 or request.response.status_code == 304:
                    if not (request.url.endswith(".css") or request.url.endswith(".js")  or "fontawesome" in request.url):
                        payload_size += len(request.response.body)
                                    
                request_response = request.response.status_code
                requests[request_response].append(request.url)

        for response_code in requests.keys():
            if response_code == 420:
                if len(requests[420]) == 0:
                    unfiltered_percentage = 100
                else:
                    unfiltered_percentage = (1 - (len(requests[420]) / img_requests)) * 100
                # unfiltered_percentages[website_name] = unfiltered_percentage
                # print("{} : {:.2f}%".format(website.split("/")[2:][0], unfiltered_percentage))

        # if len(requests[200]) == 1:
        #     print(driver.requests[-10:])
                
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

        for request in website_requests:
            if request.response:
                response_code = request.response.status_code
                if  response_code == 200  or response_code == 301 or response_code == 304:
                    if not (request.url.endswith(".css") or request.url.endswith(".js") or "fontawesome" in request.url):
                        payload_size += len(request.response.body)
        # print("{} : {:.2f}%".format(website_name, len(all_imgs)/nr_of_external_images*100))

        # if payload_size == 0:
        #     print(driver.requests[-10:])
    
    access_times[website_name] = time.time() - timer
    unfiltered_percentages[website_name] = unfiltered_percentage
    payload_sizes[website_name] = payload_size / 1000 # in kilobytes
    print("\u2713", website_name, payload_size/1000, "kB", access_times[website_name], "s")


def test_websites(browser):
    global unfiltered_percentages, access_times, payload_sizes, driver, PORT
    # PORT = 8899
    # access_times = {website_names[website] : -1 for website in WEBSITES}
    # unfiltered_percentages = {website_names[website] : -1 for website in WEBSITES}
    # payload_sizes = {website_names[website] : 0 for website in WEBSITES}
    # driver = get_driver(browser)
    # excel_row_index = 0
    # for website in WEBSITES:
    #     test_website(website)
    #     website_name = website_names[website]

    #     # save the access times and unfiltered percentages to a xlsx file
    #     # the website name, access time and unfiltered percentage all go in the same row
    #     excel = pd.read_excel("client/test_results/filtered_{}_test_results.xlsx".format(browser))
    #     new_row = [website_name, unfiltered_percentages[website_name], access_times[website_name], payload_sizes[website_name]]
    #     excel.loc[excel_row_index] = new_row
    #     excel_row_index += 1

    #     excel.to_excel("client/test_results/filtered_{}_test_results.xlsx".format(browser), index=False)

    # print("\u2713", "filtered_{} excel written\n".format(browser))
    # driver.close() # close the driver
    PORT = 7777
    access_times = {website_names[website] : -1 for website in WEBSITES}
    unfiltered_percentages = {website_names[website] : -1 for website in WEBSITES}
    payload_sizes = {website_names[website] : 0 for website in WEBSITES}

    excel_row_index = 0
    driver =  get_driver(browser)
    for website in WEBSITES:
        test_website(website)
        website_name = website_names[website]
        excel = pd.read_excel("client/test_results/unfiltered_{}_test_results.xlsx".format(browser))
        new_row = [website_name, unfiltered_percentages[website_name], access_times[website_name], payload_sizes[website_name]]
        excel.loc[excel_row_index] = new_row
        excel_row_index += 1
        excel.to_excel("client/test_results/unfiltered_{}_test_results.xlsx".format(browser), index=False)
        # driver.delete_all_cookies()

    driver.quit()
    print("\u2713", "unfiltered_{} excel written\n".format(browser))
    
        
# browsers = ['chrome', 'firefox', 'safari', 'edge']
browsers = ['chrome', 'firefox', 'edge']
for browser in browsers:
    test_websites(browser)

    