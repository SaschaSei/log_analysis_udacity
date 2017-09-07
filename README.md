# Log Analysis for Udacity Full Stack Web Dev
from Sascha Seiberl

This program is written for the Udacity Full Stack Web Dev Nanodegree. It uses
a database provided by Udacity and outputs three pieces of data. The database is a
collection of articles, authors and server logs.

## Output
My program will ouput:
- a list of the three most viewd articles
- a list of the most viewd authors and
- the dates when 1% or more of the server requests resulted in errors

## Prerequisits
- the program is written in Python 3.6.2 downloadable [here](https://www.python.org/downloads/)
- you will also need to install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- and [Vagrant](https://www.vagrantup.com/downloads.html)
- download the [database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- download the [repository](https://github.com/SaschaSei/log_analysis_udacity.git)

## How to run the program

### Setup
- install VirtualBox
- install Vagrant
- unzip the database file "newsdata.zip" into the vagrant directory
- put the repository files into the same directory

### Run
- start and log into vagrant from the command line
```sh
$ vagrant up
$ vagrant ssh
```
- navigate to the folder with the repo and the database and launch the file:
log_analysis.py

### Views
On the first run the program will create two views in the database.
One that shows the daily server request errors and on that shows the daily requests.
- daily_error_count:
```sh
create view daily_error_count as select cast(time as date), status, count(*)
from log where log.status like concat(4, '%')
group by cast(time as date), status order by cast(time as date) desc;
```

- daily_request_count:
```sh
create view daily_request_count as select cast(time as date),
count(*) from log group by cast(time as date)
order by cast(time as date) desc;
```
