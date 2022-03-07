# Mark Feehily
# Professor Santore
# COMP 490
# 3/6/2022

# Sprint 3 - used for Sprint 4 and Run

import sqlite3
from sqlite3 import IntegrityError
from typing import Tuple

import requests
import pprint
import secrets
import sys


def get_data(url):
    response = requests.get(url + secrets)
    data_list = response.json()
    data = data_list['items']
    return data


def user_ratings(self):
    shows = get_data(f"https://imdb-api.com/en/API/Top250TVs/{secrets}")
    url = f"https://imdb-api.com/en/API/UserRatings/{secrets}"
    for i in range(0, 200):
        if shows[i]['rank'] == '1' or shows[i]['rank'] == '50' \
                or shows[i]['rank'] == '100' or shows[i]['rank'] == '200':
            r = requests.get(url + "/" + shows[i]['id'])
            info = r.json()
            print("User rating data for the number " + shows[i]['rank'] + " ranked show:")
            pprint.pprint(info)
            print('\n')


def wheelofTime_ratings():
    user_url = f"https://imdb-api.com/en/API/UserRatings/{secrets}"
    wheelofTime_id = 'tt0331080'
    w = requests.get(user_url + "/" + wheelofTime_id)
    wheel_info = w.json()
    print("rating data for Wheel of Time:")
    pprint.pprint(wheel_info)


def listOutShows(self):
    shows = get_data(f"https://imdb-api.com/en/API/Top250TVs/{secrets}")
    print('\n')
    print("Top 250 shows:")
    print('\n')
    for i in range(0, len(shows)):
        print(shows[i])
        print('\n')


def save(data, filename='data.txt'):
    sys.stdout = open(filename, "w")
    user_ratings(data)
    wheelofTime_ratings()
    listOutShows(data)

    sys.stdout.close()


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    return connection, cursor


def shows_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS shows (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        fullTitle TEXT NOT NULL,
        year INTEGER DEFAULT 0,
        crew TEXT NOT NULL,
        imDbRating REAL DEFAULT 0,
        imDbRatingCount INTEGER DEFAULT 0
        );''')


def showRatings(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS show_ratings (
            imDbID TEXT NOT NULL UNIQUE,
            totalRating INTEGER DEFAULT 0,
            totalRatingVotes INTEGER DEFAULT 0,
            ten_rating_percentage REAL DEFAULT 0,
            ten_rating_votes INTEGER DEFAULT 0,
            nine_rating_percentage REAL DEFAULT 0,
            nine_rating_votes INTEGER DEFAULT 0,
            eight_rating_percentage REAL DEFAULT 0,
            eight_rating_votes INTEGER DEFAULT 0,
            seven_rating_percentage REAL DEFAULT 0,
            seven_rating_votes INTEGER DEFAULT 0,
            six_rating_percentage REAL DEFAULT 0,
            six_rating_votes INTEGER DEFAULT 0,
            five_rating_percentage REAL DEFAULT 0,
            five_rating_votes INTEGER DEFAULT 0,
            four_rating_percentage REAL DEFAULT 0,
            four_rating_votes INTEGER DEFAULT 0,
            three_rating_percentage REAL DEFAULT 0,
            three_rating_votes INTEGER DEFAULT 0,
            two_rating_percentage REAL DEFAULT 0,
            two_rating_votes INTEGER DEFAULT 0,
            one_rating_percentage REAL DEFAULT 0,
            one_rating_votes INTEGER DEFAULT 0,
            FOREIGN KEY (imDbId) REFERENCES shows (id)
            ON DELETE CASCADE
            );''')


def addToShows(cursor: sqlite3.Cursor, data):
    for i in range(0, len(data)):
        try:
            cursor.execute('''INSERT INTO shows (id, title,
                           fullTitle, year, crew, imDbRating, imDbRatingCount)
                           VALUES(?, ?, ?, ?, ?, ?, ?)''',
                           (data[i]['id'], data[i]['title'], data[i]['fullTitle'], data[i]['year'],
                            data[i]['crew'], data[i]['imDbRating'], data[i]['imDbRatingCount']))
            cursor.execute('SELECT rowid, * FROM shows')
            cursor.fetchall()
        except IntegrityError:
            cursor.execute('''DROP TABLE shows''')
            shows_table(cursor)
            addToShows(cursor, data)


def wheelofTime_table(cursor: sqlite3.Cursor):
    cursor.execute('''INSERT OR IGNORE INTO shows (id, title,
                           fullTitle, year, crew, imDbRating, imDbRatingCount)
                           VALUES(?, ?, ?, ?, ?, ?, ?)''',
                   ('tt0331080', 'Wheel of Time', 'Wheel of Time (2003)', '2003',
                    'The Dalai Lama, Lama Lhundup Woeser, Takna Jigme Sangpo',
                    0, 0))
    cursor.execute('SELECT rowid, * FROM shows')
    cursor.fetchone()


def addToShowRatings(cursor: sqlite3.Cursor, data):
    user_url = f"https://imdb-api.com/en/API/UserRatings/{secrets}"
    for i in range(len(data)):
        try:
            if data[i]['rank'] == '1' or data[i]['rank'] == '50' \
                    or data[i]['rank'] == '100' or data[i]['rank'] == '200':
                r = requests.get(user_url + "/" + data[i]['id'])
                info = r.json()
                if len(info['ratings']) == 0:
                    cursor.execute('''INSERT INTO show_ratings (imDbId, totalRating, totalRatingVotes,
                                ten_rating_percentage, ten_rating_votes, nine_rating_percentage, nine_rating_votes,
                                eight_rating_percentage, eight_rating_votes, seven_rating_percentage, seven_rating_votes,
                                six_rating_percentage, six_rating_votes, five_rating_percentage, five_rating_votes,
                                four_rating_percentage, four_rating_votes, three_rating_percentage, three_rating_votes,
                                two_rating_percentage, two_rating_votes, one_rating_percentage, one_rating_votes)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (
                                       info['imDbId'], info['totalRating'], info['totalRatingVotes'],
                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                else:
                    cursor.execute('''INSERT INTO show_ratings (imDbId, totalRating, totalRatingVotes,
                    ten_rating_percentage, ten_rating_votes, nine_rating_percentage, nine_rating_votes,
                    eight_rating_percentage, eight_rating_votes, seven_rating_percentage, seven_rating_votes,
                    six_rating_percentage, six_rating_votes, five_rating_percentage, five_rating_votes, four_rating_percentage,
                    four_rating_votes, three_rating_percentage, three_rating_votes, two_rating_percentage, two_rating_votes,
                    one_rating_percentage, one_rating_votes)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                   (
                                       info['imDbId'], info['totalRating'], info['totalRatingVotes'],
                                       info['ratings'][0]['percent'], info['ratings'][0]['votes'],
                                       info['ratings'][1]['percent'], info['ratings'][1]['votes'],
                                       info['ratings'][2]['percent'], info['ratings'][2]['votes'],
                                       info['ratings'][3]['percent'], info['ratings'][3]['votes'],
                                       info['ratings'][4]['percent'], info['ratings'][4]['votes'],
                                       info['ratings'][5]['percent'], info['ratings'][5]['votes'],
                                       info['ratings'][6]['percent'], info['ratings'][6]['votes'],
                                       info['ratings'][7]['percent'], info['ratings'][7]['votes'],
                                       info['ratings'][8]['percent'], info['ratings'][8]['votes'],
                                       info['ratings'][9]['percent'], info['ratings'][9]['votes']))

                cursor.execute('SELECT * FROM shows where title is "Wheel of Time"')
                cursor.fetchone()

                wheel_of_time_id = 'tt0331080'
                w = requests.get(user_url + "/" + wheel_of_time_id)
                wheel_info = w.json()
                cursor.execute('''INSERT OR IGNORE INTO show_ratings (imDbId, totalRating, totalRatingVotes,
                            ten_rating_percentage, ten_rating_votes, nine_rating_percentage, nine_rating_votes,
                            eight_rating_percentage, eight_rating_votes, seven_rating_percentage, seven_rating_votes,
                            six_rating_percentage, six_rating_votes,
                            five_rating_percentage, five_rating_votes, four_rating_percentage,
                            four_rating_votes, three_rating_percentage, three_rating_votes, two_rating_percentage, two_rating_votes,
                            one_rating_percentage, one_rating_votes)
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (wheel_of_time_id, wheel_info['totalRating'],
                                wheel_info['totalRatingVotes'], wheel_info['ratings'][0]['percent'],
                                wheel_info['ratings'][0]['votes'], wheel_info['ratings'][1]['percent'],
                                wheel_info['ratings'][1]['votes'], wheel_info['ratings'][2]['percent'],
                                wheel_info['ratings'][2]['votes'], wheel_info['ratings'][3]['percent'],
                                wheel_info['ratings'][3]['votes'], wheel_info['ratings'][4]['percent'],
                                wheel_info['ratings'][4]['votes'], wheel_info['ratings'][5]['percent'],
                                wheel_info['ratings'][5]['votes'], wheel_info['ratings'][6]['percent'],
                                wheel_info['ratings'][6]['votes'], wheel_info['ratings'][7]['percent'],
                                wheel_info['ratings'][7]['votes'], wheel_info['ratings'][8]['percent'],
                                wheel_info['ratings'][8]['votes'], wheel_info['ratings'][9]['percent'],
                                wheel_info['ratings'][9]['votes']))

                cursor.execute('SELECT rowid, * FROM show_ratings')
                cursor.fetchall()
        except IntegrityError:
            cursor.execute('''DROP TABLE show_ratings''')
            showRatings(cursor)
            addToShowRatings(cursor, data)


def closeDataBase(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


def popularTv(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS popular_tv (
            id TEXT PRIMARY KEY,
            rank INTEGER DEFAULT 0,
            rankUpDown INTEGER DEFAULT 0,
            title TEXT NOT NULL,
            fullTitle TEXT NOT NULL,
            year INTEGER DEFAULT 0,
            crew TEXT NOT NULL,
            imDbRating REAL DEFAULT 0,
            imDbRatingCount INTEGER DEFAULT 0
            );''')


def moviesTable(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            fullTitle TEXT NOT NULL,
            year INTEGER DEFAULT 0,
            crew TEXT NOT NULL,
            imDbRating REAL DEFAULT 0,
            imDbRatingCount INTEGER DEFAULT 0
            );''')


def popularMovies(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS popular_movies (
            id TEXT PRIMARY KEY,
            rank INTEGER DEFAULT 0,
            rankUpDown INTEGER DEFAULT 0,
            title TEXT NOT NULL,
            fullTitle TEXT NOT NULL,
            year INTEGER DEFAULT 0,
            crew TEXT NOT NULL,
            imDbRating REAL DEFAULT 0,
            imDbRatingCount INTEGER DEFAULT 0
            );''')


def movieRatings(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS movie_ratings (
                imDbID TEXT NOT NULL UNIQUE,
                title TEXT,
                fullTitle TEXT,
                type TEXT,
                year INTEGER DEFAULT 0,
                imDb REAL DEFAULT 0,
                metacritic REAL DEFAULT 0,
                theMovieDb REAL DEFAULT 0,
                rottenTomatoes REAL DEFAULT 0,
                tV_com REAL DEFAULT 0,
                filmAffinity INTEGER DEFAULT 0,
                FOREIGN KEY (imDbId) REFERENCES movies (id)
                ON DELETE CASCADE
                );''')


def addToPopularTv(cursor: sqlite3.Cursor, data):
    for i in range(0, len(data)):
        try:
            cursor.execute('''INSERT INTO popular_tv (id, rank, rankUpDown, title,
                           fullTitle, year, crew, imDbRating, imDbRatingCount)
                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (data[i]['id'], data[i]['rank'], data[i]['rankUpDown'], data[i]['title'],
                            data[i]['fullTitle'], data[i]['year'], data[i]['crew'], data[i]['imDbRating'],
                            data[i]['imDbRatingCount']))

            cursor.execute('SELECT rowid, * FROM popular_tv')
            cursor.fetchall()
        except IntegrityError:
            cursor.execute('''DROP TABLE popular_tv''')
            popularTv(cursor)
            addToPopularTv(cursor, data)


def addToPopularMovies(cursor: sqlite3.Cursor, data):
    for i in range(0, len(data)):
        try:
            cursor.execute('''INSERT INTO popular_movies (id, rank, rankUpDown, title,
                           fullTitle, year, crew, imDbRating, imDbRatingCount)
                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (data[i]['id'], data[i]['rank'], data[i]['rankUpDown'], data[i]['title'],
                            data[i]['fullTitle'], data[i]['year'], data[i]['crew'], data[i]['imDbRating'],
                            data[i]['imDbRatingCount']))

            cursor.execute('SELECT rowid, * FROM popular_movies')
            cursor.fetchall()
        except IntegrityError:
            cursor.execute('''DROP TABLE popular_movies''')
            popularMovies(cursor)
            addToPopularMovies(cursor, data)


def addToMovies(cursor: sqlite3.Cursor, data):
    for i in range(0, len(data)):
        try:
            cursor.execute('''INSERT INTO movies (id, title,
                           fullTitle, year, crew, imDbRating, imDbRatingCount)
                           VALUES(?, ?, ?, ?, ?, ?, ?)''',
                           (data[i]['id'], data[i]['title'], data[i]['fullTitle'], data[i]['year'],
                            data[i]['crew'], data[i]['imDbRating'], data[i]['imDbRatingCount']))

            cursor.execute('SELECT rowid, * FROM movies')
            cursor.fetchall()
        except IntegrityError:
            cursor.execute('''DROP TABLE movies''')
            moviesTable(cursor)
            addToMovies(cursor, data)


def getRankChange(data):
    rank_changes = []
    for i in range(0, len(data)):
        if data[i]['rankUpDown'].startswith('+'):
            data[i]['rankUpDown'] = data[i]['rankUpDown'][1:]
        if "," in data[i]['rankUpDown'][0:4]:
            data[i]['rankUpDown'] = data[i]['rankUpDown'].replace(",", "")
        float(data[i]['rankUpDown'])
        rank_changes.append(data[i]['rankUpDown'])

    biggest_changes = []
    changes = sorted(rank_changes, key=int)
    biggest_changes.append(changes[len(changes) - 1])
    biggest_changes.append(changes[len(changes) - 2])
    biggest_changes.append(changes[len(changes) - 3])
    biggest_changes.append(changes[0])
    return biggest_changes


def addToMovieRatings(cursor: sqlite3.Cursor, data):
    ratings_url = f"https://imdb-api.com/en/API/Ratings/{secrets}"
    rank_changes = getRankChange(data)
    for i in range(0, len(data)):
        try:
            if data[i]['rankUpDown'] == rank_changes[3] or data[i]['rankUpDown'] == rank_changes[2] or \
                    data[i]['rankUpDown'] == rank_changes[1] or data[i]['rankUpDown'] == rank_changes[0]:
                r = requests.get(ratings_url + "/" + data[i]['id'])
                info = r.json()
                cursor.execute('''INSERT INTO movie_ratings (imDbId, title, fullTitle, type, year, imDb, metacritic,
                                        theMovieDb, rottenTomatoes, tV_com, filmAffinity)
                                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (
                                   info['imDbId'], info['title'], info['fullTitle'], info['type'],
                                   info['year'], info['imDb'], info['metacritic'], info['theMovieDb'],
                                   info['rottenTomatoes'], info['tV_com'], info['filmAffinity']))

            cursor.execute('SELECT * FROM movie_ratings')
            cursor.fetchall()
        except IntegrityError:
            cursor.execute('''DROP TABLE movie_ratings''')
            movieRatings(cursor)
            addToMovieRatings(cursor, data)
