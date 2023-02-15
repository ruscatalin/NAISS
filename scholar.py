# We use the scholarly library to perform a systematic literature review.
# The found papers will be filtered first on whether they are relevant to our exposed challenges.
# We will learn whether the papers are relvant by analysing the abstract, title and keywords. For this, GPT3 will be used.

"""
The following search terms should be used. Note that round brackets signify interchangeable terms.
[blocking] image steganography e-commerce
(malicious/compromised/untrusted) (hosting providers##/payment gateway##) e-commerce
(e-skimmer/##skimming##/magecart) (##attacks##/defense) e-commerce
(image/html) authentication
end to end (integrity/authenticity) e-commerce
secure web application [host]
secure code (distribution/poisoning)
##(##card/##credential) sniffing##
web skimmer filter
code injection (defense/prevention)
"""

search_terms = [
    "blocking image steganography e-commerce",
    "malicious hosting providers e-commerce",
    "compromised hosting providers e-commerce",
    "untrusted hosting providers e-commerce",
    "MageCart defense e-commerce",
    "e-skimmer defense e-commerce",
    "image authentication",
    "html authentication",
    "end to end integrity e-commerce",
    "end to end authenticity e-commerce",
    "secure web application host",
    "secure code distribution",
    "secure code poisoning",
    "web skimmer filter",
    "code injection defense",
    "code injection prevention"
]

from serpapi import GoogleSearch  # pip install google-search-results
import requests
import pandas as pd

results = {
    search_term: {'title': [], 'link': [], 'result id':[], 'bibtex': []} for search_term in search_terms
}

params = {
    "engine": "google_scholar",
    'as_ylo': 2002,     # only papers from 2002 onwards
    "lr": "lang_en",    # only English results
    "num": 20,          # 20 results per search term (2 pages of results)
    "as_sdt": 7,        # include patents
    "q": "",
    "api_key": "73bfeb7e2fe3d58294a222e86620425abce3a745b0f6d5a308cedb0456b815e4"
}


# for search_term in search_terms:
#     params['q'] = search_term
#     search = GoogleSearch(params)
#     search_results = search.get_dict()
#     try:
#         print(search_term, len(search_results['organic_results']))
#     except KeyError:
#         print(search_term, 0)
#         continue
#     # We now collect the title, abstract (called snippet in serpapi) and the link from the 'organic results'
#     for result in search_results['organic_results']:
#         results[search_term]['title'].append(result['title'])
#         # abstract = result['snippet'].replace('\u2026', '')
#         # abstract = abstract.replace('\u2022', "")
#         # abstract = abstract.replace('\u201c', "")
#         # abstract = abstract.replace('\u201d', "")
#         # abstract = abstract.replace('\u2019', "'")
#         # abstract = abstract.replace('\u2010', "-")
#         # abstract = abstract.replace('\u2014', " ")
#         # results[search_term]['abstract'].append(abstract)
#         try:
#             results[search_term]['link'].append(result['link'])
#         except KeyError:
#             results[search_term]['link'].append('No link')
#         results[search_term]['result id'].append(result['result_id'])

# # write each search term and its results to a new line
# excel_row_index = 0
# for search_term in search_terms:
#     excel = pd.read_excel('unfiltered.xlsx')
#     new_row = [search_term, results[search_term]['title'], results[search_term]['abstract'], results[search_term]['link'], results[search_term]['result id'], results[search_term]['bibtex']]
#     excel.loc[excel_row_index] = new_row
#     excel_row_index += 1
#     excel.to_excel('unfiltered.xlsx', index=False)

# try to save results as a json with pretty print
import json
# with open('unfiltered.json', 'w') as fp:
#     json.dump(results, fp, indent=4)

# read the json file
# with open('unfiltered.json', 'r') as fp:
#     results = json.load(fp)

# use openai to figure out whether or not the paper is relevant
# import openai

# openai.api_key = "sk-****************************************"
# engine = "text-davinci-003"

# for search_term in search_terms:
#     # search titles from the last to the first using index
#     for i in range(len(results[search_term]['title']) - 1, -1, -1):
#         prompt = "Determine whether the following paper/article/book/patent addresses the challenge of e-skimmers/MageCart threats that are hidden (with steganography) inside images on e-commerce platforms. Another difficult aspect of this challenge is that those malicious images can be injected into web hosting provider's storage." + "\
#         The given paper has the title \"{}\". Its abstract snippet (taken from Google Scholar) is \"{}\"".format(results[search_term]['title'][i], results[search_term]['abstract'][i]) + "\
#         Is the given paper/book/patent relevant to the challenge above (taking into consideration the title and the abstract snippet)? Answer with ONLY yes/no:"
#         response = openai.Completion.create(engine=engine, prompt=prompt)
#         text = response['choices'][0].text.lower().replace('\n', '')
#         print(i, text)
        
#         if 'yes' in text:
#             # now get its bibtex data from Google Scholar
#             result_id = results[search_term]['result id'][i]
#             params['q'] = result_id
#             params['engine'] = "google_scholar_cite"
#             search = GoogleSearch(params)
#             bibtex_url = search.get_dict()['links'][0]['link']
#             r = requests.get(bibtex_url)
#             r = r.text
#             print(r)
#             results[search_term]['bibtex'].append(r)
#         elif 'no' in text:
#             results[search_term]['title'].pop(i)
#             results[search_term]['abstract'].pop(i)
#             results[search_term]['link'].pop(i)
#             results[search_term]['result id'].pop(i)
        

# with open('filtered.json', 'w') as fp:
#     json.dump(results, fp, indent=4)

# OpenAI doesn't work that well since the abstract is too small, so we'll just work manually
# The links that will have a ! at their start are the ones that we'll discard

with open('unfiltered.json', 'r') as fp:
    results = json.load(fp)
    count = 0
    for term in results:
        for i in range(len(results[term]['title']) - 1, -1, -1):
            if results[term]['link'][i].startswith('!') or results[term]['link'][i].startswith('No link'):
                results[term]['title'].pop(i)
                results[term]['link'].pop(i)
                results[term]['result id'].pop(i)
        count += len(results[term]['title'])
    print('Total works after filtering:', count)

    count = 0
    titles = []
    # Now, let's remove the duplicates
    for term in results:
        # collect all the titles
        titles.extend(results[term]['title'])
    
    # identify the duplicates
    duplicates = []
    for i in range(len(titles) - 1):
        for j in range(i + 1, len(titles)):
            if titles[i] == titles[j]:
                duplicates.append(titles[i])
    
    print("Number of duplicates:", len(duplicates))

    count = 0
    # remove the duplicates
    for term in results:
        for i in range(len(results[term]['title']) - 1, -1, -1):
            if results[term]['title'][i] in duplicates:
                title = results[term]['title'][i]
                results[term]['title'].pop(i)
                results[term]['link'].pop(i)
                results[term]['result id'].pop(i)
                duplicates.remove(title)
        count += len(results[term]['title'])

    print('Total works after removing duplicates:', count)
        

with open('filtered.json', 'w') as fp:
    json.dump(results, fp, indent=4)
