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
import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myproject.settings")
django.setup()
# Importing my app's Django models
from News_Articles.models import News_Article, Author, Category

## We setup the query parameters according to our intent.

lan = 'english'
loc = 'Colombia'
Qry = 'PV power'
Max = 15

## We use the function NewsClient and store the results of our query in the object Client
Client = scraparazzie.NewsClient(language = lan, location = loc, query = Qry, max_results= Max)

## We get the information from our query in a set of lists using the function export_news() in our Client object. 
## We get one list per result, each list contains: 1) title of the news article, 2) source of the news article, 3) link of the news article, 4) publish date
## We will store the url of each news article in a dictionary
items = Client.export_news()
dict_urls = []
a = 0
for item in items:
    dict_urls.append({'link':item['link'], 'title': item['title'], 'published_date': item['publish_date']})
    a = a+1

## After getting our list of news articles URLs we can make use of newspaper3k library to extract complementary information of each URL (when availabe) such as authors, publish date, title, summary, text content, html content, etc.
## To do so, we first create an article object by using the class Article and then proceed to use the functions download, parse and nlp to be able to extract out the complementary properties of each news article.
## We then create a pandas DataFrame and store the desired data in individual columns for each article. Each df is then stored in a dictionary.
## Bear in mind that sometimes we can get errors using newspaper3k library such as exceeding the limit of queries in an specific news portal, or being unable to get information from an specific URL.
## To troubleshoot this, I have included a try-except rule so the extraction process does not finish abruptly.

## After getting our list of news articles URLs we can make use of newspaper3k library to extract complementary information of each URL (when availabe) such as authors, publish date, title, summary, text content, html content, etc.
## To do so, we first create an article object by using the class Article and then proceed to use the functions download, parse and nlp to be able to extract out the complementary properties of each news article.
## We then create a dictionary and store the desired data in individual lists for each article.
## Bear in mind that sometimes we can get errors using newspaper3k library such as exceeding the limit of queries in an specific news portal, or being unable to get information from an specific URL.
## To troubleshoot this, I have included a try-except rule so the extraction process does not finish abruptly.
dict = []
dict_auth = []
for url in range(len(dict_urls)):
    try:
        art = Article(dict_urls[url]['link'])
        art.download()
        art.parse()
        ## We will make use of this natural language processing function (nlp) to get information such as summary and keywords, which we will use to assign a category to the news article
        art.nlp()
        ## Here we clean and complete data that could be lost from the scrapping method
        ## If we get no published_date for the news article, we set a default date of '1999-01-01' so the parameter meets with the django model
        if (dict_urls[url]['published_date']==None):
            pub = 'no'
            pub_date = datetime('1999/01/01')
        else:
            pub= 'yes'
            # Parse the date string using strptime and format the date as YYYY-MM-DD
            parsed_date = datetime.strptime(dict_urls[url]['published_date'], "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            pub_date = formatted_date
        ## If we get no author after scrapping the website, we set a Jhon Doe author to meet with the requirement
        if (art.authors==[]):
            auth = 'John Doe, the writer of this article was not identified'
        else:
            auth = ''
            for i in art.authors:
                auth = auth + ' ' + i
        dict.append({'author':auth, 'title': dict_urls[url]['title'], 'summary': art.summary, 'text': art.text, 'html': art.html, 'category': art.keywords[0], 'published': pub, 'published date': pub_date})
        ## We will try to capture the information of the news article main author by storing the first 2 elements of the authors list
        if (len(art.authors)<2):
            name = 'John Doe'
        else:
            name = art.authors[0] + ' ' + art.authors[1]
        dict_auth.append(name)
    except :
        pass

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
