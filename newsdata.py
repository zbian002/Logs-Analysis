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
error_requests = """select total.date,
                    round(errors.error_requests * 1.0 / total.requests * 100, 2) as percent
                    from (
                        select date(time), count(*) as error_requests
                        from log where status like '404%'
                        group by date(time)
                    ) as errors, (
		                  select date(time), count(*) as requests
                          from log group by date(log.time)
                    ) as total
                    where total.date = errors.date
                    and round(errors.error_requests * 1.0 / total.requests * 100, 2) > 1
                    order by percent desc;"""

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

# Print days did more than 1% of requests lead to errors
def print_errors_days():
    print('\n' + "Days did more than 1% of requests lead to errors:" + '\n')
    errors_days = get_news(error_requests)
    for date, percent in errors_days:
        print("{0:%B %d, %Y} -- {1:.2f} % errors".format(date, percent))

if __name__ == '__main__':
    print_most_popular_articles()
    print_most_popular_authors()
    print_errors_days()
