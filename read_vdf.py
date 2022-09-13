import vdf
from steamgrid import SteamGridDB
import json
import requests
import os
import time

import requests
from bs4 import BeautifulSoup
import os, sys

import jellyfish


# create a new class
class ShortcutConverter():
    def __init__(self):
        pass

    def convert_shortcut(self, shortcut_path):
        with open(shortcut_path, 'rb') as appinfo:
            shortcuts = vdf.binary_loads(appinfo.read())["shortcuts"]
        for shortcut in shortcuts.values():
            # using griddb to find nearest match
            if shortcut["AppName"].isnumeric():
                appid = int(shortcut["AppName"])
                self.search_appid(appid)
            else:
                game_name = shortcut["AppName"]
                self.search_game_name(game_name)


    # load steam library
    def search_game_name(self, game_name):
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
        for row in search_result_rows[:1]:
            steam_game_name = row.find("span", class_="title").text
            steam_appid = row["data-ds-appid"]
            image_url = row.find("img")["src"]
            # if the game name is too different, discard the result
            if jellyfish.jaro_distance(steam_game_name.lower(), game_name.lower()) > 0.7:
                print(f"Finding {game_name} @steam: {steam_game_name} - AppID: {steam_appid}: Image URL: {image_url}")
            else:
                print(f"Cannot find game {game_name} on steam")


    def search_appid(self, appid):
        # load steam app list if self.applist doesnt exist
        if not hasattr(self, "applist"):
            self.load_steam_applist()
        # search for the game id
        try:
            game_name = self.applist_names[self.applist_appids.index(appid)]
            print(f"Game Name: {game_name}: steam_AppID: {appid}")
        except ValueError:
            print(f"Game ID {appid} not found")


    def load_steam_applist(self):
        applist_path = "steam_applist.json"
        # check created time, if older than 1 day, update
        if not os.path.exists(applist_path) or os.stat(applist_path).st_mtime > time.time() - 86400:
            # download the latest steam app list
            url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
            r = requests.get(url, allow_redirects=True)
            open('steam_applist.json', 'wb+').write(r.content)

        with open('applist.json', encoding="UTF-8") as f:
            steam_applist = json.load(f)
            self.steam_applist = steam_applist["applist"]["apps"]
            self.applist_names = [i["name"] for i in self.steam_applist]
            self.applist_appids = [i["appid"] for i in self.steam_applist]

        

if __name__ == "__main__":
    shortcut_converter = ShortcutConverter()
    # shortcut_converter.search_game_name("control")
    # shortcut_converter.search_appid(1174180)
    shortcut_converter.convert_shortcut("shortcuts.vdf")

