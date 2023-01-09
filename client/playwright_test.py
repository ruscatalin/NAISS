# pip install playwright
# playwright install

import re
from playwright.sync_api import Page, expect

HOSTNAME = "localhost"
PORT = 7777
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


def test_website(page: Page):
    for website in WEBSITES:
        page.goto("{}{}".format(ADDRESS, website))
        print("Checking out", website)

        # get all the images
        all_images = page.query_selector_all("img")

        # all_images = page.get_by_role("img")
        # print(all_images)
        # expect(all_images).to_be_visible()

