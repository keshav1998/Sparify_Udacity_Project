# Data Modeling with Postgres
> Keshav Mishra

This ETL Pipeline was designed for a startup **Sparkify**, who wants to analyze the data comming from their songs and user activity on their new music streaming app.The analytics team is particularly interested in understanding what songs users are listening to. This project a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app. On the basis of this a database is created with defined facts and dimension tables.

### Files in Project

* `create_tables.py`: Script to create and drop database and tables.

* `sql_queries.py`: Contans postgreSql queries to create, drop and insert values in tables.

* `etl.py`: Script to transform the original data from json files to Postgres tables, that contains valuable information.

* `etl.ipynb`: Notebook with the step by step process of how are we accessing the data and how tables are being inputted.

* `test.ipynb`: Notebook to look into different tables created during the process.


#### Fact Table
* `songplays`: records in log data associated with song plays i.e. records with page NextSong
*songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

#### Dimension Tables
* `users`: users in the app
*user_id, first_name, last_name, gender, level*

* `songs`: songs in music database
*song_id, title, artist_id, year, duration*

* `artists`: artists in music database
*artist_id, name, location, lattitude, longitude*

* `time`: timestamps of records in songplays broken down into specific units
*start_time, hour, day, week, month, year, weekday*


### ETL Script
An ETL script automatically loops through the logs and songs directories, reads every file, transforms the data using Pandas, and insert them on the star-schema acording with the tables previously defined. It asumes that the main tables are already created and uses ´sql_queries.py´.

### How to run:
   - run command to install requirements.
        > pip install -r requirements.txt
        
   - run ``create_tables.py`` to create database and tables.
   - run ``etl.py`` to execute the pipeline to read data from data files and transfer to respective tables.