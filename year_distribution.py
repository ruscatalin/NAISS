# we look into lit.bib and find the year of each paper
# we then plot the distribution of the years

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

years = {'{}'.format(year) : 0 for year in range(2002, 2023)}


# read lit.bib
with open('lit.bib', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if 'year' in line:
            # get what is between the curly brackets
            year = line.split('{')[1].split('}')[0]
            years[year] += 1

# plot the years as a dot graph
plt.figure(figsize=(18, 5))
plt.plot(years.keys(), years.values())
# plot a trendline
values = np.array(list(years.values()))
z = np.polyfit(range(2002, 2023), values, 1)
p = np.poly1d(z)
plt.plot(p(range(2002, 2023)), 'r--')
# show a legend
plt.legend(['Number of papers', 'Trendline'])
# show the number of papers on the graph
for i, v in enumerate(years.values()):
    plt.text(i, v, str(v), color='black', fontweight='bold')

plt.title('Year distribution of papers')

plt.savefig('year-distribution.png')