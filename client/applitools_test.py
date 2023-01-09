import os
import pytest

from applitools.selenium import *  # pip install eyes-selenium
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


API_KEY = "uIV100HcDNZqxH9KCPW6UV102103tvwOv109mpzvo7yBj104lz2Mk110"

HOSTNAME = "localhost"
PORT = 8899
ADDRESS = "{}:{}/".format(HOSTNAME, PORT)
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

@pytest.fixture(scope='session')
def api_key():
    return API_KEY

@pytest.fixture(scope='session')
def headless():
  """
  Reads the headless mode setting from an environment variable.
  Uses headless mode for Continuous Integration (CI) execution.
  Uses headed mode for local development.
  """
  h = os.getenv('HEADLESS', default='false')
  return h.lower() == 'false'

@pytest.fixture(scope='session')
def batch_info():
  """
  Creates a new batch for tests.
  A batch is the collection of visual checkpoints for a test suite.
  Batches are displayed in the dashboard, so use meaningful names.
  """
  return BatchInfo("Example: Selenium Python pytest with the Classic runner")

@pytest.fixture(scope='session')
def configuration(api_key: str, batch_info: BatchInfo):
  """
  Creates a configuration for Applitools Eyes.
  """

  # Construct the object
  config = Configuration()

  # Set the batch for the config.
  config.set_batch(batch_info)

  # Set the Applitools API key so test results are uploaded to your account.
  # If you don't explicitly set the API key with this call,
  # then the SDK will automatically read the `APPLITOOLS_API_KEY` environment variable to fetch it.
  config.set_api_key(api_key)

  # Return the configuration object
  return config
  
@pytest.fixture(scope='session')
def runner():
  """
  Creates the classic runner.
  After the test suite finishes execution, closes the batch and report visual differences to the console.
  Note that it forces pytest to wait synchronously for all visual checkpoints to complete.
  """
  run = ClassicRunner()
  yield run
  print(run.get_all_test_results())

@pytest.fixture(scope='function')
def webdriver(headless: bool):
  """
  Creates a WebDriver object for Chrome.
  After the test function finishes execution, quits the browser.
  """
  options = ChromeOptions()
  options.headless = headless
  driver = Chrome(options=options)
  yield driver
  driver.quit()


@pytest.fixture(scope='function')
def eyes(
  runner: ClassicRunner,
  configuration: Configuration,
  webdriver: Chrome,
  request: pytest.FixtureRequest):
  """
  Creates the Applitools Eyes object connected to the ClassicRunner and set its configuration.
  Then, opens Eyes to start visual testing before the test, and closes Eyes at the end of the test.
  """

  eyes = Eyes(runner)
  eyes.set_configuration(configuration)

  eyes.open(
    driver=webdriver,
    app_name='ACME Bank Web App',
    test_name=request.node.name,
    viewport_size=RectangleSize(1024, 768))
  
  yield eyes
  eyes.close_async()

def test_website(webdriver: Chrome, eyes: Eyes):
  # define the strict match that websites will be compared against using eyes
  eyes.set_match_level(MatchLevel.STRICT)

  for website in WEBSITES:
    webdriver.get("{}{}".format(ADDRESS, website))
    # check if the images are visible on the website
    all_imgs = webdriver.find_elements(By.TAG_NAME, "img")
    all_links = webdriver.find_elements(By.TAG_NAME, "link")
    all_favicons = [link for link in all_links if link.get_attribute("rel") == "icon"]
    all_imgs.extend(all_favicons)
    # cut the website/{clean/stego} part of the website from the website
    website = website.split("/")[2][0]
    # print("{} : {}".format(website, len(all_imgs)))

    # use eyes to check whether all images are visible
    eyes.check(Target.window().fully().layout())
    

  
  # webdriver.get("{}{}".format(ADDRESS, WEBSITES[0]))

  # check if the images are visible on the website
  # all_imgs = webdriver.find_elements(By.TAG_NAME, "img")
  
  # eyes.check(Target.window().fully().ignore(all_imgs))

# options = ChromeOptions()
# options.headless = headless
# driver = Chrome(options=options)

