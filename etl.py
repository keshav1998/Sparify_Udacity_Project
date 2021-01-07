import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
       Read the json files for song data and Insert appropirate values
       in the songs and artist tables.
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    try:
        song_data = list(df[['song_id','title', 'artist_id', 'year', 'duration']].values[0])
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e: 
        print("Error: Inserting Rows")
        print (e)
    
    
    # insert artist record
    try:
        artist_data = list(df[['artist_id','artist_name', 'artist_location','artist_latitude', 'artist_longitude']].values[0])
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e: 
        print("Error: Inserting Rows")
        print (e)


def process_log_file(cur, filepath):
    """
       Read Json files containing user data, process required data and
       insert data into time_data,user information and song_plays tables.
       Executes query to access songs database.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df = df[df['page']=='NextSong'].reset_index(drop=True)

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts)
    
    # insert time data records
    time_data = (t.values,t.dt.hour.values, t.dt.day.values, t.dt.week.values, t.dt.month.values, t.dt.year.values, t.dt.weekday.values)
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    
    # creating time dictionary
    df_dict = {}
    for valset, label in zip(time_data, column_labels):
        df_dict[label] = valset
        
    
    time_df = pd.DataFrame(df_dict)

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e: 
            print("Error: Inserting Rows")
            print (e)

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as e: 
            print("Error: Inserting Rows")
            print (e)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts), row.userId,row.level, songid, artistid, row.sessionId, row.location,  row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
       Get the list of files from the required directory, iterate over
       files and pass them to their respective data proccessing 
       function.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
       Connect with postgres server and create a cursor to execute 
       queries from 'sql_queries.py'. It further call the process_data
       function with respect to the data(song or log).
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()