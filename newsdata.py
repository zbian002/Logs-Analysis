#!/usr/bin/env python3

import psycopg2

# Database queries
# Database query 1: What are the most popular three articles of all time?
most_popular_articles = """select articles.title, count(*) as num
                           from articles, log
                           where log.status = '200 OK'
                           and articles.slug = substring(log.path, 10)
                           group by articles.title
                           order by num desc
                           limit 3;"""

# Database query 2: Who are the most popular article authors of all time?
most_popular_authors = """select authors.name, count(*) as num
                          from authors, log, articles
                          where log.status = '200 OK'
                          and articles.slug = substring(log.path, 10)
                          and articles.author = authors.id
                          group by authors.name
                          order by num desc;"""

# Database query 3: On which days did more than 1% of requests lead to errors?
#error_request = """select time """

# Function
# Open the database and establish connection with it
def get_news(query):
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    news = c.fetchall()
    db.close()
    return news

# Print the most popular three articles of all time
def print_most_popular_articles():
    print('\n' + "The most popular three articles of all time:" + '\n')
    top_three_articiles = get_news(most_popular_articles)
    for title, count in top_three_articiles:
        print(" \"{}\" -- {} views".format(title, count))

# Print the most popular article authors of all time
def print_most_popular_authors():
    print('\n' + "The most popular article authors of all time:" + '\n')
    all_the_authors = get_news(most_popular_authors)
    for name, count in all_the_authors:
        print(" {} -- {} views".format(name, count))

if __name__ == '__main__':
    print_most_popular_articles()
    print_most_popular_authors()
