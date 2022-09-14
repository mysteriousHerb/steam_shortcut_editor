import vdf
import json
import requests
import os
import time
from bs4 import BeautifulSoup
import os, sys

# create a new class
class ShortcutConverter():
    def __init__(self):
        pass

    def load_shortcut(self, shortcut_path):
        with open(shortcut_path, 'rb') as appinfo:
            shortcuts = vdf.binary_loads(appinfo.read())["shortcuts"]
            shortcut_names = [i["AppName"] for i in shortcuts.values()]
        return shortcuts, shortcut_names

    def modify_shortcut(self, shortcut_path, index, game_name=None, appid=None):
        shortcuts, shortcut_names = self.load_shortcut(shortcut_path)
        if game_name:
            shortcuts[str(index)]["AppName"] = game_name
        if appid:
            shortcuts[str(index)]["AppName"] = appid
            # shortcuts[str(index)]["appid"] = appid


        dump = vdf.binary_dumps({"shortcuts": shortcuts})
        with open(shortcut_path, 'wb+') as appinfo:
            appinfo.write(dump)


    def convert_shortcut(self, shortcut_path):
        shortcuts = self.load_shortcut(shortcut_path)

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
        # with open('steam_search.html', 'w+', encoding="UTF-8") as f:
        #     f.write(soup.prettify())

        # find the element by id=search_resultsRows
        search_results_rows = soup.find(id="search_resultsRows")
        if not search_results_rows:
            return [{"game_name": "", "appid": "", "image_url": ""}]
        # find all the divs with class name "search_result_row"
        search_result_rows = search_results_rows.find_all("a", class_="search_result_row")
        sanitised_results = []
        for row in search_result_rows[:5]:
            try: 
                steam_game_name = row.find("span", class_="title").text
                steam_appid = row["data-ds-appid"]
                image_url = row.find("img")["src"]
                sanitised_results.append({"game_name": steam_game_name, "appid": steam_appid, "image_url": image_url})
            except KeyError:
                pass
        return sanitised_results

    def search_appid(self, appid):
        # load the steam game page
        url = f"https://store.steampowered.com/app/{appid}"
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}
        soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')

        # find class of img_ctn
        img_ctn = soup.find(class_=["game_header_image_ctn", "img_ctn"])  

        if not img_ctn:
            print("Not found")
        else:
            # find image url
            game_name = soup.find("title").text.replace(" on Steam", "")
            image_url = img_ctn.find("img")["src"]

        return [{"game_name": game_name, "appid": appid, "image_url": image_url}]

        

if __name__ == "__main__":
    shortcut_converter = ShortcutConverter()
    shortcut_converter.search_game_name("control")
    # shortcut_converter.search_appid(1174180)
    # shortcut_converter.convert_shortcut("shortcuts.vdf")

