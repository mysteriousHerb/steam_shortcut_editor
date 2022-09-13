from email import header
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


import os, sys

# export PATH=$PATH:/home/deck/Documents/github/shortcut_editor


binary = FirefoxBinary(r'/home/deck/.local/share/flatpak/app/org.mozilla.firefox/current/active/export/share/applications/org.mozilla.firefox.desktop')

driver = webdriver.Firefox(firefox_binary=binary)
driver.get("http://www.python.org")


# export PATH="/home/deck/Documents/github/shortcut_editor/"
# export PATH="/var/lib/flatpak/app/com.microsoft.Edge/current/active/export/share/applications/"

# options = Options()
# options.binary_location = r"/home/deck/Documents/github/shortcut_editor/msedgedriver"

# driver = webdriver.Edge(executable_path=r"/home/deck/Documents/github/shortcut_editor/msedgedriver")
# driver.get('https://bing.com')




# send a requests query to the steamdb api

def search_game(game_name):
    url = f"https://steamdb.info/instantsearch/?query={game_name}"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
    # find class name ais-Hits-list
    print(soup)
    # save soup as html
    with open('steamdb.html', 'w') as f:
        f.write(soup.prettify())

    results = soup.find_all("div", class_="ais-Hits-list")
    print(results)
# https://steamdb.info/instantsearch/?query={}


# search_game("control")