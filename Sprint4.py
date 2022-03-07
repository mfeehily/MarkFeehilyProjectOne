# Mark Feehily
# Professor Santore
# COMP 490
# 3/6/2022

# Sprint 4


import tkinter
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plot
import sqlite3
import Run
import Sprint3
import secrets


def home_page():
    root = tkinter.Tk()
    root.title("Update Data")
    root.geometry('150x150')
    update = tkinter.Button(root, text='Update Data', command=lambda: Run.previous_sprints())
    update.grid(row=1, column=1, padx=10, pady=20)
    visual = tkinter.Button(root, text='Run Data ', command=lambda: visualization())
    visual.grid(row=2, column=1, padx=10, pady=10)
    root.mainloop()


def visualization():
    root = tkinter.Tk()
    root.title("Show or Movie Data")
    root.geometry('400x400')
    show_button = tkinter.Button(root, text='Most Popular Shows', command=lambda: popularShows_gui())
    show_button.grid(row=1, column=1, padx=10, pady=20, )
    movie_button = tkinter.Button(root, text='Most Popular Movies', command=lambda: popularMovies_gui())
    movie_button.grid(row=2, column=1, padx=10, pady=10)
    movie_button = tkinter.Button(root, text='Top 250 Shows', command=lambda: top250Shows_gui())
    movie_button.grid(row=3, column=1, padx=10, pady=10)
    movie_button = tkinter.Button(root, text='Top 250 Movies', command=lambda: top250Movies_gui())
    movie_button.grid(row=4, column=1, padx=10, pady=10)
    up_down_button = tkinter.Button(root, text='Up and Down ', command=lambda: upDown('popularMovies',
                                                                                      'popularTv',
                                                                                      'showsDb.sqlite'))
    up_down_button.grid(row=5, column=1, padx=10, pady=10)
    up_down_button = tkinter.Button(root, text='Movies appearing \n in most popular movies\n and top 250 movies',
                                    command=lambda: inBoth('popular_movies', 'movies', 'shows_db.sqlite'))
    up_down_button.grid(row=6, column=1, padx=10, pady=10)
    up_down_button = tkinter.Button(root, text='Shows appearing \n in most popular shows\n and top 250 shows',
                                    command=lambda: inBoth('popular_tv', 'shows', 'shows_db.sqlite'))
    up_down_button.grid(row=7, column=1, padx=10, pady=10)
    root.mainloop()


def popularShows_gui():
    pop_tv = Sprint3.get_data(f"https://imdb-api.com/en/API/MostPopularTVs/{secrets}")
    mostPopular(pop_tv, 'popular_tv', "Most Popular Tv Shows", '2000x600', 'showsDb.sqlite')


def popularMovies_gui():
    pop_movies = Sprint3.get_data(f"https://imdb-api.com/en/API/MostPopularMovies/{secrets}")
    mostPopular(pop_movies, 'popular_movies', "Most Popular Movies", '2000x600', 'showsDb.sqlite')


def top250Shows_gui():
    shows = Sprint3.get_data(f"https://imdb-api.com/en/API/Top250TVs/{secrets}")
    top250Tables(shows, 'shows', "Top 250 Shows", '2000x600')


def top250Movies_gui():
    movies = Sprint3.get_data(f"https://imdb-api.com/en/API/Top250Movies/{secrets}")
    top250Tables(movies, 'movies', "Top 250 Movies", '2000x600')


def mostPopular(data, table_name, title, geometry, db_name):
    root = tkinter.Tk()
    root.title(title)
    root.geometry(geometry)

    frame2 = scrollbar(root)
    rankStatement = '''SELECT * from ''' + table_name + ''' ORDER BY rank DESC'''
    upDownStatement = '''SELECT * from ''' + table_name + ''' ORDER BY rankUpDown ASC'''

    labeling(data, table_name, title, geometry, frame2, rankStatement, upDownStatement,
             db_name)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''SELECT * from ''' + table_name)
    fillWindow(data, cursor, frame2)


def top250Tables(data, table_name, title, geometry):
    root = tkinter.Tk()
    root.title(title)
    root.geometry(geometry)
    second_frame = scrollbar(root)
    Id = tkinter.Label(second_frame, text='id')
    Id.grid(row=0, column=0)
    title = tkinter.Label(second_frame, text='title')
    title.grid(row=0, column=1)
    year = tkinter.Label(second_frame, text='year')
    year.grid(row=0, column=2)
    director = tkinter.Label(second_frame, text='crew')
    director.grid(row=0, column=3)
    imdbRating = tkinter.Label(second_frame, text='imDbRating')
    imdbRating.grid(row=0, column=4)
    imdbCount = tkinter.Label(second_frame, text='imDbRatingCount')
    imdbCount.grid(row=0, column=5)
    ratingsLabel = tkinter.Label(second_frame, text='Ratings (if available)')
    ratingsLabel.grid(row=0, column=6)
    conn = sqlite3.connect('showsDb.sqlite')
    cursor = conn.cursor()
    cursor.execute('''SELECT * from ''' + table_name)

    for i in range(len(data)):
        record = cursor.fetchone()
        idIn = Label(second_frame, text=str(record[0]))
        idIn.grid(row=i + 1, column=0)
        fullTitleIn = Label(second_frame, text=str(record[2]))
        fullTitleIn.grid(row=i + 1, column=1)
        yearIn = Label(second_frame, text=str(record[3]))
        yearIn.grid(row=i + 1, column=2)
        directorIn = Label(second_frame, text=str(record[4]))
        directorIn.grid(row=i + 1, column=3)
        imdbRatingIn = Label(second_frame, text=str(record[5]))
        imdbRatingIn.grid(row=i + 1, column=4)
        imdbCountIn = Label(second_frame, text=str(record[6]))
        imdbCountIn.grid(row=i + 1, column=5)
        ratingsIn = tkinter.Button(second_frame, text='Ratings')
        ratingsIn.grid(row=i + 1, column=6)


def upDownSorting(data, table_name, title, geometry, select_statement, db_name):
    root = tkinter.Tk()
    root.title(title)
    root.geometry(geometry)
    frame2 = scrollbar(root)
    rankStatement = '''SELECT * from ''' + table_name + ''' ORDER BY rank ASC'''
    upDownStatement = '''SELECT * from ''' + table_name + ''' ORDER BY rankUpDown DESC'''
    labeling(data, table_name, title, geometry, frame2, rankStatement, upDownStatement,
             'showsDb.sqlite')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    statement = select_statement
    cursor.execute(statement)
    fillWindow(data, cursor, frame2)


def fillWindow(data, cursor, second_frame):
    for i in range(len(data)):
        record = cursor.fetchone()
        idIn = Label(second_frame, text=str(record[0]))
        idIn.grid(row=i + 1, column=0)
        rankIn = Label(second_frame, text=str(record[1]))
        rankIn.grid(row=i + 1, column=1)
        upDownIn = Label(second_frame, text=str(record[2]))
        upDownIn.grid(row=i + 1, column=2)
        full_title = Label(second_frame, text=str(record[4]))
        full_title.grid(row=i + 1, column=3)
        yearIn = Label(second_frame, text=str(record[5]))
        yearIn.grid(row=i + 1, column=4)
        crewIn = Label(second_frame, text=str(record[6]))
        crewIn.grid(row=i + 1, column=5)
        imdbRatingIn = Label(second_frame, text=str(record[7]))
        imdbRatingIn.grid(row=i + 1, column=6)
        imdbCountIn = Label(second_frame, text=str(record[8]))
        imdbCountIn.grid(row=i + 1, column=7)
        ratingsIn = tkinter.Button(second_frame, text='Ratings', command=lambda: ratingsCheck(cursor, record))
        ratingsIn.grid(row=i + 1, column=8)


def ratingsCheck(cursor, record):
    root = Tk()
    root.title = 'Ratings'
    root.geometry = '1000x1000'
    if cursor.execute('''SELECT * from movie_ratings WHERE movie_ratings.fullTitle = ''' + str(record[4])):
        ratings = cursor.fetchone()
        ratingsIn = Label(root, text=str(ratings))
        ratingsIn.grid(row=1, column=1, rowspan=10, columnspan=10)
    else:
        ratingsIn = Label(root, text='No Ratings for this movie')
        ratingsIn.grid(row=1, column=1)


def scrollbar(root):
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)
    background = Canvas(frame)
    background.pack(side=LEFT, fill=BOTH, expand=1)
    ScrollBar = ttk.Scrollbar(frame, orient=VERTICAL, command=background.yview)
    ScrollBar.pack(side=RIGHT, fill=Y)
    background.configure(yscrollcommand=frame.set)
    background.bind('<Configure>', lambda e: background.configure(scrollregion=background.bbox("all")))
    frame2 = Frame(background)
    background.create_window((0, 0), window=frame2, anchor="nw")

    return frame2


def labeling(data, table_name, title, geometry, second_frame, rank_statement, up_down_statement, db_name):
    Id = tkinter.Label(second_frame, text='id')
    Id.grid(row=0, column=0)
    rankButton = tkinter.Button(second_frame, text='rank',
                                command=lambda: upDownSorting(data, table_name, title, geometry,
                                                              rank_statement, db_name))
    rankButton.grid(row=0, column=1)
    upDownButton = tkinter.Button(second_frame, text='rankUpDown',
                                  command=lambda: upDownSorting(data, table_name, title, geometry,
                                                                up_down_statement, db_name))
    upDownButton.grid(row=0, column=2)
    title = tkinter.Label(second_frame, text='title')
    title.grid(row=0, column=3)
    year = tkinter.Label(second_frame, text='year')
    year.grid(row=0, column=4)
    director = tkinter.Label(second_frame, text='director')
    director.grid(row=0, column=5)
    imdb_rating = tkinter.Label(second_frame, text='imDbRating')
    imdb_rating.grid(row=0, column=6)
    imdb_count = tkinter.Label(second_frame, text='imDbRatingCount')
    imdb_count.grid(row=0, column=7)
    ratings = tkinter.Label(second_frame, text='Ratings (if available)')
    ratings.grid(row=0, column=8)


def upDown(first_table, second_table, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''SELECT * from ''' + first_table + ''' rankUpDown > 0''')
    moviesUp = cursor.fetchall()
    cursor.execute('''SELECT * from ''' + first_table + ''' rankUpDown < 0''')
    moviesDown = cursor.fetchall()
    cursor.execute('''SELECT * from ''' + second_table + ''' rankUpDown > 0''')
    showsUp = cursor.fetchall()
    cursor.execute('''SELECT * from ''' + second_table + ''' rankUpDown < 0''')
    showsDown = cursor.fetchall()
    data = {'Movies Rank up': len(moviesUp), 'Movies Rank down': len(moviesDown),
            'Shows Rank up': len(showsUp), 'Shows Rank down': len(showsDown)}
    up_down = list(data.keys())
    values = list(data.values())
    fig = plot.figure(figsize=(10, 5))
    plot.bar(up_down, values, color='maroon', width=0.4)
    plot.ylabel("Number of shows and movies")
    plot.title("Shows and Movies Movements")
    plot.show()


def bothTables(first_table_name, second_table_name, db_name):
    root = tkinter.Tk()
    root.title("Existing In Both")
    root.geometry('1000x1000')
    second_frame = scrollbar(root)

    in_both = inBoth(first_table_name, second_table_name, db_name)

    idLabel = tkinter.Label(second_frame, text='id')
    idLabel.grid(row=0, column=0)
    rankingsButton = tkinter.Label(second_frame, text='rank')
    rankingsButton.grid(row=0, column=1)
    upDownButton = tkinter.Label(second_frame, text='rankUpDown')
    upDownButton.grid(row=0, column=2)
    titleLabel = tkinter.Label(second_frame, text='title')
    titleLabel.grid(row=0, column=3)
    yearLabel = tkinter.Label(second_frame, text='year')
    yearLabel.grid(row=0, column=4)

    for i in range(len(in_both)):
        record = in_both[i]
        idInput = Label(second_frame, text=str(record[0]))
        idInput.grid(row=i + 1, column=0)
        rankInput = Label(second_frame, text=str(record[1]))
        rankInput.grid(row=i + 1, column=1)
        upDownInput = Label(second_frame, text=str(record[2]))
        upDownInput.grid(row=i + 1, column=2)
        fullTitleInput = Label(second_frame, text=str(record[4]))
        fullTitleInput.grid(row=i + 1, column=3)
        yearInput = Label(second_frame, text=str(record[5]))
        yearInput.grid(row=i + 1, column=4)


def inBoth(first_table_name, second_table_name, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''SELECT * from ''' + first_table_name +
                   ''' INNER JOIN ''' + second_table_name +
                   ''' on ''' + first_table_name + '''.fullTitle = ''' + second_table_name + '''.fullTitle''')
    in_both = cursor.fetchall()
    return in_both
