# Log Analysis for Udacity Full Stack Web Dev

This program is written for the Udacity Full Stack Web Dev Nanodegree. It uses
a database provided by Udacity and outputs three pieces of data.

## Prerequisits
- the program is written in Python 3.6.2 downloadable [here](https://www.python.org/downloads/)
- you will also need to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- and [Vagrant](https://www.vagrantup.com/downloads.html)

## How to run the program

- install VirtualBox
- install Vagrant
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

create view article_count as select articles.title, count(*) from articles inner join log on log.path like concat('%', articles.slug, '%') where log.status = '200 OK' group b
y articles.title order by count desc;


select authors.name, count(*) from authors inner join articles on authors.id = articles.author inner joi
n log on log.path like concat('%', articles.slug, '%') where log.status = '200 OK' group by authors.name order
by count(*) desc;


daily_error_count:  create view daily_error_count as select cast(time as date), status, count(*) from log where log.status like conca
t(4, '%') group by cast(time as date), status order by cast(time as date) desc;


daily_request_count: create view daily_request_count as select cast(time as date), count(*) from log group by cast(time as date) order
 by cast(time as date) desc;

 select daily_error_count.time,  round(daily_error_count.count * 100 / daily_request_count.count) from daily_error
_count inner join daily_request_count on daily_error_count.time = daily_request_count.time where  round(daily_error_coun
t.count * 100 / daily_request_count.count) >=1 order by daily_error_count.time;
