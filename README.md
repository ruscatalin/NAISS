# NAISS: Network Authentication of Images to Stop e-Skimmers

Source code for [NAISS: Network-Authentication of Images to Stop e-Skimmers](https://essay.utwente.nl/94962/).

## Abstract
The rise of payment details theft has led to increasing concerns regarding the security of e-commerce platforms. For the MageCart threat family, the attacks employ e-skimmers, which are pieces of software code that instruct clients to forward payment details to an attacker-controlled server. They can be injected into hosting providers’ servers as HTML tags such as script, iframe, and img. By leveraging image steganography - the technique of hiding structured information inside images without visual perturbances - MageCart groups can deliver e-skimmers without raising any suspicion. In this report, we system- atically review applicable solutions in the literature and evaluate their drawbacks in the setting of a compromised hosting provider. While promising, existing solutions in the lit- erature present shortcomings such as lack of compatibility, adoptability or functionality under the presence of an attacker. Based on this review, we compile a set of features for a better solution, which we use as a foundation for designing our proposed solution - NAISS: Network Authentication of Images to Stop e-Skimmers. Through our solution, digital signa- tures of individual images are checked inside a server-side middlebox residing in the hosting provider’s network to prevent the transmission of unauthorized images to clients. The sig- natures are provided by the e-commerce platform developer prior to uploading a website to the hosting provider. Our proof-of-concept implementation shows that NAISS is capable of filtering 100% of present stegoimages, regardless of their novelty, while imposing a minimal performance detriment and no client-side modifications.

## Table of contents
1. [Installation](#installation)
    1. [Prerequisites](#prerequisites)
    2. [Setup](#setup)
2. [Usage](#usage)
    1. [Making stegoimages](#making-stegoimages)
    2. [Making (unsigned) websites](#making-unsigned-websites)
    3. [Signing websites](#signing-websites)
    4. [Generating new keys](#generating-new-keys)
    5. [Running the webserver and the NAISS filter](#running-the-webserver-and-the-naiss-filter)
    6. [Running client tests](#running-client-tests)
    7. [Plotting](#plotting)

## Installation
### Prerequisites
- Python 3.7.0 for generating stegoimages using SteganoGAN
- (Ideally) Python 3.10.6 for everything else
- Docker for running the webserver and the NAISS filter/reverse proxy

### Setup
1. Clone the repository: `git clone https://github.com/ruscatalin/NAISS.git`.
2. `cd NAISS`.
3. Install the requirements using `pip install -r requirements.txt`. Use `pip3 install -r requirements.txt` if you use Linux or MacOS. To use pip for a specific version of Python, use `<path_to_python_executable> -m pip install -r requirements.txt`.

## Usage
### Making stegoimages
While in the root of the project, run the `makestegos.py` script (located inside `utils/`). It uses the images inside `server/website/images/` to embed a payload in each of them. It will generate and save the stegoimages in the `server/website/images/stegoimages` directory. Remember that the script needs to be run with Python 3.7.0, so point to the correct executable if you have multiple versions of Python installed.

### Making (unsigned) websites
While in the root of the project, run the `makewebsites.py` script (located inside `utils/`). Make sure that for externally-loaded images, the `img.xlsx` file is prepared with the correct URLs and names. The script will generate and save the websites in the `server/website/websites/{clean/stego}` directory, depending on whether or not the website in question contains stegoimages or not. 

The html files will be names as follows: `nosig_{clean/stego}_{external/internal}_{jpg/png}_index.html`. The `nosig` part is because the websites are unsigned; `clean/stego` refers to whether or not the website contains stegoimages; `external/internal` refers to whether or not the images are loaded from an external source (e.g. hosted on imgur.com); and `jpg/png` refers to the format of the images being used.

### Signing websites
In order to sign the unsigned websites, run the `multi_signer.py` script (this too is located inside `utils/`). It uses two keys: an assumed 'good' key and an 'evil' one (the latter is presumed to be of an attacker). The script will generate and save the signed websites in the `server/website/websites/{clean/stego}` directory. The websites will be appended with `sig` or `evilsig` instead of `nosig`, depending on which key was used to sign the images. Remember to move `public_key.pem` inside the `filter/` directory in order to provide the NAISS filter with the correct public key.

### Generating new keys
In order to generate new (Eliptic Curve) keys, inspect the `sign.py` script (located inside `utils/`) and uncomment a specific code block in the main function. Then, just simply run the script to generate and save the key files. The keys are saved inside `utils`.

### Running the webserver and the NAISS filter
If using MacOS, simply run `docker compose up` while in the root folder of the project. If using some other OS, inspect the bottom of the `docker-compose.yaml` and change the driver of the 'naiss' network.

Now the webserver should be accessible at `localhost:7777/websites/` and the NAISS reverse proxy at `localhost:8899/websites/`. One can now manually navigate to the desired website variant.

### Running client tests
While in the root of the project, run `python3 client/selenium_test.py`. Results will be saved in the `client/test_results` directory as excel files. The excel files will be named as follows: `{filtered/unfiltered}_{chrome/edge/firefox}_test_results.xlsx`. Here `filtered` refers to whether or not the website was accessed through the NAISS filter, and `chrome/edge/firefox` refers to the browser used to run the tests.

### Plotting
While in the root of the project, run `python3 client/visualise.py`. The script will use all the data from the tests to generate and save the plots in `client/test_results/` as png images. The plots are of different types:
- comparison of the pixel and byte size of the clean and stegoimages
- comparison of the images that arrived at the client, based on whether the right key was used or not
- average time taken (in seconds) to load the images, based on all the categories our tests and websites have: `sig/nosig/evilsig`, `clean/stego`, `external/internal`, `jpg/png`, `chrome/edge/firefox` and `filtered/unfiltered`
- average transferred payload size (in kilobytes) of the websites, aggregated by the same categories as above
