import os
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import pandas as pd
import numpy as np
from PIL import Image


f_chrome_excel = pd.read_excel("client/test_results/filtered_chrome_test_results.xlsx")
f_firefox_excel = pd.read_excel("client/test_results/filtered_firefox_test_results.xlsx")
f_edge_excel = pd.read_excel("client/test_results/filtered_edge_test_results.xlsx")
uf_chrome_excel = pd.read_excel("client/test_results/unfiltered_chrome_test_results.xlsx")
uf_firefox_excel = pd.read_excel("client/test_results/unfiltered_firefox_test_results.xlsx")
uf_edge_excel = pd.read_excel("client/test_results/unfiltered_edge_test_results.xlsx")

excels = {
    "chrome": [f_chrome_excel, uf_chrome_excel],
    "firefox": [f_firefox_excel, uf_firefox_excel],
    "edge": [f_edge_excel, uf_edge_excel],
    "all": [f_chrome_excel, f_firefox_excel, f_edge_excel, uf_chrome_excel, uf_firefox_excel, uf_edge_excel]
}

categories = {
    "has_signature": ['sig', 'nosig', 'evilsig'],
    "has_stegoimages": ['clean', 'stego'],
    "image_type": ['external', 'internal'],
    "image_format": ['jpg', 'png'],
    "browser": ['chrome', 'firefox', 'edge'],
    "is_filtered": ['filtered', 'unfiltered']
}

all_categories = []
for category in categories.values():
    all_categories.extend(category)


def plot_unfiltered_percentage_by_signature():
    # plot the unfilitered percentage for each website
    # aggregate sig websites and compare them against aggregated nosig + evilsig websites
    sig_bin = []
    nosig_evilsig_bin = []
    for excel in excels['all']:
        for website in excel['website name']:
            # find the unfiltered percentage of the website
            uf_percentage = excel.iloc[excel.index[excel['website name'] == website].tolist()[0]]['unfiltered percentage']
            if 'nosig' in website or 'evilsig' in website:
                nosig_evilsig_bin.append(uf_percentage)
            else:
                sig_bin.append(uf_percentage)

    sig_unfiltered_percentage = np.array(sig_bin, dtype=object).mean()
    nosig_evilsig_unfiltered_percentage = np.array(nosig_evilsig_bin, dtype=object).mean()

    with plt.style.context('bmh'):
        plt.figure(figsize=(15, 8))
        plt.bar(1, sig_unfiltered_percentage, color='g')
        plt.bar(2, nosig_evilsig_unfiltered_percentage, color='r')
        plt.xticks([1, 2], ['signed', 'no signature + malicious signature'])
        plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        plt.ylabel('Unfiltered percentage')
        plt.title('Unfiltered percentage for signed vs no signature + malicious signature websites')
        # plt.show()
        plt.savefig('client/test_results/unfiltered_percentage_by_signature.png')
        plt.close()

def plot_measurement_by_category(measurement):
    bins = {category : [] for category in all_categories}
    for browser in excels.keys():
        if browser == 'all':
            continue
        for excel in excels[browser]:
            for website in excel['website name']:
                measure = excel.iloc[excel.index[excel['website name'] == website].tolist()[0]][measurement]
                bins[browser].append(measure)

                if excel is excels[browser][0]:
                    bins['filtered'].append(measure)
                else:
                    bins['unfiltered'].append(measure)

                if 'nosig' in website:
                    bins['nosig'].append(measure)
                elif 'evilsig' in website:
                    bins['evilsig'].append(measure)
                elif 'sig' in website:
                    bins['sig'].append(measure)

                if 'clean' in website:
                    bins['clean'].append(measure)
                elif 'stego' in website:
                    bins['stego'].append(measure)

                if 'external' in website:
                    bins['external'].append(measure)
                elif 'internal' in website:
                    bins['internal'].append(measure)

                if 'jpg' in website:
                    bins['jpg'].append(measure)
                elif 'png' in website:
                    bins['png'].append(measure)

    with plt.style.context('bmh'):
        plt.figure(figsize=(20, 8))
        index = 1
        max_avg = 0
        for category in bins:
            if category == 'all':
                continue
            value_to_plot = np.array(bins[category], dtype=object).mean()
            if value_to_plot > max_avg:
                max_avg = value_to_plot
            # compute a gradient color based on the value to plot
            vmin, vmax = 0, 3
            if measurement == 'size':
                vmin, vmax = -50, 700
            gradient_color = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=True)(value_to_plot)
            gradient_color = plt.cm.Reds(gradient_color)
            plt.bar(index, value_to_plot, color=gradient_color)
            index += 1
        plt.vlines([3.5, 5.5, 7.5, 9.5, 12.5], ymin=0, ymax=1.15*max_avg, color='k', linestyles='dotted', linewidth=1)
        plt.xticks(range(1, len(bins) + 1), bins.keys())
        plt.ylabel('Average {} ({})'.format(measurement, 'kB' if measurement == 'size' else 's'))
        plt.title('Average {} for each category'.format(measurement))
        # plt.show()
        plt.savefig('client/test_results/{}_by_category.png'.format(measurement.replace(' ', '_')))
        plt.close()

def plot_image_size_differences():
    # plot the difference between the clean and stego image sizes from server/website/images
    # the clean images are in the images folder, while the stegoimages are inside images/stegoimages

    # get the clean image sizes
    clean_image_sizes = {"bytes": [], "pixels_width": [], 'pixels_height': []}
    for image in os.listdir('server/website/images'):
        if image.endswith('.jpg') or image.endswith('.png'):
            clean_image_sizes['bytes'].append(os.path.getsize('server/website/images/{}'.format(image)))
            pixels = Image.open('server/website/images/{}'.format(image)).size
            clean_image_sizes['pixels_width'].append(pixels[0])
            clean_image_sizes['pixels_height'].append(pixels[1])

    # get the stego image sizes
    stego_image_sizes = {"bytes": [], "pixels_width": [], 'pixels_height': []}
    for image in os.listdir('server/website/images/stegoimages'):
        if image.endswith('.jpg') or image.endswith('.png'):
            stego_image_sizes['bytes'].append(os.path.getsize('server/website/images/stegoimages/{}'.format(image)))
            pixels = Image.open('server/website/images/stegoimages/{}'.format(image)).size
            stego_image_sizes['pixels_width'].append(pixels[0])
            stego_image_sizes['pixels_height'].append(pixels[1])
    
    # plot the difference between the clean and stego image sizes
    with plt.style.context('bmh'):
        plt.figure(figsize=(15, 8))
        plt.bar(1, np.array(clean_image_sizes['bytes'], dtype=object).mean()/1000, color='orange')
        plt.bar(2, np.array(stego_image_sizes['bytes'], dtype=object).mean()/1000, color='b')
        plt.xticks([1, 2], ['clean images', 'stegoimages'])
        plt.ylabel('Average image size (kB)')
        plt.title('Average image size for clean vs stegoimages with small payload')
        # plt.show()
        plt.savefig('client/test_results/image_differences_bytes.png')
        plt.close()

        plt.figure(figsize=(15, 8))
        plt.bar(1, np.array(clean_image_sizes['pixels_width'], dtype=object).mean(), color='orange')
        plt.bar(2, np.array(stego_image_sizes['pixels_width'], dtype=object).mean(), color='orange')
        plt.bar(3, np.array(clean_image_sizes['pixels_height'], dtype=object).mean(), color='b')
        plt.bar(4, np.array(stego_image_sizes['pixels_height'], dtype=object).mean(), color='b')
        plt.xticks([1, 2, 3, 4], ['clean width', 'stego width', 'clean height', 'stego height'])
        plt.ylabel('Average image size (pixels)')
        plt.title('Average image size for clean vs stegoimages')
        # plt.show()
        plt.savefig('client/test_results/image_differences_pixels.png')
        plt.close()


# plot_unfiltered_percentage_by_signature()
# plot_measurement_by_category('access time')
# plot_measurement_by_category('size')
# plot_image_size_differences()