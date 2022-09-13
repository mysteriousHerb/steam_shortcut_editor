import vdf
from steamgrid import SteamGridDB
import json
import requests
import os
import time

shortcut_path = "shortcuts.vdf"
with open(shortcut_path, 'rb') as appinfo:
    shortcuts = vdf.binary_loads(appinfo.read())["shortcuts"]
    shortcut_names = [i["AppName"] for i in shortcuts.values()]

print(shortcuts["5"]["AppName"])
shortcuts["5"]["AppName"] = "test"

dump = vdf.binary_dumps({"shortcuts": shortcuts})
with open("shortcuts_backup.vdf", 'wb+') as appinfo:
    appinfo.write(dump)

with open("shortcuts_backup.vdf", 'rb') as appinfo:
    shortcuts = vdf.binary_loads(appinfo.read())
    shortcut_names = [i["AppName"] for i in shortcuts["shortcuts"].values()]

print(shortcuts["shortcuts"]["5"]["AppName"])