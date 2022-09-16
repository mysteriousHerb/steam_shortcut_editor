## Steam shortcut editor

### Purpose:
allow you to modify the shortcuts file quickly and set game name to be the appid so you have access to community controls

### usage:
![](data/usage_demo.gif)

### How to build
/home/deck/anaconda3/bin/python -m PyInstaller app.py --noconfirm  --onefile --name shortcut_editor --icon="data/logo_square.ico", such as using pipenv
### For development
- clone the repo to your computer `git clone https://github.com/herbzhao/steam_shortcut_editor.git`
- create a virtual environment if preferred, such as using pipenv
- install the necessary modules: `pip3 install -r requirements.txt` or `python -m pip install -r requirements.txt`
- For people on steamdeck, I had huge problem getting tkinter installed, the final solution was using anaconda https://www.anaconda.com/products/distribution
