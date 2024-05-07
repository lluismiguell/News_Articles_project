## News articles web scraping query code, by: Luis Miguel Leon Gil
## SSL Troubleshoot for my MacOS computer that does not have updated SSL certificates
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download()

## We setup our workspace by importing the installed libraries from the requirements file.
from scraparazzie import scraparazzie
import newspaper
from newspaper import Article
import nltk
nltk.download('punkt')
import pandas as pd
import os
import django
import datetime

## We need to set the 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myproject.settings")
django.setup()
# Importing my app's Django models
from News_Articles.models import News_Article, Author, Category

## We pick a news portal to get the news articles from
news_portal = 'http://cnn.com'

## By using the build function we initialize a news source object that helps us extracting categories, feeds, brand and descriptions of news articles, we store this information in the object news_papers.
news_papers = newspaper.build(news_portal)#,memoize_articles=False) ## that last commented part is only included if you don't want to cache all previously extracted articles

## We check the amount of articles extracted from the source
print('News articles extracted from source: '+ str(news_papers.size()))

dict_urls = {}
a = 0
## We proceed to store the url of each news article in a dictionary
for article in news_papers.articles:
    dict_urls[a] = article.url
    a = a+1

## Sometimes we get many news articles and to keep the task manageable we limit the urls to a maximum number and select the first ones that meet said quantity from the list.
Max_articles = 20

new_dict_urls = []
if len(dict_urls) > Max_articles:
    for val in range(Max_articles):
        new_dict_urls.append(dict_urls[val])
else:
    for val in range(len(dict_urls)):
        new_dict_urls.append(dict_urls[val])


dict = []
dict_auth = []
for url in range(len(new_dict_urls)):
    try:
        art = Article(new_dict_urls[url])
        art.download()
        art.parse()
        ## We will make use of this natural language processing function (nlp) to get information such as summary and keywords, which we will use to assign a category to the news article
        art.nlp()
        ## Here we clean and complete data that could be lost from the scrapping method
        ## If we get no published_date for the news article, we set a default date of '1999-01-01' so the parameter meets with the django model
        if (art.publish_date==None):
            pub = 'no'
            pub_date = datetime('1999/01/01')
        else:
            pub= 'yes'
            pub_date = art.publish_date
        ## If we get no author after scrapping the website, we set a Jhon Doe author to meet with the requirement
        if (art.authors==[]):
            auth = 'John Doe, the writer of this article was not identified'
        else:
            auth = ''
            for i in art.authors:
                auth = auth + ' ' + i
        dict.append({'author':auth, 'title': art.title, 'summary': art.summary, 'text': art.text, 'html': art.html, 'category': art.keywords[0], 'published': pub, 'published date': pub_date})
        ## We will try to capture the information of the news article main author by storing the first 2 elements of the authors list
        if (len(art.authors)==0):
            name = 'John Doe'
        else:
            name = art.authors[0]
        dict_auth.append(name)
    except :
        pass

## We check the new amount of articles extracted from the source
print('number of news obtained '+ str(len(dict)))

## We then migrate the News articles information we just captured into instances of the model News_Article of our App

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
    paper.save()

## We determine the unique categories and authors from our article list and migrate them to the models Categories and Authors of our App
## We extract the list of authors and categories from the original article list

categories = []
for n in range(len(dict)):
    categories.append(dict[n]['category'])

## We build a function that extracts the unique authors and categories from the News Articles list
def get_unique_values(Original_list):
  unique_values = set()
  for item in Original_list:
    if isinstance(item, str):
      unique_values.add(item)
    elif isinstance(item, list):
      unique_values.update(get_unique_values(item))
  return list(unique_values)

unique_authors = get_unique_values(dict_auth)
unique_cats = get_unique_values(categories)

## We migrate the results to our database
author = Author()
author.Uni_author = unique_authors
author.save()

category = Category()
category.category = unique_cats
category.save()