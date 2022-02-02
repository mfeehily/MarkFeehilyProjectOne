# Mark Feehily
# professor Santore
# COMP 490
# 2/2/22

from bs4 import BeautifulSoup
import requests
import secrets


def main():
    url = f"https://imdb-api.com/en/API/UserRatings/{secrets}/tt1375666"
    results = requests.get(url)
    soup = BeautifulSoup(results.content, 'lxml')

    # created Lists that hold movie data
    title = []
    year = []
    director = []
    rating = []

    tables = soup.body.find("tbody", {"class": "lister-list"})
    # finds the title, year, and director of movie
    titles = tables.find_all("td", {"class": "titleColumn"})
    for x in titles:
        # appends the titles
        title.append(x.a.get_text())
        # finds the years of the movies
        years = x.find("span", {"class": "secondaryInfo"}).get_text()
        year.append(years[1:-1])
        # finds the director of the movies
        directors = x.a['title'].split("(dir.)")
        director.append(directors[0])
    # add rating to each movie
    rating1 = tables.find_all("td", {"class": "imdbRating"})

    for x in rating1:
        rating.append(x.get_text().strip())
    # Printing the data to the terminal
    print(title)
    print(year)
    print(director)
    print(rating)
    print("length = ", len(title))
    response = (title + year + director + rating)
    # Writing movie data to a file
    with open('test.txt', 'w') as file:
        file.write(response)
    # when results are not equal to 200 prints "results are not equal to 200"
    if results.status_code != 200:
        print("results are not equal to 200")
        return

    # data = results.json()
    # file = open("test", "w")
    # file.write(response)
