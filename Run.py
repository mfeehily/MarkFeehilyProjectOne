# Mark Feehily
# Professor Santore
# COMP 490
# 3/6/2022

# Run - used to run GUI for sprint 4


import Sprint3
import Sprint4
import secrets


def previous_sprints():
    pop_movies = Sprint3.get_data(f"https://imdb-api.com/en/API/MostPopularMovies/{secrets}")
    movies = Sprint3.get_data(f"https://imdb-api.com/en/API/Top250Movies/{secrets}")
    pop_tv = Sprint3.get_data(f"https://imdb-api.com/en/API/MostPopularTVs/{secrets}")
    shows = Sprint3.get_data(f"https://imdb-api.com/en/API/Top250TVs/{secrets}")
    Sprint3.save(shows)
    conn, cursor = Sprint3.open_db('showsDb.sqlite')
    Sprint3.shows_table(cursor)
    Sprint3.wheelofTime_ratings()
    Sprint3.showRatings(cursor)
    Sprint3.addToShowRatings(cursor, shows)
    Sprint3.popularTv(cursor)
    Sprint3.addToPopularTv(cursor, pop_tv)
    Sprint3.moviesTable(cursor)
    Sprint3.addToMovies(cursor, movies)
    Sprint3.popularMovies(cursor)
    Sprint3.addToPopularMovies(cursor, pop_movies)
    Sprint3.movieRatings(cursor)
    Sprint3.addToMovieRatings(cursor, pop_movies)
    Sprint3.closeDataBase(conn)


def main():
    Sprint4.home_page()


if __name__ == '__main__':
    main()