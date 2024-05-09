## News articles web scraping query code, by: Luis Miguel Leon Gil
## SSL Troubleshoot for my MacOS computer that does not have updated SSL certificates, you can comment lines form 5 to 10 if you have updated SSL certificates.
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download()
nltk.download('punkt')

## We setup our workspace by importing the installed libraries from the requirements file.
import newspaper
from newspaper import Article
import django
import datetime
import os
import re

## We need to set the django settings by default so we can use Django's Object Relational Mapper (ORM) to migrate pyhthon objects from this script to our Django models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myproject.settings")
django.setup()
## Now we import my app's models
from News_Articles.models import News_Article, Author, Category

## For this excercise I've selected the CNN news portal since their news articls meet with all the information requirements given in the assignment.
news_portal = 'https://www.cnn.com'

## By using the build function we initialize a news source object that will help us extracting news articles' relevant data, we store this information in the object news_papers.
news_papers = newspaper.build(news_portal,memoize_articles=False) ## We include memoize_articles to keep the cache from all previously extracted articles everytime we run the script.

## We check the amount of articles extracted from the source
print('News articles extracted from source: '+ str(news_papers.size()))

## For each News Article extracted from the news portal we will extract its URL. 
## CNN URLs are consistent: after .com/ or .com/YYYY/MM/DD/ we can find a category keyword for the news article presented. 
## We will take advantage of this structure to extract and assign a News category to each news article URL.
 
dict_urls = {}
dict_cats = {}
a = 0
## We proceed to store the url and category of each news article in a corresponding dictionary
for article in news_papers.articles:
    ## Extracting News article URL
    dict_urls[a] = article.url
    ## Extracting and assiging a category to each article
    ## We need to determine if the URL is built with the .com/category/ or .com/YYYY/MM/DD/category/ form
    match = re.search(r".com\/(\d{4})\/(\d{2})\/(\d{2})\/", dict_urls[a])
    if match:
        parts = dict_urls[a].split("/")
        for p in range(len(parts)):
            if parts[p].endswith(".com"):
                pos = p+4
        dict_cats[a] = parts[pos]
    else:
        parts = dict_urls[a].split("/")
        for p in range(len(parts)):
            if parts[p].endswith(".com"):
                pos = p+1
        dict_cats[a] = parts[pos]
    a = a+1

## Sometimes we get many news articles so to keep the task manageable we limit the urls to a maximum number and select the first ones that meet said quantity from the list.
Max_articles = 100

new_dict_urls = []
new_dict_cats = []
if len(dict_urls) > Max_articles:
    for val in range(Max_articles):
        new_dict_urls.append(dict_urls[val])
        new_dict_cats.append(dict_cats[val])
else:
    for val in range(len(dict_urls)):
        new_dict_urls.append(dict_urls[val])
        new_dict_cats.append(dict_cats[val])

## After getting our list of news articles URLs we can make use of newspaper3k library to extract complementary information of each URL (when availabe) such as authors, publish date, title, summary, text content, html content, etc.
## To do so, we first create an article object by using the class Article and then proceed to use the functions download, parse and nlp to be able to extract out the complementary properties of each news article.
## We then store the desired data in a unique dictionary position (dict).
## Bear in mind that sometimes we can get errors using newspaper3k library such as exceeding the limit of queries in an specific news portal, or being unable to get information from an specific URL.
## To troubleshoot this, I have included a try-except rule so the extraction process does not finish abruptly.

Author_name = []
dict = []
for url in range(len(new_dict_urls)):
    try:
        art = Article(new_dict_urls[url])
        art.download()
        art.parse()
        art.nlp()
        ## The following lines are used to extract the main author information from the News articles and then, complement it with a job description of said author
        ## To do this we will take advantage of CNN news Web portal structure again. 
        ## Most of the News Articles main authors (the first author on the News Article) appear in a CNN profile webpage with the form https://edition.cnn.com/profiles/name-surname'. 
        ## I found this characteristic extra useful, so we will replace the name and surname fields with the corresponding author information and scrap their job description from their profile page.
        ## We take the author string extracted from the article and remove leading or trailing whitspaces, put all word in lowercase and replace blank spaces with '-'
        auth = art.authors[0].strip().lower().replace(" ", "-")
        
        ## Now we scrap the information from the CNN profile page 
        au_bio = Article('https://edition.cnn.com/profiles/'+auth)
        au_bio.download()
        au_bio.parse()
        
        ## If we get no published_date for the news article, we set a default date of '1999-01-01' so the parameter meets with the django model
        if (art.publish_date==None):
            pub = 'no'
            pub_date = datetime('1999/01/01')
        else:
            pub= 'yes'
            pub_date = art.publish_date
        
        ## Finally we store the News Article's relevant information in our dictionary for future storage in our Django Database
        dict.append({'author':au_bio.text[7:].replace("\n\n", " "), 'title': art.title, 'summary': art.summary, 'text': art.text, 'html': art.html, 'category': new_dict_cats[url], 'published': pub, 'published date': pub_date, 'url': new_dict_urls[url]})
        Author_name.append({'author':art.authors[0]})
    except :
        pass

## We check the new amount of articles extracted from the source
print('number of news obtained '+ str(len(dict)))

## Finally we will identify the unique authors and categories from our final News article list, we will store this unique elements in corresponding dictionaries
authors = []
categories = []
for n in range(len(dict)):
    authors.append(Author_name[n]['author'])
    categories.append(dict[n]['category'])

## We build a function that extracts the unique authors and categories from the whole list of articles
def get_unique_values(Original_list):
  unique_values = set()
  for item in Original_list:
    if isinstance(item, str):
      unique_values.add(item)
    elif isinstance(item, list):
      unique_values.update(get_unique_values(item))
  return list(unique_values)

unique_authors = get_unique_values(authors)
unique_cats = get_unique_values(categories)

## We then migrate the News articles information we just captured into instances of the models News_Article, Author and Category of our App

for n in range(len(dict)):
    paper = 0
    paper = News_Article()
    paper.title = dict[n]['title']
    paper.summary = dict[n]['summary']
    paper.content = dict[n]['html']
    paper.published = dict[n]['published']
    paper.pub_date = dict[n]['published date']
    paper.category = dict[n]['category']
    paper.author = dict[n]['author']
    paper.link = dict[n]['url']
    paper.save()

author = Author()
author.Uni_author = unique_authors
author.save()

category = Category()
category.category = unique_cats
category.save()
