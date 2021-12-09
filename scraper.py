import requests # pulling data
from bs4 import BeautifulSoup # xml parsing
import json # exporting to files
import codecs
import sqlite3 #importing sqlite3 library for interfacing with a simple one-file database
import datetime #importing datetime functions

#convertor function
def convertor_function(article):
    article_string = str(article)
    return article_string

#database_save function
def database_save(articles):
    today_date = datetime.date.today().strftime("%d/%m/%Y %H:%M:%S")
    database_connection = sqlite3.connect('articles.db3')
    database_cursor = database_connection.cursor()
    database_cursor.execute("INSERT INTO articles (datetime, article_number, article_text) VALUES ('" + today_date + "', '" + str(articles.title) + "' '" + str(articles.text) + "')")
    print("INSERT INTO articles (datetime, article_number, article_text) VALUES ('" + today_date + "', '" + str(articles.title) + "' '" + str(articles.text) + "')")
    return None

# save function
def save_function(article_list):
    with open('articles.txt', 'w', encoding="utf-8") as outfile:
        json.dump(article_list, outfile, ensure_ascii=False)

# scraping function
def bashim_rss():
    article_list = []

    try:
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get('https://bash.im/rss/')

        soup = BeautifulSoup(r.content, features='xml', from_encoding='utf-8')
              
        # select only the "items" (i.e. articles) I want from the data
        articles = soup.findAll('item')
        
        # for each "item" I want, I parse it into a list. Each article will consist from a title, a link to an article, date of publication and a text of article.
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text
            description = a.find('description').text
         
            # create an "article" object with the data
            # from each "item"
            article = {
                'title': title,
                'link': link,
                'published': published,
                'description': description
                }

            # append my "article_list" with each "article" object
            article_list.append(convertor_function(article))
            #article_list.append(article)
                    
        # after the loop, dump my saved objects into a .txt file
        #return save_function(article_list)
        for a in article_list:
           database_save(a)      

    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)

print('Starting scraping')
bashim_rss()
print('Finished scraping')

