import datetime
from selenium.webdriver.common.by import By
from seleniumwire import webdriver # pip install selenium-wire
import time
import pandas as pd
import openpyxl

HOSTNAME = "localhost"  # assuming you are running the server on the same machine
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
    match which_one:
        case "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            return webdriver.Chrome(executable_path='client/chromedriver_mac_arm64/chromedriver', chrome_options=options)
        case "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            return webdriver.Firefox(options=options)
        case "edge":
            options = webdriver.EdgeOptions()
            options.add_argument('--headless')
            return webdriver.Edge(executable_path='client/edgedriver_mac64_m1/msedgedriver', options=options)

website_names = {website: website.split("/")[2:][0].split(".")[0] for website in WEBSITES}

def test_website(website):
    """
    Access a website and collect the following information:
        - the time it took to load the website
        - the transfered payload size
        - the number of images that were loaded (unfiltered)

    Parameters:
        website (str): the URL of the website to be accessed
    """
    global PORT

    ADDRESS = "http://{}:{}/".format(HOSTNAME, PORT)
    website_name = website_names[website]
    payload_size = 0
    timer = time.time()
    driver.get("{}{}".format(ADDRESS, website))  # load the website

    access_times[website_name] = time.time() - timer
    website_requests = driver.requests
    
    if "internal" in website: # these are the internally-loading websites
        requests = {200: [], 301: [], 400: [], 404: [], 420: [], 500: []}
        img_requests = 0
        
        for request in website_requests:
            # only count the image requests for 'internal' websites
            if request.url.endswith(".png") or request.url.endswith(".jpg") or request.url.endswith(".ico"):
                img_requests += 1

            if  request.response:
                if request.response.status_code == 200:  # only count the payload size for 200 responses (successful requests)
                    payload_size += len(request.response.body)
                                    
                request_response = request.response.status_code
                requests[request_response].append(request.url)

        for response_code in requests.keys():
            if response_code == 420:  # 420 is the custom response given by the NAISS filter to denied image requests
                if len(requests[420]) == 0:
                    unfiltered_percentage = 100
                else:
                    unfiltered_percentage = (1 - (len(requests[420]) / img_requests)) * 100
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

        for request in website_requests:
            if request.response:
                response_code = request.response.status_code
                if  response_code == 200:
                    payload_size += len(request.response.body)
        # print("{} : {:.2f}%".format(website_name, len(all_imgs)/nr_of_external_images*100))
    
    unfiltered_percentages[website_name] = unfiltered_percentage
    payload_sizes[website_name] = payload_size / 1000 # in kilobytes
    print("\u2713", website_name, payload_size/1000, "kB", round(access_times[website_name], 3), "s")


def run_repetitions(repetitions, browser, unfiltered=False):
    """
    Run the test for a browser a certain number of times. Save the results in an excel file.
    The excel file is named {filtered/unfiltered}_{browser}_test_results.xlsx, where {filtered/unfiltered} is whether the websites were accessed through the NAISS filter or not.
    Each repetition is saved in a separate sheet, named run_{repetition_number}.

    Parameters:
        repetitions (int): the number of times the test should be run
        browser (str): the browser to be used for the test
        unfiltered (bool): whether the websites should be accessed through the NAISS filter or not
    """
    global unfiltered_percentages, access_times, payload_sizes, driver

    access_times = {website_names[website] : -1 for website in WEBSITES}
    unfiltered_percentages = {website_names[website] : -1 for website in WEBSITES}
    payload_sizes = {website_names[website] : 0 for website in WEBSITES}

    uf = "un" if unfiltered else ""

    for repetition in range(repetitions):
        print('---- Repetition {} ---- {}'.format(repetition+1, time.strftime("%H:%M", time.localtime())))
        excel = openpyxl.load_workbook("client/test_results/{}filtered_{}_test_results.xlsx".format(uf, browser))
        sheet = excel['run_{}'.format(repetition+1)]
        sheet.delete_rows(2, sheet.max_row)
        for website in WEBSITES:
            driver = get_driver(browser)
            test_website(website)  # collect the data for the current website
            website_name = website_names[website]
            new_row = [website_name, unfiltered_percentages[website_name], access_times[website_name], payload_sizes[website_name]]
            sheet.append(new_row) 
            driver.quit()
        excel.save("client/test_results/{}filtered_{}_test_results.xlsx".format(uf, browser))

    print("\u2713", "{}filtered_{} excel written\n".format(uf, browser))

def test_websites(browser):
    """
    Access all the websites using a given browser and write the collected data to an excel file.
    The access is done twice: once with the NAISS filter and once without it.

    Parameters:
        browser (str): the browser to be used for accessing the websites
    """
    global unfiltered_percentages, access_times, payload_sizes, driver, PORT

    repetitions = 10 # we are going to use this to collect multiple data points for each website

    PORT = 8899  # the port on which the NAISS filter is running (filtered connection)
    run_repetitions(repetitions, browser)

    PORT = 7777
    run_repetitions(repetitions, browser, True)
    

# test the websites using all the browsers
browsers = ['chrome', 'firefox', 'edge']
for browser in browsers:
    test_websites(browser)

    