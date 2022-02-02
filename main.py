import json
from bs4 import BeautifulSoup
import requests
import secrets
def main():
    url = f"https://imdb-api.com/en/API/UserRatings/{secrets}/tt1375666"
    results = requests.get(url)
    soup = BeautifulSoup(results.content, 'lxml')
    title = []
    year = []
    director = []
    rating = []
    tables = soup.body.find("tbody", {"class": "lister-list"})
    titles = tables.find_all("td", {"class": "titleColumn"})
    for x in titles:
        title.append(x.a.get_text())
        years = x.find("span", {"class": "secondaryInfo"}).get_text()
        year.append(years[1:-1])
        directors = x.a['title'].split("(dir.)")
        director.append(directors[0])
    rating1 = tables.find_all("td", {"class": "imdbRating"})
    for x in rating1:
        rating.append(x.get_text().strip())
    print(title)
    print(year)
    print(director)
    print(rating)
    print("length = ", len(title))
    response = (title + year + director + rating)
    with open('test.txt', 'w') as file:
        file.write(response)















    if results.status_code != 200:
        print("help")
        return

    # data = results.json()
    # file = open("test", "w")
    # file.write(response)