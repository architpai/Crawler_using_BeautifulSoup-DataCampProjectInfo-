# Imports

import pandas as pd
from datetime import datetime
import re
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup

# html object of given url is created and passed to BeautifulSoup
url = "https://www.datacamp.com/community/tutorials"
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

# Identified all hyperlinks on the page using list comprehension
# and filtered for those having community/tutorials?page= in it
pages = [i.text for i in soup.find_all('a') if 'community/tutorials?page' in str(i)]
lastpage = pages[-1]

description = []
upvote = []
author = []
publishdate = []
title = []
# Scrape
for cp in np.arange(1, int(lastpage) + 1):
    url = f"https://www.datacamp.com/community/tutorials?page={cp}"
    print(url)
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    description.append([i.text for i in soup.find_all(class_='jsx-2625178925 blocText description')])
    upvote.append([i.text for i in soup.find_all(class_='jsx-1727309017 voted')])
    author.append([i.text for i in soup.find_all(class_='jsx-886169423 name')])
    publishdate.append([i.text for i in soup.find_all(class_='jsx-886169423 date')])
    title.append([i.text for i in soup.find_all(class_='jsx-2625178925 blue')])
# Flattening List of lists
descriptionflat = [y for x in description for y in x]
upvoteflat = [y for x in upvote for y in x]
authorflat = [y for x in author for y in x]
publishdateflat = [y for x in publishdate for y in x]
titleflat = [y for x in title for y in x]
# Formatting date from string to DateTime
publishdateformatted = [
    datetime.strptime(re.sub('rd, ', ', ', re.sub('st, ', ', ', re.sub('nd, ', ', ', re.sub('th, ', ', ', a)))),
                      "%B %d, %Y") for a in publishdateflat]
cdata = {"author": authorflat, "publishdate": publishdateflat, "title": titleflat, "description": descriptionflat,
         "upvote": upvoteflat}
# Saving Scraped Data in xlsx format
df = pd.DataFrame(data=cdata)
df.to_csv("datacampTutCrawl.csv", header=True, index=False)
