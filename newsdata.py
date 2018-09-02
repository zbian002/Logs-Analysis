import psycopg2, bleach

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
error_request = """select time """
