# img_viewer.py
import requests
import PySimpleGUI as sg
import os.path
from PIL import Image, ImageTk
from io import BytesIO
from read_vdf import ShortcutConverter
import shutil



# create a gui that can display image from URL
# example image: https://cdn.cloudflare.steamstatic.com/steam/apps/1799930/capsule_sm_120.jpg
# download image

# create a new class for GUI
class GUI():
    def __init__(self):
        self.shortcut_converter = ShortcutConverter()
        # default path
        shortcut_path = r"/home/deck/.local/share/Steam/userdata/"
        self.shortcut_path = os.path.join(shortcut_path, os.listdir(shortcut_path)[0], "config/shortcuts.vdf")
        self.logo_url = "https://i.imgur.com/dHLVSds.png"

    def download_image(self, url=""):
        # download image
        if url == "":
            url = self.logo_url
        response = requests.get(url)
        # use pillow to convert the image as png
        img = Image.open(BytesIO(response.content))
        img = img.resize((120*2, 45*2), Image.Resampling.LANCZOS)
        png_bio = BytesIO()
        img.save(png_bio, format="PNG")
        png_data = png_bio.getvalue()
        return png_data

    def find_steam_game(self):
        # prevent clicking empty list
        if len(self.values["-SHORTCUT_LIST-"]) > 0:
            selected = self.values["-SHORTCUT_LIST-"][0]
            game_name = selected.split("#")[1]
            if not game_name.isnumeric():
                sanitised_results = self.shortcut_converter.search_game_name(game_name)
                self.steam_game_name_list = [result["game_name"] for result in sanitised_results]
                self.window["-GAMENAME_LIST-"].update(self.steam_game_name_list)
                self.appid_list = [result["appid"] for result in sanitised_results]
                self.window["-APPID_LIST-"].update(self.appid_list)
                self.img_url_list = [result["image_url"] for result in sanitised_results]

            else:
                sanitised_results = self.shortcut_converter.search_appid(game_name)
                self.steam_game_name_list = [result["game_name"] for result in sanitised_results]
                self.window["-GAMENAME_LIST-"].update(self.steam_game_name_list)
                self.appid_list = [result["appid"] for result in sanitised_results]
                self.window["-APPID_LIST-"].update(self.appid_list)
                self.img_url_list = [result["image_url"] for result in sanitised_results]

    def load_shortcut(self):
        self.shortcuts, self.shortcut_names= self.shortcut_converter.load_shortcut(self.shortcut_path)
        # append a 1# to the front of the shortcut name to prevent duplicates
        self.shortcut_names= [f"{i}#{name}" for i, name in enumerate(self.shortcut_names)]

        self.window["-SHORTCUT_LIST-"].update(self.shortcut_names)

    def backup_shortcut(self):
        shutil.copyfile(self.shortcut_path, self.shortcut_path.replace(".vdf", "_backup.vdf"))


    def refresh_selection(self, mode):
        if mode == "shortcut_list":
            if len(self.values["-SHORTCUT_LIST-"]) > 0:
                # default to select the first game of the list
                self.window["-APPID_LIST-"].update(set_to_index=0)
                self.window["-GAMENAME_LIST-"].update(set_to_index=0)
                img_url = self.img_url_list[0]
                png_data = self.download_image(img_url)
                self.window["-IMAGE-"].update(data=png_data)
                


        if mode == "gamename_list":
            if len(self.values["-GAMENAME_LIST-"]) > 0:
                selected = self.values["-GAMENAME_LIST-"]
                indexes = [self.steam_game_name_list.index(i) for i in selected]
                self.window["-APPID_LIST-"].update(set_to_index=indexes)
                # update image
                img_url = self.img_url_list[indexes[0]]
                png_data = self.download_image(img_url)
                self.window["-IMAGE-"].update(data=png_data)

        elif mode == "appid_list":
            # prevent clicking empty list
            if len(self.values["-APPID_LIST-"]) > 0:
                selected = self.values["-APPID_LIST-"]
                indexes = [self.appid_list.index(i) for i in selected]
                self.window["-GAMENAME_LIST-"].update(set_to_index=indexes)
                # update image
                img_url = self.img_url_list[indexes[0]]
                png_data = self.download_image(img_url)
                self.window["-IMAGE-"].update(data=png_data)
        pass


    def replace_name(self, mode="manual"):
        if len(self.values["-SHORTCUT_LIST-"]) > 0:
            selected = self.values["-SHORTCUT_LIST-"][0]
            shortcut_index = self.shortcut_names.index(selected)
            if mode == "manual":
                if len(self.values["-MANUAL_NAME-"]) > 0:
                    manual_game_name = self.values["-MANUAL_NAME-"]
                    self.shortcut_converter.modify_shortcut(self.shortcut_path, shortcut_index, game_name=manual_game_name)
                    self.load_shortcut()
                    self.window["-MANUAL_NAME-"].update("")
            elif mode == "gamename_list":
                if len(self.values["-GAMENAME_LIST-"]) > 0:
                    selected_game = self.values["-GAMENAME_LIST-"][0]
                    # replace the game name
                    self.shortcut_converter.modify_shortcut(self.shortcut_path, shortcut_index, game_name=selected_game)
                    # reload the shortcut
                    self.load_shortcut()

    def replace_appid(self):
        if len(self.values["-SHORTCUT_LIST-"]) > 0:
            selected = self.values["-SHORTCUT_LIST-"][0]
            shortcut_index = self.shortcut_names.index(selected)
            # which game to replace with?
            if len(self.values["-APPID_LIST-"]) > 0:
                selected_appid = self.values["-APPID_LIST-"][0]
                # replace the game name
                self.shortcut_converter.modify_shortcut(self.shortcut_path, shortcut_index, appid=selected_appid)
                # reload the shortcut
                self.load_shortcut()



    def app_window(self):
        # Define the window's contents

        shortcut_converter = ShortcutConverter()
        
        png_data = self.download_image()

        top_row = [
            [
                sg.Text(".vdf Path"),
                sg.Input(self.shortcut_path, key="-SHORTCUT_PATH-", enable_events=True),
                sg.FileBrowse("Browse", key="-SHORTCUT_PATH-"),
                sg.Button("Backup shortcuts", key="-BACKUP_SHORTCUT-"),
            ],
            [
                sg.Button("Load non-steam games", key="-LOAD_SHORTCUT-"),
                sg.Button("Update gamename", key="-REPLACE_NAME-"),
                sg.Button("Update appid", key="-REPLACE_APPID-"),
                sg.Button("Quit"),
            ], 
            [
                # add a input field
                sg.Button("Change name manually", key="-MANUAL_REPLACE_NAME-"),
                sg.Input(key="-MANUAL_NAME-"),
            ]
        ]
        column_1 = [
            [sg.Text("Shortcut")],
            [
                # add a label
                sg.Listbox(values=[], size=(30, 20), key="-SHORTCUT_LIST-", enable_events=True, horizontal_scroll=True)
            ],
        ]
        column_2 = [
            [sg.Text("Steam game name")],
            [
                sg.Listbox(values=[], size=(30, 20), key="-GAMENAME_LIST-", enable_events=True, horizontal_scroll=True),
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
                sg.Image(png_data, key="-IMAGE-", size = (120*2, 45*2)),
            ]
        ]

        layout = [[top_row, sg.Column(column_1), sg.Column(column_2), sg.Column(column_3), sg.Column(column_4)]]

        game_name_list = appid_list = []
        # Create the window
        self.window = sg.Window("Steam shortcut manager", layout, resizable=True, size=(900, 400))
        
        
        # Display and interact with the Window using an Event Loop
        while True:
            self.event, self.values = self.window.read()
            # See if user wants to quit or window was closed
            if self.event == "Quit" or self.event == sg.WIN_CLOSED:
                break
            if self.event == "-LOAD_SHORTCUT-":
                self.load_shortcut()
            if self.event == "-BACKUP_SHORTCUT-":
                self.backup_shortcut()

            if self.event == "-SHORTCUT_LIST-":
                self.find_steam_game()
                self.refresh_selection("shortcut_list")
                # change MANUAL_NAME to the selected game name
                if len(self.values["-SHORTCUT_LIST-"]) > 0:
                    self.window["-MANUAL_NAME-"].update(self.values["-SHORTCUT_LIST-"][0].split("#")[1])

            # update the game name
            if self.event == "-REPLACE_NAME-":
                self.replace_name(mode="gamename_list")
            
            if self.event == "-REPLACE_APPID-":
                self.replace_appid()

            if self.event == "-MANUAL_REPLACE_NAME-":
                self.replace_name(mode="manual")

            if self.event == "-SHORTCUT_PATH-":
                self.shortcut_path = self.values["-SHORTCUT_PATH-"]
                if os.path.exists(self.shortcut_path):
                    self.load_shortcut()

            if self.event == "-GAMENAME_LIST-":
                self.refresh_selection(mode="gamename_list")
                # prevent clicking empty list


            if self.event == "-APPID_LIST-":
                self.refresh_selection(mode="appid_list")

        self.window.close()

if __name__ == "__main__":
    gui = GUI()
    gui.app_window()
