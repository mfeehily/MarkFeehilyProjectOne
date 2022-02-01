from bs4 import BeautifulSoup
import requests
import secrets
import re


def main():
    films = []
    names = []
    ratings = []
    genres = []

    url = f"https://imdb-api.com/en/API/UserRatings/{secrets}/tt1375666"
    results = requests.get(url)
    soup = BeautifulSoup(results.content, features="html.parser")
    containers = soup.find_all("div", class_="lister-item-content")

    title = films.lower()

    for result in containers:
        name1 = result.h3.a.text
        name = result.h3.a.text.lower()
        if title in name:
            rating = result.find("div", class_="inline-block ratings-imdb-rating")["data-value"]

            genre = result.p.find("span", class_="genre")
            genre = genre.contents[0]
            names.append(name1)
            ratings.append(rating)
            genres.append(genre)

            print(films + ratings + name)

    # if results.status_code != 200:
        # print("help")
        # return

    # data = results.json()

    # file = open("test", "w")
    # file.write(data)
