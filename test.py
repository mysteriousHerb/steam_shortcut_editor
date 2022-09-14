import requests
from bs4 import BeautifulSoup


appid = "690040"
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
    print(game_name)
    print(image_url)