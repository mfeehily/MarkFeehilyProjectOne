# Mark Feehily
# Professor Santore
# COMP 490
# 2/10/2022

# Sprint 2

import secrets
import sqlite3
import sys
from typing import Tuple
import requests
import pandas as pd
import csv


def setup(cursor: sqlite3.Cursor):  # database setup
    cursor.execute('''CREATE TABLE IF NOT EXISTS headline_data( 
        Id TEXT PRIMARY KEY, 
        Title TEXT NOT NULL,
        Director TEXT,
        Year INTEGER NOT NULL,
        Rating FLOAT DEFAULT 0,
        Rating_number FLOAT DEFAULT 0);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings_data(
            id TEXT NOT NULL,
            total_rating FLOAT NOT NULL,
            rating_votes INTEGER NOT NULL,
            TenRating FLOAT NOT NULL,
            TenRateVotes INTEGER NOT NULL,
            NineRating FLOAT NOT NULL,
            NineRateVotes INTEGER NOT NULL,
            EightRating FLOAT NOT NULL,
            EightRateVotes INTEGER NOT NULL,
            SevenRate FLOAT NOT NULL,
            SevenRateVotes INTEGER NOT NULL,
            SixRating FLOAT NOT NULL,
            SixRateVotes INTEGER NOT NULL,
            FiveRating FLOAT NOT NULL,
            FiveRateVotes INTEGER NOT NULL,
            FourRate FLOAT NOT NULL,
            FourRateVotes INTEGER NOT NULL,
            ThreeRate FLOAT NOT NULL,
            ThreeRateVotes INTEGER NOT NULL,
            TwoRate FLOAT NOT NULL,
            TwoRateVotes INTEGER NOT NULL,
            OneRate FLOAT NOT NULL,
            OneRateVotes INTEGER NOT NULL,
            FOREIGN KEY (id) REFERENCES headline_data (id)
            ON DELETE CASCADE ON UPDATE NO ACTION);''')

    url = f"https://imdb-api.com/en/API/Top250TVs/{secrets}"  # assign API with data to url
    results = requests.get(url)
    if results.status_code != 200:  # if there is not enough data a failed to get data message will appear
        print(f"Failed to get data {results.status_code}error{results.reason} ")
        sys.exit(-1)

    response = results.json()
    show_list = response["items"]
    List_data = show_list[0].keys()

    with open("output.csv", 'w') as f:  # open output file
        writer = csv.DictWriter(f, List_data)
        writer.writeheader()
        writer.writerows(show_list)
        f.close()


def open_Data_Base(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:  # open database
    Data_Base_Connect = sqlite3.connect(filename)
    cursor = Data_Base_Connect.cursor()
    return Data_Base_Connect, cursor


def data():  # database data
    top_250 = pd.read_csv('Data.csv', encoding="latin-1")
    return top_250


def rate():  # database rate
    r_data = pd.read_cvs('Data2.csv', encoding="latin-1")
    return r_data


def headlined_data(cursor: sqlite3.Cursor, connect: sqlite3.Connection):
    top_250 = data()
    keys = top_250['id'].tolist()
    Dictionary_data = {}
    for item in keys:
        Dictionary_data[item] = (top_250.loc[top_250['id'] == item]['title'].tolist()[0],
                                 top_250.loc[top_250['id'] == item]['fullTitle'].tolist()[0],
                                 top_250.loc[top_250['id'] == item]['director'].tolist()[0],
                                 top_250.loc[top_250['id'] == item]['year'].tolist()[0],
                                 top_250.loc[top_250['id'] == item]['imDbRating'].tolist()[0],
                                 top_250.loc[top_250['id'] == item]['imDbRatingCount'].tolist()[0])

    for key in Dictionary_data.keys():
        cursor.execute("""INSERT INTO headline_data (id, title, full_title, Director, year, rating, rating_count)
                                  VALUES (?,?,?,?,?,?,?)""", (key, Dictionary_data[key][0],
                                                              Dictionary_data[key][1],
                                                              Dictionary_data[key][2],
                                                              Dictionary_data[key][3],
                                                              Dictionary_data[key][4],
                                                              Dictionary_data[key][5]))
        connect.commit()  # commit the values from dictionary data


def close_Data_Base(connection: sqlite3.Connection):  # close database
    connection.commit()
    connection.close()


def main():
    name = 'movies.db'  # sets name of database file
    connect, cursor = open_Data_Base(name)  # adds data to database file
    setup(cursor)
    headlined_data(cursor, connect)
    connect.commit()
    close_Data_Base(connect)


if __name__ == '__main__':
    main()
