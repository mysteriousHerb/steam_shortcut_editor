import vdf
from steamgrid import SteamGridDB
import json
import requests
import os
import time

applist_path = "steam_applist.json"

# load steam library

# check created time, if older than 1 day, update
if os.path.exists(applist_path):
    if os.stat(applist_path).st_mtime < time.time() - 86400:
        url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        r = requests.get(url, allow_redirects=True)
        open('steam_applist.json', 'wb+').write(r.content)
else:
    url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    r = requests.get(url, allow_redirects=True)
    open('steam_applist.json', 'wb+').write(r.content)

with open('applist.json') as f:
    steam_applist = json.load(f)
    steam_applist = steam_applist["applist"]["apps"]

# convert lists of dictionary into two lists for fast searching
applist_names = [i["name"] for i in steam_applist]
applist_appids = [i["appid"] for i in steam_applist]

def search_steam_applist(game_name):
    url = f"https://www.steamgriddb.com/api/v2/search/autocomplete/{game_name}"
    headers = {"Authorization": "Bearer 446cecd21f68a3385bcdfe953ccc7390"}
    r = requests.get(url, headers=headers)
    return r.json()

sgdb = SteamGridDB('446cecd21f68a3385bcdfe953ccc7390')
# load all the non-steam game shortcuts
with open('shortcuts.vdf', 'rb') as appinfo:
    shortcuts = vdf.binary_loads(appinfo.read())["shortcuts"]

for shortcut in shortcuts.values():
    # using griddb to find nearest match
    match_results = sgdb.search_game(shortcut["AppName"])
    # using the first result as closest match - future can be selectable by user
    if len(match_results) > 0:
        game_name = match_results[0].name
        # find index of game by matching the name
        try: 
            index = applist_names.index(game_name)
            # get the id of the game
            appid = applist_appids[index]
            print(f"Game: {game_name}, ID: {appid}")
        except ValueError:
            print(f"Game: {game_name}: not found")

    else:
        print(f"Game: {game_name}: not found")

