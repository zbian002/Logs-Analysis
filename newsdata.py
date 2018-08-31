import psycopg2, bleach

# Database queries
# Database query 1: The most popular three articles of all time:
most_popular_articles = """select articles.title, count(*) as num
                    from articles, log
                    where log.status = '200 OK'
                    and articles.slug = substring(log.path, 10)
                    order by num desc
                    limit 3;"""
