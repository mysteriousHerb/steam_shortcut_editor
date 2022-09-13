# img_viewer.py
import requests
import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk
from io import BytesIO
from read_vdf import ShortcutConverter


# create a gui that can display image from URL
# example image: https://cdn.cloudflare.steamstatic.com/steam/apps/1799930/capsule_sm_120.jpg
# download image


def download_image(url):
    # download image
    response = requests.get(url)
    # use pillow to convert the image as png
    img = Image.open(BytesIO(response.content))
    img = img.resize((120*2, 45*2), Image.Resampling.LANCZOS)
    png_bio = BytesIO()
    img.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()
    return png_data


def update_game_list():
    shortcut_list = ["1#control", "2#witcher 3", "3#backpack hero", "4#Shotgun King: The Final Checkmate", "5#Moonlight", "6#870780", "7#690040"]

    return shortcut_list, game_name_list, appid_list


def app_window():
    # Define the window's contents

    shortcut_converter = ShortcutConverter()

    top_row = [
        [
            sg.Button("Load non-steam games", key="LOAD_SHORTCUT"),
            sg.Button("Update gamename", key="GAME_NAME"),
            sg.Button("Update appid", key="APPID"),
            sg.Button("Quit"),
        ]
    ]
    column_1 = [
        [sg.Text("Shortcut")],
        [
            # add a label
            sg.Listbox(values=[], size=(30, 20), key="-SHORTCUT_LIST-", enable_events=True)
        ],
    ]
    column_2 = [
        [sg.Text("Steam game name")],
        [
            sg.Listbox(values=[], size=(30, 20), key="-GAMENAME_LIST-", enable_events=True),
        ],
    ]

    column_3 = [
        [sg.Text("Steam APPID")],
        [
            sg.Listbox(values=[], size=(10, 20), key="-APPID_LIST-", enable_events=True),
        ],
    ]

    column_4 = [
        [
            sg.Image("logo_wide_small.png", key="-IMAGE-", size = (120*2, 45*2)),
        ]
    ]

    layout = [[top_row, sg.Column(column_1), sg.Column(column_2), sg.Column(column_3), sg.Column(column_4)]]

    game_name_list = appid_list = []
    # Create the window
    window = sg.Window("Steam shortcut manager", layout, resizable=True, size=(1000, 200))

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        if event == "LOAD_SHORTCUT":
            shortcut_list = update_game_list()
            window["-SHORTCUT_LIST-"].update(shortcut_list)

        if event == "-SHORTCUT_LIST-":
            # prevent clicking empty list
            if len(values["-SHORTCUT_LIST-"]) > 0:
                selected = values["-SHORTCUT_LIST-"][0]
                game_name = selected.split("#")[1]
                if not game_name.isnumeric():
                    sanitised_results = shortcut_converter.search_game_name(game_name)
                    steam_game_name_list = [result["game_name"] for result in sanitised_results]
                    window["-GAMENAME_LIST-"].update(steam_game_name_list)
                    appid_list = [result["appid"] for result in sanitised_results]
                    window["-APPID_LIST-"].update(appid_list)
                    img_url_list = [result["image_url"] for result in sanitised_results]

                else:
                    sanitised_results = shortcut_converter.search_appid(game_name)
                    steam_game_name_list = [result["game_name"] for result in sanitised_results]
                    window["-GAMENAME_LIST-"].update(steam_game_name_list)
                    appid_list = [result["appid"] for result in sanitised_results]
                    window["-APPID_LIST-"].update(appid_list)
                    img_url_list = [result["image_url"] for result in sanitised_results]

        if event == "-GAMENAME_LIST-":
            # prevent clicking empty list
            if len(values["-GAMENAME_LIST-"]) > 0:
                selected = values["-GAMENAME_LIST-"]
                indexes = [steam_game_name_list.index(i) for i in selected]
                window["-APPID_LIST-"].update(set_to_index=indexes)
                # update image
                img_url = img_url_list[indexes[0]]
                png_data = download_image(img_url)
                window["-IMAGE-"].update(data=png_data)

        if event == "-APPID_LIST-":
            # prevent clicking empty list
            if len(values["-APPID_LIST-"]) > 0:
                selected = values["-APPID_LIST-"]
                indexes = [appid_list.index(i) for i in selected]
                window["-GAMENAME_LIST-"].update(set_to_index=indexes)
                # update image
                img_url = img_url_list[indexes[0]]
                png_data = download_image(img_url)
                window["-IMAGE-"].update(data=png_data)

    window.close()
    # "LISTBOX_SELECT_MODE_" and include: LISTBOX_SELECT_MODE_SINGLE LISTBOX_SELECT_MODE_MULTIPLE LISTBOX_SELECT_MODE_BROWSE LISTBOX_SELECT_MODE_EXTENDED

    # def game_entry_row(game_name, appid):
    #     layout = [
    #         # a check box
    #         [sg.Checkbox("enable", key="-CHECKBOX-")],
    #         [sg.Text(f"{game_name}"), sg.Input(key="-GAME_NAME-")],
    #         [sg.Text(f"{appid}"), sg.Input(key="-GAME_ID-")],
    #     ]


if __name__ == "__main__":
    download_image("https://cdn.cloudflare.steamstatic.com/steam/apps/1799930/capsule_sm_120.jpg")
    app_window()
