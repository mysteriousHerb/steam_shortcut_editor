import vdf
from steamgrid import SteamGridDB
import json
import requests
import os
import time

shortcut_path = "shortcuts.vdf"
with open(shortcut_path, 'rb') as appinfo:
    shortcuts = vdf.binary_loads(appinfo.read())["shortcuts"]
    print(shortcuts)