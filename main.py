from data.types import id_to_name, gamedata, Types
from tkinter import Tk
from tkinter import filedialog
import eel
import os
import json
from data.hashes import Hashlist
from data.decode import Decoder
from data.encode import Encoder
from copy import deepcopy
from traceback import format_exc
from urllib.request import urlopen

options = {}
hashes = Hashlist("./data/hashes")
decoder = Decoder(hashes)
encoder = Encoder()
savefiles = {}
saveslots = {}


with open("./data/version") as f:
    currentversion = f.read()
    newversion = currentversion

def loadsettings():
    with open("./data/settings") as f:
        global options, newversion
        options = json.load(f)
        if options["checkforupdate"]:
            newversion = urlopen("https://raw.githubusercontent.com/NetroScript/Graveyard-Keeper-Savefile-Editor/master/data/version").read().decode()

@eel.expose
def getsavefiles():
    i = 1
    out = []

    for file in os.listdir(options["path"]):
        if file.endswith(".info"):
            with open(os.path.join(options["path"], file)) as f:
                data = json.load(f)
                out.append({
                    "version": round(data["version"], 3),
                    "savetime": data["real_time"],
                    "days": int(data["game_time"]),
                    "church": data["stats"].split("ss)")[1].strip(),
                    "graveyard": data["stats"].split("ll)")[1].split("(cr")[0].strip(),
                    "id": file.split(".info")[0],
                    "num": i
                })
                saveslots[i] = file.split(".info")[0]
                i += 1

    return out


@eel.expose
def getsavefile(slot, shash):
    if shash not in savefiles:
        try:
            curpath = os.path.join(options["path"], str(saveslots[int(slot)])+".dat")
            data = decoder.decode(curpath)
            data["slot"] = saveslots[int(slot)]
            savefiles[shash] = data
        except Exception:
            print("Error:")
            print(format_exc())
            return {"Error": "Seems like there was a problem while loading the file, check the console for more information"}
        return editablevalues(shash)
    else:
        return {"Error": "An instance of this save slot is already open."}


@eel.expose
def getcustomsavefile(shash):
    file = filedialog.askopenfilename(title="Select a savegame which is not created by Graveyard Keeper", defaultextension=".dat", filetypes=(("Graveyard Keeper File Save", "*.dat"), ("All Files", "*.*")))
    if file in savefiles:
        savefiles[shash] = file
        return editablevalues(file)
    try:
        data = decoder.decode(file)
        savefiles[shash] = file
        savefiles[file] = data
        return editablevalues(file)
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "The chosen .dat file doesn't seem to be a save file or the save file editor is out of date :c"}


@eel.expose
def getjsonsavefile(shash):
    file = filedialog.askopenfilename(title="Select a savegame which is exported by this application", defaultextension=".json", filetypes=(("Graveyard Keeper JSON File Save", "*.json"), ("All Files", "*.*")))
    if file in savefiles:
        savefiles[shash] = file
        return editablevalues(file)
    try:
        with open(file) as f:
            data = json.load(f)
        if "savedata" and "header" and "serializer" in data:
            savefiles[shash] = file
            savefiles[file] = data
            return editablevalues(file)
        else:
            return {"Error": "The chosen .json file doesn't seem to be an exported .json file."}
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "The chosen .json file doesn't seem to be a save file or the save file editor is out of date :c"}


@eel.expose
def saveslot(data, shash, slot):
    modifysave(data, shash)
    curpath = os.path.join(options["path"], str(saveslots[int(slot)])+".dat")
    try:
        os.replace(curpath, curpath+".back")
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "There was an error while creating the backup file."}
    try:
        encoder.encode(curpath, savefiles[shash])
        return {}
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "There was an error while generating the saved file."}


@eel.expose
def savecustomsavefile(data, shash):
    file = filedialog.asksaveasfilename(title="Export .dat file", defaultextension=".dat", filetypes=(("Graveyard Keeper File Save", "*.dat"), ("All Files", "*.*")))
    if type(savefiles[shash]) == dict:
        s = shash
    else:
        s = savefiles[shash]
    modifysave(data, s)
    try:
        encoder.encode(file, savefiles[s])
        return {}
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "There was an error while generating the saved file."}


@eel.expose
def savejsonsavefile(data, shash):
    file = filedialog.asksaveasfilename(title="Export .json file", defaultextension=".json", filetypes=(("Graveyard Keeper JSON File Save", "*.json"), ("All Files", "*.*")))
    if type(savefiles[shash]) == dict:
        s = shash
    else:
        s = savefiles[shash]
    modifysave(data, s)
    try:
        with open(file, "w") as f:
            print("Dumping JSON to " + file)
            json.dump(savefiles[s], f)
        return {}
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "There was an error while generating the saved file."}


def modifysave(data, shash):
    mods = ["r", "g", "b", "energy", "inventory_size"]
    for key in mods:
        if data[key]["s"] == -1:
            savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"].append({"v": key, "type": 10})
            savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"].append({"v": key, "type": 5})
            data[key]["s"] = len(savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"])-1
            if key not in savefiles[shash]["serializer"]:
                savefiles[shash]["serializer"].append(key)

        savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][data[key]["s"]] = modifyvaluetype(shash, savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][data[key]["s"]], data[key]["cur"])

    savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_money"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_money"], data["money"])

    savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_hp"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_hp"], data["hp"])
    if data["hp"] >= 100:
        savefiles[shash]["savedata"]["max_hp"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["max_hp"], data["hp"])

    if data["energy"]["cur"] >= 100:
        savefiles[shash]["savedata"]["max_energy"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["max_energy"], data["energy"]["cur"])

    perks = {}
    i = 0
    for _ in data["perks"]:
        perks[data["perks"][i]["v"]] = False
        i +=1

    for i in range(len(savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"])-1, -1, -1):
        if savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"][i-1]["v"] in gamedata["perks"]:
            if savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"][i-1]["v"] not in perks:
                del savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"][i-1]
                del savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][i-1]
            else:
                perks[savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"][i-1]["v"]] = True

    for key in perks:
        if not perks[key]:
            savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"].append({"v": key, "type": 10})
            savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"].append({"v": 1, "type": 19})
            if key not in savefiles[shash]["serializer"]:
                savefiles[shash]["serializer"].append(key)

    difference = len(data["inventory"]) - len(savefiles[shash]["savedata"]["_inventory"]["v"]["15320842"]["v"])

    if difference > 0:
        while difference != 0:
            savefiles[shash]["savedata"]["_inventory"]["v"]["15320842"]["v"].append(deepcopy(savefiles[shash]["savedata"]["_inventory"]["v"]["15320842"]["v"][-1]))
            difference -= 1
    if difference < 0:
        while difference != 0:
            del savefiles[shash]["savedata"]["_inventory"]["v"]["15320842"]["v"][-1]
            difference += 1

    i = 0
    for _ in savefiles[shash]["savedata"]["_inventory"]["v"]["15320842"]["v"]:
        d = savefiles[shash]["savedata"]["_inventory"]["v"]["15320842"]["v"][i]["v"]
        d["id"] = modifyvaluetype(shash, d["id"], data["inventory"][i]["id"])
        d["_params"]["v"]["_durability"] = modifyvaluetype(shash, d["_params"]["v"]["_durability"], data["inventory"][i]["durability"])
        d["value"] = modifyvaluetype(shash, d["value"], data["inventory"][i]["amount"])
        i += 1


# Made for the basic types, not made for Vector2, Vector3, ...
# For those just process the original value (The encoder itself checks if Vector2_00 changed to f.e. Vector2_11
def modifyvaluetype(shash, value, newvalue):
    t = value["type"]
    if type(newvalue) == dict and "v" in newvalue:
        v = newvalue["v"]
    else:
        v = newvalue
    if t == Types.Bool_True or t == Types.Bool_False:
        if v:
            t = Types.Bool_True.value
        else:
            t = Types.Bool_False.value
    elif t == Types.Int32 or t == Types.Int32_0 or t == Types.Int32_1:
        if v == 0:
            t = Types.Int32_0.value
        elif v == 1:
            t = Types.Int32_1.value
        else:
            t = Types.Int32.value
    elif t == Types.Single or t == Types.Single_0 or t==Types.Single_1:
        if v == 0:
            t = Types.Single_0.value
        elif v == 1:
            t = Types.Single_1.value
        else:
            t = Types.Single.value
    elif t == Types.String or t == Types.String_Empty or t == Types.String_Indexed:
        if len(v) == 0:
            t = Types.String_Empty.value
        elif len(v) > 30:
            t = Types.String.value
        else:
            t = Types.String_Indexed.value
            if v not in savefiles[shash]["serializer"]:
                savefiles[shash]["serializer"].append(v)

    if type(newvalue) == dict and "v" in newvalue:
        newvalue["type"] = t
        return newvalue
    elif type(newvalue) != dict:
        value["type"] = t
        value["v"] = newvalue
        return value
    else:
        return newvalue

@eel.expose
def unloadsave(shash):
    shash = str(shash)
    if type(savefiles[shash]) == dict:
        del savefiles[shash]
        print("Unloading Save File")
    else:
        file = savefiles[shash]
        length = 0
        for dat in savefiles:
            if type(savefiles[dat]) == str:
                if savefiles[dat] == file:
                    length += 1
        if length == 1:
            del savefiles[file]
            print("Unloading Save File")
        del savefiles[shash]

def editablevalues(shash):
    data = savefiles[shash]
    obj = dict()
    obj["hash"] = shash
    obj["money"] = data["savedata"]["_inventory"]["v"]["_params"]["v"]["_money"]["v"]
    obj["hp"] = data["savedata"]["_inventory"]["v"]["_params"]["v"]["_hp"]["v"]
    obj["locals"] = id_to_name
    obj["perks"] = []
    # The following 2 are currently just placeholders, but could be added in the future
    obj["technologies1"] = []
    obj["relationships"] = []
    obj["inventory"] = []
    obj["bugs"] = {}
    mod = ["r", "g", "b", "inventory_size", "energy"]

    i = 0
    for k in data["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"]:
        key = k["v"]
        if key in gamedata["perks"]:
            obj["perks"].append({"v": key, "s": i})
        elif key in gamedata["relationships"]:
            obj["relationships"].append({"v": key, "s": i, "cur": data["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][i]["v"]})
        elif key in gamedata["technologies1"]:
            obj["technologies1"].append({"v": key, "s": i})
        elif key in mod:
            obj[key] = {"v": key, "s": i, "cur": data["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][i]["v"]}
        i += 1

    for k in mod:
        if k not in obj:
            obj[k] = {"v": k, "s": -1, "cur": 0}

    i = 0
    for key in data["savedata"]["_inventory"]["v"]["15320842"]["v"]:
        item = {}
        d = data["savedata"]["_inventory"]["v"]["15320842"]["v"][i]["v"]
        item["id"] = d["id"]["v"]
        item["durability"] = d["_params"]["v"]["_durability"]["v"]
        item["amount"] = d["value"]["v"]
        obj["inventory"].append(item)
        i+=1
    return obj


@eel.expose
def siteloaded():
    if newversion != currentversion:
        eel.checkVersion(currentversion, newversion)


web_app_options = {
    'mode': "chrome-app",
    'port': 8005,
    'chromeFlags': ["--window-size=800,1000"]
}


root = Tk()
root.iconbitmap("./data/html/favicon.ico")
root.withdraw()


@eel.expose
def get_folder():
    print("Test")
    options["path"] = filedialog.askdirectory(title="Select the savegame folder of Graveyard Keeper")
    return options["path"]


@eel.expose
def set_settings(path, check):
    options["path"] = path
    options["checkforupdate"] = check
    with open("./data/settings", "w") as f:
        json.dump(options, f)
    return True


if __name__ == "__main__":

    eel.init("./data/html")

    if os.path.isfile("./data/settings"):
        loadsettings()
        eel.start("loadsavefile.html", options=web_app_options)
    else:
        eel.start("no settings.html", options=web_app_options)
