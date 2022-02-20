# Mark Feehily
# Professor Santore
# COMP 490
# 2/20/2022

# Sprint 3


import secrets
import requests
import sqlite3
import pandas as pd
import csv
from typing import Tuple

url1 = f"https://imdb-api.com/en/API/MostPopularTVs/{secrets}"  # Uses API to get data needed for most popular TV shows
response = requests.get(url1)
data1 = response.json()
list1 = data1['items']

url2 = f"https://imdb-api.com/en/API/Top250TVs/{secrets}"  # Uses API to get data needed for top 250 TV shows
response = requests.get(url2)
data2 = response.json()
list2 = data2['items']
key = list2[0].keys()

url3 = f"https://imdb-api.com/en/API/MostPopularMovies/{secrets}]"
response = requests.get(url3)  # Uses API to get data needed for most popular movies
data3 = response.json()
list3 = data3['items']
key2 = list3[0].keys()


def setup(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS pop_shows(
        id TEXT PRIMARY KEY,
        rank TEXT,
        rankUpDown FLOAT,
        title TEXT,
        fullTitle INTEGER,
        year FLOAT DEFAULT 0,
        director TEXT,
        imDbRating TEXT,
        imDbRatingCount FLOAT DEFAULT 0);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS movie_headlines(
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            full_title TEXT NOT NULL,
            director TEXT,
            year INTEGER NOT NULL,
            rating FLOAT DEFAULT 0,
            rating_count FLOAT DEFAULT 0);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS movie_upDownTrend(
            id TEXT PRIMARY KEY,
            title TEXT
            full_title TEXT
            imDbRating
            imDbRatingCount FLOAT DEFAULT 0,
            rankUpDown FLOAT DEFAULT 0);''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS pop_movies(
            id TEXT PRIMARY KEY,
            rank TEXT,
            rankUpDown FLOAT,
            title TEXT,
            fullTitle INTEGER,
            year FLOAT DEFAULT 0,
            director TEXT,
            imDbRating TEXT,
            imDbRatingCount FLOAT DEFAULT 0);''')


with open("output_2.csv", 'w') as f:
    writer = csv.DictWriter(f, key)  # Writes to file output_2 using dictionary writer
    writer.writeheader()
    writer.writerows(list2)
    f.close()

with open("output_3.csv", 'w') as f:
    writer = csv.DictWriter(f, key2)  # Writes to file output_3 using dictionary writer
    writer.writeheader()
    writer.writerows(list3)
    f.close()


def pop_csv():
    with open("output.csv", 'w') as f:
        keys = list[0].keys()
        writer1 = csv.DictWriter(f, keys)  # writes the data to a file using dictionary writer
        writer1.writeheader()
        writer1.writerows(list)
        f.close()


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:  # Opens a new database
    database_connection = sqlite3.connect(filename)
    cursor = database_connection.cursor()
    return database_connection, cursor


def close_db(connection: sqlite3.Connection):  # Closes the database
    connection.commit()
    connection.close()


def get_data():
    mostPopular = pd.read_csv('output.csv', encoding="latin-1")
    return mostPopular


def get_movies():
    movie_top250 = pd.read_csv('output2.csv', encoding="latin-1")
    return movie_top250


def get_data03():
    popular_Movies = pd.read_csv('output3.csv', encoding="latin-1")
    return popular_Movies


def movie_Top250(cursor: sqlite3.Cursor, conn: sqlite3.Connection):  # adds data to top 250 movies in database file
    movie250 = get_movies()
    keys = movie250['id'].tolist()
    data_dicts = {}
    for item in keys:
        data_dicts[item] = (movie250.loc[movie250['id'] == item]['title'].tolist()[0],
                            movie250.loc[movie250['id'] == item]['fullTitle'].tolist()[0],
                            movie250.loc[movie250['id'] == item]['director'].tolist()[0],
                            movie250.loc[movie250['id'] == item]['year'].tolist()[0],
                            movie250.loc[movie250['id'] == item]['imDbRating'].tolist()[0],
                            movie250.loc[movie250['id'] == item]['imDbRatingCount'].tolist()[0])

    for key in data_dicts.keys():
        cursor.execute("""INSERT INTO movie_headlines (id, title, full_title, director, year, rating, rating_count)
                                  VALUES (?,?,?,?,?,?,?)""", (key, data_dicts[key][0], data_dicts[key][1],
                                                              data_dicts[key][2], data_dicts[key][3],
                                                              data_dicts[key][4],
                                                              data_dicts[key][5]))
        conn.commit()


def popular_movies(cursor: sqlite3.Cursor, conn: sqlite3.Connection):  # add Popular movies data into database
    pop_movies = get_data03()
    kii = pop_movies['id'].tolist()
    data_dict02 = {}
    for item in kii:
        data_dict02[item] = (pop_movies.loc[pop_movies['id'] == item]['rank'].tolist()[0],
                             pop_movies.loc[pop_movies['id'] == item]['rankUpDown'].tolist()[0],
                             pop_movies.loc[pop_movies['id'] == item]['title'].tolist()[0],
                             pop_movies.loc[pop_movies['id'] == item]['fullTitle'].tolist()[0],
                             pop_movies.loc[pop_movies['id'] == item]['year'].tolist()[0],
                             pop_movies.loc[pop_movies['id'] == item]['Director'].tolist()[0],
                             pop_movies.loc[pop_movies['id'] == item]['imDbRating'].tolist()[0],
                             pop_movies.loc[pop_movies['id'] == item]['imDbRatingCount'].tolist()[0])

    for key in data_dict02.keys():
        cursor.execute("""INSERT INTO pop_movies (id, rank, rankUpDown, title, fulLTitle, director, year, imDbRating,
        imDbRatingCount) VALUES (?,?,?,?,?,?,?,?,?)""", (key, data_dict02[key][0], data_dict02[key][1],
                                                         data_dict02[key][2], data_dict02[key][3],
                                                         data_dict02[key][4], data_dict02[key][5],
                                                         data_dict02[key][6], data_dict02[key][7]))
        conn.commit()


def popular_shows(cursor: sqlite3.Cursor, conn: sqlite3.Connection):  # add popular shows data into database
    head_d = get_data()
    key = head_d['id'].tolist()
    data_dict = {}
    for item in key:
        data_dict[item] = (head_d.loc[head_d['id'] == item]['rank'].tolist()[0],
                           head_d.loc[head_d['id'] == item]['rankUpDown'].tolist()[0],
                           head_d.loc[head_d['id'] == item]['title'].tolist()[0],
                           head_d.loc[head_d['id'] == item]['fullTitle'].tolist()[0],
                           head_d.loc[head_d['id'] == item]['year'].tolist()[0],
                           head_d.loc[head_d['id'] == item]['director'].tolist()[0],
                           head_d.loc[head_d['id'] == item]['imDbRating'].tolist()[0],
                           head_d.loc[head_d['id'] == item]['imDbRatingCount'].tolist()[0])

    for key in data_dict.keys():
        cursor.execute("""INSERT INTO pop_shows (id, rank, rankUpDown, title, fulLTitle, director, year, imDbRating,
        imDbRatingCount) VALUES (?,?,?,?,?,?,?,?,?)""", (key, data_dict[key][0], data_dict[key][1],
                                                         data_dict[key][2], data_dict[key][3],
                                                         data_dict[key][4], data_dict[key][5],
                                                         data_dict[key][6], data_dict[key][7]))
        conn.commit()


def rankUpDown(cursor: sqlite3.Cursor, conn: sqlite3.Connection):
    cursor.execute("""INSERT INTO movie_upDownTrend
                   SELECT id, title, rankUpDown
                   FROM popular_movies
                   ORDER BY rankUpDown DESC
                   LIMIT 3""")

    cursor.execute("""INSERT INTO movie_upDownTrend
                       SELECT id, title, rankUpDown
                       FROM popular_movies
                       ORDER BY rankUpDown ASC
                       LIMIT 1""")
    conn.commit()
# creates database section that show the rank up or down


def main():
    pop_csv()
    name = 'movie_api.db'
    conn, cursor = open_db(name)
    setup(cursor)
    movie_Top250(cursor, conn)
    popular_movies(cursor, conn)
    popular_shows(cursor, conn)
    rankUpDown(cursor, conn)
    conn.commit()
    close_db(conn)


if __name__ == '__main__':
    main()



