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

# First view needed in database and the query to create it.
view_one = ["daily_error_count",
                "create view daily_error_count as select cast(time as date), "
                "status, count(*) from log "
                "where log.status like concat(4, '%') "
                "group by cast(time as date), status "
                "order by cast(time as date) desc;"]

# Second view needed in database and query to create it
view_two = ["daily_request_count",
            "create view daily_request_count as select cast(time as date), "
            "count(*) from log group by cast(time as date) "
            "order by cast(time as date) desc;"]



# Establishes connection to DB throws error if failing.
def connect_to_DB(db_name = DB_NAME):
    try:
        db = psycopg2.connect(database=DB_NAME)
        cursor = db.cursor()
        return db, cursor
    except:
        print ("Unable to connect.")

# Gets query returns results from DB.
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


def create_view(view):
    if (not check_for_view(view[0])):
        db, cursor = connect_to_DB()
        cursor.execute(view[1])
        db.commit()
        db.close()
        print "{} view created".format(view[0])

def check_for_view(view_name):
    db, cursor = connect_to_DB()
    cursor.execute("select exists(select * from information_schema.tables "
                    "where table_name = '{}')".format(view_name))
    return cursor.fetchone()[0]
    db.close()


if __name__ == '__main__':

    create_view(view_one)
    create_view(view_two)


    # Get data to print out.
    top_three_articles = get_query_results(query_1)
    most_popular_authors = get_query_results(query_2)
    error_days = get_query_results(query_3)


    # Print data.
    print "\n Top Three Articles: \n"
    print_results(top_three_articles)

    print "\n Most Popular Authors: \n"
    print_results(most_popular_authors)

    print "\n Days With 1% Errors Or More: \n"
    print_error_result(error_days)
