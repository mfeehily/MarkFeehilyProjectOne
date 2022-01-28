import requests
import secrets


def main():
    loc = f"https://imdb-api.com/en/API/UserRatings/{secrets}/tt1375666"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help")
        return

    data = results.json()

    with open ('test.txt', 'W') as f:
        print(results)

