# Introduction
The goal here is to crawl and scrape DataCamp's tutorials page and extract meaningful information which can be saved for later and analyzed.
The website is scraped using python's BeautifulSoup package.
# Methodology
Before begining the scraping it was important to understand the underlying structure of the webpage and to codify the information using xpaths for both understanding and telling the program what to look for while crawling.
To understand the page structure, Chrome browser developer tools was used. After quickly glancing over the html structure the use of classes in the html tags was apparent, these classes are precise what enabled easy of crawling and extraction of the webpage.
The following information is scraped from the page:
1.Author
2.Publish Date
3.Title
4.Description
5.Up Votes
The sample URL that is used to loop and scrape is the following https://www.datacamp.com/community/tutorials?page=2. The page=2 argument changes for each page. In order to loop through all the pages to get the necessary dataset, we need to find out the number of pages.
```
pages = [i.text for i in soup.find_all('a') if 'community/tutorials?page' in str(i)]
lastpage = pages[-1]
```
In the above code a list of page number was comprehened by finding all a tags in the webpage which had *"community/tutorials?page"* in it and then the last element was accessed.
Next the acutal process of Scraping begins:
```
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
 ```
 In the code above alot of things are happening so lets break it down to 2 major portions the crawling and the extraction ingoring the for loop which facilitates us in crawling all the pages from 1 to the last page which during the time of writing was 29.
 
First the url is stored in the variable url which is then passed to the urlopen() to fetch the url which returns the html contents of the url which is then passed to BeautifulSoup which returns a object which is a special type of list.(It is easier to think of it like a file handle)
 ```
    url = f"https://www.datacamp.com/community/tutorials?page={cp}"
    print(url)
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
```
The next section appends the data extracted from various tags(more about it in a bit) into apt lists created beforehand.
The way to find the data is to use the soup object to parse the html and find tag in which the piece if information is stored , luckly DataCamps website uses React and hence has convinient class names to help us extract the data.The classes where figured about by using Chrome's dev tools.
```
description.append([i.text for i in soup.find_all(class_='jsx-2625178925 blocText description')])
    upvote.append([i.text for i in soup.find_all(class_='jsx-1727309017 voted')])
    author.append([i.text for i in soup.find_all(class_='jsx-886169423 name')])
    publishdate.append([i.text for i in soup.find_all(class_='jsx-886169423 date')])
    title.append([i.text for i in soup.find_all(class_='jsx-2625178925 blue')])
```
![](https://github.com/architpai/Crawler_using_BeautifulSoup_tut/blob/main/Screenshots/ss1.png)
Once we have looped through all the pages we end up with all the information we need but in form of a list of lists and hence they needed to he flatened
simple list comprehension was used to achieve the same. The newly generated lists where then stored in a dictionary.
```
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
```
**Note:** The extracted published date was in string format was had be converted into DateTime before behind fed in to the dictionary
Then a Pandas Dataframe is generated using the dictionary which is then exported into a .csv file for future use.
![](https://github.com/architpai/Crawler_using_BeautifulSoup_tut/blob/main/Screenshots/ss2.png)

