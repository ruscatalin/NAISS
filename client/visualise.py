# here we use matplotlib to plot the data we have collected in test_results.xlsx

from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
# import pyplot_themes as themes # pip install pyplot-themes
import pandas as pd
import numpy as np


excel = pd.read_excel("client/test_results.xlsx")

categories = {
    "has_signature": ['sig', 'nosig', 'evilsig'],
    "has_stegoimages": ['clean', 'stego'],
    "image_type": ['external', 'internal'],
    "image_format": ['jpg', 'png']
}

all_categories = []
for category in categories.values():
    all_categories.extend(category)


def plot_unfiltered_percentage_by_signature():
    # plot the unfilitered percentage for each website
    # aggregate sig websites and compare them against aggregated nosig + evilsig websites
    sig_bin = []
    nosig_evilsig_bin = []
    for website in excel['website name']:
        if 'nosig' in website or 'evilsig' in website:
            nosig_evilsig_bin.append(website)
        else:
            sig_bin.append(website)

    sig_unfiltered_percentage = excel.loc[excel['website name'].isin(sig_bin)]['unfiltered percentage'].mean()
    nosig_evilsig_unfiltered_percentage = excel.loc[excel['website name'].isin(nosig_evilsig_bin)]['unfiltered percentage'].mean()

    with plt.style.context('bmh'):
        plt.figure(figsize=(10, 8))
        plt.bar(1, sig_unfiltered_percentage, color='g')
        plt.bar(2, nosig_evilsig_unfiltered_percentage, color='r')
        plt.xticks([1, 2], ['signed', 'no signature + malicious signature'])
        plt.yticks([0, 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        plt.ylabel('Unfiltered percentage')
        plt.title('Unfiltered percentage for signed vs no signature + malicious signature websites')
        plt.show()
        plt.close()

def plot_access_time_by_category():
    bins = {category : [] for category in all_categories}
    for website in excel['website name']:
        access_time = excel.loc[excel['website name'] == website]['access time']

        if 'nosig' in website:
            bins['nosig'].append(access_time)
        elif 'evilsig' in website:
            bins['evilsig'].append(access_time)
        elif 'sig' in website:
            bins['sig'].append(access_time)

        if 'clean' in website:
            bins['clean'].append(access_time)
        elif 'stego' in website:
            bins['stego'].append(access_time)

        if 'external' in website:
            bins['external'].append(access_time)
        elif 'internal' in website:
            bins['internal'].append(access_time)

        if 'jpg' in website:
            bins['jpg'].append(access_time)
        elif 'png' in website:
            bins['png'].append(access_time)

    with plt.style.context('bmh'):
        plt.figure(figsize=(10, 5))
        index = 1
        for category in bins:
            value_to_plot = np.array(bins[category], dtype=object).mean()
            # compute a gradient color based on the value to plot
            gradient_color = mcolors.Normalize(vmin=0, vmax=3.3, clip=True)(value_to_plot)
            gradient_color = plt.cm.Reds(gradient_color)
            plt.bar(index, value_to_plot, color=gradient_color)
            index += 1
        plt.xticks(range(1, len(bins) + 1), bins.keys())
        plt.ylabel('Average access time')
        plt.title('Average access time for each category through NAISS')
        plt.show()
        plt.close()

plot_unfiltered_percentage_by_signature()
# plot_access_time_by_category()