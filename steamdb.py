import requests
from bs4 import BeautifulSoup
import os, sys


# send a requests query to the steamdb api

def search_game(game_name):
    url = f"https://store.steampowered.com/search/?term={game_name}"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
    # find class name ais-Hits-list
    # print(soup)
    # save soup as html
    with open('steamdb.html', 'w+', encoding="UTF-8") as f:
        f.write(soup.prettify())

    # find the element by id=search_resultsRows
    search_results_rows = soup.find(id="search_resultsRows")
    # find all the divs with class name "search_result_row"
    search_result_rows = search_results_rows.find_all("a", class_="search_result_row")
    for row in search_result_rows[:5]:
        # print the name of the game
        print(row.find("span", class_="title").text)
        # print appid of the game
        print(row["data-ds-appid"])
        # image url
        print(row.find("img")["src"])

    # print(search_results)
    # find all the class name="search_result_row "
    # search_results = search_results.find_all(class_="search_result_row ")



# https://steamdb.info/instantsearch/?query={}


search_game("LegionCraft")
