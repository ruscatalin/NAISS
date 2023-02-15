# use pandas to read the publisher-database.xlsx file
# for each column, count the number of papers that are published by that publisher

import pandas as pd

excel = pd.read_excel('publisher-database.xlsx')

results = {publisher: 0 for publisher in excel.columns}

for publisher in excel.columns:
    results[publisher] = excel[publisher].count()

# sort the results by the number of papers
results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}

# let's plot the results
import matplotlib.pyplot as plt

plt.figure(figsize=(18, 5))
plt.bar(results.keys(), results.values())


for i, v in enumerate(results.values()):
    plt.text(i, v, str(v), color='black', fontweight='bold')

plt.savefig('publisher-distribution.png')