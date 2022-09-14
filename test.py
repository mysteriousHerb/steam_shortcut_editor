import vdf
shortcut_path = "shortcuts.vdf"
with open(shortcut_path, 'rb') as appinfo:
    shortcuts = vdf.binary_loads(appinfo.read())["shortcuts"]
    shortcut_names = [i["AppName"] for i in shortcuts.values()]

print(shortcuts["1"])