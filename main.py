# Mark Feehily
# professor Santore
# COMP 490
# 2/2/22

import secrets
import sqlite3
import sys
import requests


def top_250():
    url = f"https://imdb-api.com/en/API/Top250TVs/k_12345678"
    results = requests.get(url)
    if results.status_code != 200:
        print(f"Failed to get data {results.status_code}error{results.reason} ")
        sys.exit(-1)
    response = results.json()
    show_list = response["items"]
    return show_list


def get_results(data_to_write: list[dict]):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def find_ratings(top_show_data: list[dict]) -> list[dict]:
    results = []
    api_queries = []
    base_query = f"https://imdb-api.com/en/API/UserRatings/{secrets}/tt1375666/"
    wheel_of_time_query = f"{base_query}tt7462410"
    api_queries.append(wheel_of_time_query)
    first_query = f"{base_query}{top_show_data[1]['id']}"
    api_queries.append(first_query)
    fifty_query = f"{base_query}{top_show_data[49]['id']}"
    api_queries.append(fifty_query)
    hundred_query = f"{base_query}{top_show_data[99]['id']}"
    api_queries.append(hundred_query)
    two_hundred = f"{base_query}{top_show_data[199]['id']}"
    api_queries.append(two_hundred)
    for query in api_queries:
        response = requests.get(query)
        if response.status_code != 200:
            print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
            continue
        rating_data = response.json()
        results.append(rating_data)
    return results


def main():
    top_show_data = top_250()
    ratings_data = find_ratings(top_show_data)
    get_results(ratings_data)
    get_results(top_show_data)


if __name__ == '__main__':
    main()
