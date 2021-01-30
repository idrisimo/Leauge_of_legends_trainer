import requests, urllib.request, json, ssl
from bs4 import BeautifulSoup
from tkinter import *

upgradedictonary = {"level_1": "", "level_2": "", "level_3": "", "level_4": "",
                    "level_5": "", "level_6": "", "level_7": "", "level_8": "",
                    "level_9": "", "level_10": "", "level_11": "", "level_12": "",
                    "level_13": "", "level_14": "", "level_15": "", "level_16": "",
                    "level_17": "", "level_18": ""}


# This section simply gets data from website
def geturldata(url):
    src = url.content
    soup = BeautifulSoup(src, "lxml")
    global find_name
    global web_lists
    find_name = soup.find_all("h3")
    web_lists = soup.find_all("li")
    # app.after(1000, geturldata)


# Grab champion name
def getchamp_name(find_name):
    for names in find_name:
        if names.text.endswith("Top Items"):
            champion_name = names.text.replace("'s Top Items", "")
            return champion_name


# Grabs web lists and throws out everything not needed.
def getupgrade_list(web_lists):
    upgrade_list = []
    for upgrades in web_lists:
        if "level" in upgrades.attrs:
            upgrade_list.append(upgrades.attrs)
    # This converts the list into binary so easier to work with.
    upgrade_list_binary = []
    for upgrade in upgrade_list:
        if "class" in upgrade.keys():
            upgrade_list_binary.append(1)
        else:
            upgrade_list_binary.append(0)
    ability_1 = upgrade_list_binary[0:18]
    ability_2 = upgrade_list_binary[18:36]
    ability_3 = upgrade_list_binary[36:54]
    ability_4 = upgrade_list_binary[54:72]
    ability_upgrade_list = [[ability_1] + [ability_2] + [ability_3] + [ability_4]]
    count = 0
    letters = ["Q", "W", "E", "R"]
    for i in ability_upgrade_list:
        for e in i:
            limit = 0
            while limit != 18:
                if e[limit] == 1:
                    upgradedictonary.update({"level_" + str(limit + 1): letters[count]})
                limit += 1
            count += 1


# Get player level from current match
# creates a default certificate so that the json_obj doesn't crap itself.
ssl._create_default_https_context = ssl._create_unverified_context


# Gets the current players level.
def getcurlevel():
    curgame_url = "https://127.0.0.1:2999/liveclientdata/activeplayer"
    curmatch_json = urllib.request.urlopen(curgame_url)
    curgame_data = json.load(curmatch_json)
    curchampion_level = curgame_data["level"]
    return curchampion_level


# TODO Build GUI
app = Tk()
app.title("League of Legends Trainer")
app.geometry("300x250")

lab1 = Label(app, text="Enter URL: ")
lab1.grid(row=0, column=0)
url_entry = Entry(app)
url_entry.grid(row=0, column=1)


def build():
    url = url_entry.get()
    str(url)
    buildurl = requests.get(url)
    geturldata(buildurl)


submit = Button(app, text="Submit", command=build)
submit.grid(row=0, column=2)

lab2 = Label(app, text="Champion: ")
lab2.grid(row=1, column=0)
champ_name = Label(app)
champ_name.grid(row=1, column=1)


def c_name():
    try:
        champ_name.config(text=getchamp_name(find_name), fg="black")
        app.after(1000, c_name)
    except:
        champ_name.config(text="No URL", fg="red")
        app.after(1000, c_name)


c_name()

lab4 = Label(app, text="Ability to level up: ")
lab4.grid(row=4, column=0)
abilitykey = Label(app)
abilitykey.grid(row=5, column=0)


def upgrade():
    try:
        getupgrade_list(web_lists)
        app.after(1000, upgrade)
    except:
        abilitykey.config(text="No URL")
        app.after(1000, upgrade)


upgrade()


def update_abilitykey():
    try:
        display_upgrade = upgradedictonary["level_" + str(getcurlevel())]
        abilitykey.config(text=display_upgrade, fg="blue")
        app.after(1000, update_abilitykey)
    except:
        abilitykey.config(text="Game not started", fg="red")
        app.after(1000, update_abilitykey)


update_abilitykey()

app.mainloop()
