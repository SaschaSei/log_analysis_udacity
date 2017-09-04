import psycopg2

DB_NAME = "news"

# 1. What are the most popular three articles of all time?
query_1 = ("select articles.title, count(*)"
            "from articles inner join log "
            "on log.path like concat('%', articles.slug, '%') "
            "where log.status = '200 OK'"
            " group by articles.title order by count(*) desc limit 3;")

# 2. Who are the most popular article authors of all time?
query_2 = ("select authors.name, count(*) "
            "from authors inner join articles "
            "on authors.id = articles.author inner join log "
            "on log.path like concat('%', articles.slug, '%') "
            "where log.status = '200 OK' "
            "group by authors.name order by count(*) desc;")
# 3. On which days did more than 1% of requests lead to errors?
query_3 = ("select daily_error_count.time,  "
            "round(daily_error_count.count * 100 / daily_request_count.count) "
            "from daily_error_count inner join "
            "daily_request_count on daily_error_count.time = "
            "daily_request_count.time "
            "where round(daily_error_count.count * "
            "100 / daily_request_count.count) >=1 "
            "order by daily_error_count.time;")


def connect_to_DB(db_name = DB_NAME):
    try:
        db = psycopg2.connect(database=DB_NAME)
        cur = db.cursor()
        return db, cur
    except:
        print ("Unable to connect.")

def get_query_results(query):
    db, cursor = connect_to_DB()
    cursor.execute(query)
    return cursor.fetchall()
    db.close()

def print_results(query_results):
    index = 1
    for title, results in query_results:
        print index,'. ', str(title),'\t -','\t', str(results), 'Views'
        index += 1

def print_error_result(query_result):
    for date, perc in query_result:
        print date, ' had ', perc, '% Errors'

if __name__ == '__main__':
    top_three_articles = get_query_results(query_1)
    most_popular_authors = get_query_results(query_2)
    error_days = get_query_results(query_3)

    print "\n Top Three Articles: \n"
    print_results(top_three_articles)

    print "\n Most Popular Authors: \n"
    print_results(most_popular_authors)

    print "\n Days With 1% Errors Or More: \n"
    print_error_result(error_days)
