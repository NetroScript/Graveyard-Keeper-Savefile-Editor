#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data.types import id_to_name, gamedata, Types, fallback_item, jsongamedata
from tkinter import Tk
from tkinter import filedialog
from tkinter import PhotoImage
import eel
import os
import sys
import json
from data.hashes import Hashlist
from data.decode import Decoder
from data.encode import Encoder
from copy import deepcopy
from traceback import format_exc
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import psutil


# Set up global variables and the used classes
options = {}
hashes = Hashlist("./data/hashes")
decoder = Decoder(hashes)
encoder = Encoder()
savefiles = {}
saveslots = {}


# Load the version number of this application and already create a newversion variable for a later check for updates
with open("./data/version") as f:
    currentversion = f.read()
    newversion = currentversion


# Load the information about the item version making it possible to fix bugs without having to make a new release (when no code was changed)
with open("./data/itemversion") as f:
    currentiversion = f.read()
    newiversion = currentiversion


# Load the settings of the settings file
def loadsettings():
    with open("./data/settings") as f:
        global options, newversion, newiversion, web_app_options
        options = json.load(f)

        # If the user selected that the application checks for an update load the current version from the GitHub Repo
        if options["checkforupdate"]:
            newversion = urlopen("https://raw.githubusercontent.com/NetroScript/Graveyard-Keeper-Savefile-Editor/master/data/version").read().decode()
            newiversion = urlopen("https://raw.githubusercontent.com/NetroScript/Graveyard-Keeper-Savefile-Editor/master/data/itemversion").read().decode()
        # If the user never set a manual port (in case he starts it after the update where ports were implemented)
        # choose 0 as default port
        if "port" not in options:
            options["port"] = 0
        if "backupamount" not in options:
            options["backupamount"] = 3
        web_app_options["port"] = options["port"]


# Allow the web interface to call this function so that commonly changed files can be changed without needing releases
# Now releases are only necessary when code is changed and at the same time users don't have a disadvantage
@eel.expose
def updateitemversion():
    response = urlopen("https://github.com/NetroScript/Graveyard-Keeper-Savefile-Editor/archive/master.zip")
    # Load the downloaded in memory file as a zip file
    zipfile = ZipFile(BytesIO(response.read()))
    print("Deleting Old Frontend (html folder)")
    shutil.rmtree('./data/html', ignore_errors=True)
    os.mkdir("./data/html")
    print("Copying new frontend files")
    # We iterate all files in the zip to be able to extract 1 whole specific folder
    for zip_info in zipfile.infolist():
        # We only want the rsc folder
        if zip_info.filename.startswith("Graveyard-Keeper-Savefile-Editor-master/data/html/"):
            # To prevent an error when there is no base name
            if zip_info.filename[-1] == '/':
                continue
            # So we don't extract the whole folder structure we change the path in the zip info object
            zip_info.filename = zip_info.filename.split("/data/html/")[1]
            zipfile.extract(zip_info, "./data/html/")

    # Same as above but for individual files
    print("Deleting old locals.json")
    os.remove("./data/locals.json")
    print("Copying new locals.json")
    info = zipfile.getinfo("Graveyard-Keeper-Savefile-Editor-master/data/locals.json")
    info.filename = os.path.basename(info.filename)
    zipfile.extract(info, "./data/")
    print("Deleting old itemversion")
    os.remove("./data/itemversion")
    print("Copying new itemversion")
    info = zipfile.getinfo("Graveyard-Keeper-Savefile-Editor-master/data/itemversion")
    info.filename = os.path.basename(info.filename)
    zipfile.extract(info, "./data/")

    print("Finished updating - now closing")

    # Using just exit() doesn't close the browser (GUI) window
    # The JavaScript window.close() doesn't work on newer Chrome versions, if so a splash screen is shown
    eel.closeWindow()()

    # Because this process spawns the browser windows they should be sub processes
    # Then it closes those (in case the window.close() didn't work)
    app = psutil.Process(os.getpid())
    for GUI in app.children(recursive=True):
        GUI.kill()
    exit()


# Allow the web interface to load information about all save files in the folder the user set as save directory
@eel.expose
def getsavefiles():
    i = 1
    out = []
    print("Looking for save files in the folder: " + options["path"])
    for file in os.listdir(options["path"]):
        # .info contains the information about the save, although it's content doesn't matter considering the save file
        if file.endswith(".info"):
            with open(os.path.join(options["path"], file)) as f:
                data = json.load(f)

                # The save file has an id which is from the file name, but also an iterator which is displayed in the
                # application as the number of the save file, this number also represents the position in the array of
                # save file info
                out.append({
                    "version": round(data["version"], 3),
                    "savetime": data["real_time"],
                    "days": int(data["game_time"]-1.5),
                    "church": data["stats"].split("ss)")[1].strip(),
                    "graveyard": data["stats"].split("ll)")[1].split("(cr")[0].strip(),
                    "id": file.split(".info")[0],
                    "num": i
                })
                saveslots[i] = file.split(".info")[0]
                i += 1

    return out


# Allow web ui to load a specific slot
@eel.expose
def getsavefile(slot, shash):
    # We try to load and unload the files from memory using an object so that memory is saved
    if shash not in savefiles:
        try:
            # try to load the save file into memory if it doesn't exist
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


# Allow web ui to search for a .dat save file
@eel.expose
def getcustomsavefile(shash):

    # tkinter file dialog
    tkinter_gain_focus()
    file = filedialog.askopenfilename(title="Select a savegame which is not created by Graveyard Keeper", defaultextension=".dat", filetypes=(("Graveyard Keeper File Save", "*.dat"), ("All Files", "*.*")))
    root.withdraw()
    # Check if the path is already loaded into memory
    if file in savefiles:
        savefiles[shash] = file
        return editablevalues(file)
    # if not decode the given save file and print an error if the decoder can't load it
    try:
        data = decoder.decode(file)
        savefiles[shash] = file
        savefiles[file] = data
        return editablevalues(file)
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "The chosen .dat file doesn't seem to be a save file or the save file editor is out of date :c"}


# Allow web ui to search for a .json save file
@eel.expose
def getjsonsavefile(shash):

    # tkinter file dialog
    tkinter_gain_focus()
    file = filedialog.askopenfilename(title="Select a savegame which is exported by this application", defaultextension=".json", filetypes=(("Graveyard Keeper JSON File Save", "*.json"), ("All Files", "*.*")))
    root.withdraw()
    # Check if the path is already loaded into memory
    if file in savefiles:
        savefiles[shash] = file
        return editablevalues(file)
    try:
        # load JSON
        with open(file) as f:
            data = json.load(f)
        # a basic check to see if the correct properties are in the top level of the JSON object
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


# If the user loaded a save file from a slot, save again to the slot
@eel.expose
def saveslot(data, shash, slot):

    # apply the data to the save file
    modifysave(data, shash)
    curpath = os.path.join(options["path"], str(saveslots[int(slot)])+".dat")

    makebackups = options["backupamount"]

    # Create the set amount of backups
    while makebackups > 0:

        # Get the file to be renamed
        currentone = curpath+".back_"+str(makebackups-1)+".zip" if makebackups > 1 else curpath
        try:
            # If this file to be renamed exists, rename it to the next bigger number (or replace)
            # and always rename the default save
            if os.path.isfile(currentone) or makebackups == 1:
                p = curpath+".back_"+str(makebackups) + (".zip" if makebackups > 1 else "")
                os.replace(currentone, p)

                # Only if it is the first save file, it is not zipped yet, otherwise it already will be zipped
                # But this causes the name within the zip to always be _1, but I think that shouldn't matter too much
                if makebackups == 1:
                    # Zip the file to save disk space
                    zip = ZipFile(p+".zip", "w", ZIP_DEFLATED)
                    zip.write(p, arcname=os.path.basename(p))
                    zip.close()
                    os.remove(p)

        except Exception:
            print("Error:")
            print(format_exc())
            return {"Error": "There was an error while creating the backup file."}

        makebackups -= 1

    # try saving the save file
    try:
        encoder.encode(curpath, savefiles[shash])
        return {}
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "There was an error while generating the saved file."}


# Export the save file to a .dat file
@eel.expose
def savecustomsavefile(data, shash):

    # tkinter file dialogue
    tkinter_gain_focus()
    file = filedialog.asksaveasfilename(title="Export .dat file", defaultextension=".dat", filetypes=(("Graveyard Keeper File Save", "*.dat"), ("All Files", "*.*")))
    root.withdraw()

    # Load the save object, we have to check if it is directly saved in the savefiles object or if it is linked to a
    # save hash
    if type(savefiles[shash]) == dict:
        s = shash
    else:
        s = savefiles[shash]

    # apply the data to the save file
    modifysave(data, s)

    # try saving the save file
    try:
        encoder.encode(file, savefiles[s])
        return {}
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "There was an error while generating the saved file."}


# Export the save file to a .json file
@eel.expose
def savejsonsavefile(data, shash):

    # tkinter file dialogue
    tkinter_gain_focus()
    file = filedialog.asksaveasfilename(title="Export .json file", defaultextension=".json", filetypes=(("Graveyard Keeper JSON File Save", "*.json"), ("Graveyard Keeper HTML File Save for easy loading in JavaScript", "*.html"), ("All Files", "*.*")))
    root.withdraw()

    # Load the save object, we have to check if it is directly saved in the savefiles object or if it is linked to a
    # save hash
    if type(savefiles[shash]) == dict:
        s = shash
    else:
        s = savefiles[shash]

    # apply the data to the save file
    modifysave(data, s)

    # try saving the save file - simply dumping the data we have as JSON
    try:
        with open(file, "w") as f:

            # For more compatibility we replace pythons NaN with null because NaN is not valid JSON
            jsonstring = json.dumps(savefiles[s]).replace(" NaN", " null")

            # If we want to dump it as html file we do so here
            if file.endswith(".html"):

                placeholder = ""

                with open('./data/html/dumpskeleton.html', 'r') as placeholderfile:
                    placeholder = placeholderfile.read()

                print("Creating HTML file at " + file)
                # Replace \" with \\" so JS doesn't just remove the \
                f.write(placeholder.replace("[[[[PLACEHOLDER]]]]", jsonstring.replace('\\"', '\\\\"')))

            # By default dump it as only json
            else:
                print("Dumping JSON to " + file)
                f.write(jsonstring)
        return {}
    except Exception:
        print("Error:")
        print(format_exc())
        return {"Error": "There was an error while generating the saved file."}


# Apply the changed data to our save we have in memory
def modifysave(data, shash):

    # Simple values we can iterate in the inventory object of the save
    mods = ["r", "g", "b", "energy", "inventory_size"]
    for key in mods:
        # it can happen that the user never had f.e. blue tech points, in this case generate the needed data
        # the s property is the original position in the array, -1 is set if there was none
        if data[key]["s"] == -1:
            savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"].append({"v": key, "type": 10})
            savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"].append({"v": key, "type": 5})
            data[key]["s"] = len(savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"])-1
            # if the string of the object doesn't exist yet in the string array, we add it to the array
            if key not in savefiles[shash]["serializer"]:
                savefiles[shash]["serializer"].append(key)

        # apply the new value to the original object, we use modifyvaluetype which has some additional checks
        savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][data[key]["s"]] = modifyvaluetype(shash, savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][data[key]["s"]], data[key]["cur"])

    # apply the new money value to the original object, we use modifyvaluetype which has some additional checks
    savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_money"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_money"], data["money"])

    # apply the new HP value to the original object, we use modifyvaluetype which has some additional checks
    savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_hp"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_hp"], data["hp"])

    # if the value of the HP is over 100 (or equal to 100 to reset it) we increase the maximal possible HP to the set
    # value
    if data["hp"] >= 100:
        savefiles[shash]["savedata"]["max_hp"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["max_hp"], data["hp"])

    # if the value of the energy is over 100 (or equal to 100 to reset it) we increase the maximal possible energy to
    # the set value
    if data["energy"]["cur"] >= 100:
        savefiles[shash]["savedata"]["max_energy"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["max_energy"], data["energy"]["cur"])

    # Change the day / time value
    savefiles[shash]["savedata"]["day"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["day"], data["time"]["day"])
    savefiles[shash]["savedata"]["_serialized_time_of_day"]["v"]["time_of_day"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["_serialized_time_of_day"]["v"]["time_of_day"], data["time"]["timeofday"])

    # for every relationship set the value of the "friendliness" with the NPC
    for rel in data["relationships"]:
        savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][rel["s"]] = modifyvaluetype(shash, savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][rel["s"]], rel["cur"])

    # Check the difference in size of the old inventory and the modified inventory
    difference = len(data["inventory"]) - len(savefiles[shash]["savedata"]["_inventory"]["v"]["inventory"]["v"])

    # if more items were added in the editor we copy the last item in the inventory until the amount of items in the
    # old inventory and in the new is the same
    # In the case of an empty inventory we load a fallback item which was copied before as a random item in the
    # inventory
    if difference > 0:
        while difference != 0:
            if len(savefiles[shash]["savedata"]["_inventory"]["v"]["inventory"]["v"]) > 0:
                savefiles[shash]["savedata"]["_inventory"]["v"]["inventory"]["v"].append(deepcopy(savefiles[shash]["savedata"]["_inventory"]["v"]["inventory"]["v"][-1]))
            else:
                savefiles[shash]["savedata"]["_inventory"]["v"]["inventory"]["v"].append(deepcopy(fallback_item))
            difference -= 1
    # If the new inventory has less items, we just delete the last n items
    if difference < 0:
        while difference != 0:
            del savefiles[shash]["savedata"]["_inventory"]["v"]["inventory"]["v"][-1]
            difference += 1

    # Here the items in the inventory are modified, we set the new ID, durability (to "repair" an item) and the amount
    # of the item for each item in our Array
    i = 0
    for _ in savefiles[shash]["savedata"]["_inventory"]["v"]["inventory"]["v"]:
        d = savefiles[shash]["savedata"]["_inventory"]["v"]["inventory"]["v"][i]["v"]
        d["id"] = modifyvaluetype(shash, d["id"], data["inventory"][i]["id"])
        d["_params"]["v"]["_durability"] = modifyvaluetype(shash, d["_params"]["v"]["_durability"], data["inventory"][i]["durability"])
        d["value"] = modifyvaluetype(shash, d["value"], data["inventory"][i]["amount"])
        i += 1

    # Here we check if the save is from an older version which doesn't have this variable yet
    # If there is a second inventory (for tools) we update it
    if "secondary_inventory" in savefiles[shash]["savedata"]["_inventory"]["v"]:

        # Check the difference in size of the old inventory and the modified inventory
        difference = len(data["subinventory"]) - len(savefiles[shash]["savedata"]["_inventory"]["v"]["secondary_inventory"]["v"])

        # if more items were added in the editor we ignore it because we don't allow adding to the secondary inventory
        # If the new inventory has less items, we just delete the last n items
        if difference < 0:
            while difference != 0:
                del savefiles[shash]["savedata"]["_inventory"]["v"]["secondary_inventory"]["v"][-1]
                difference += 1

        # Here the items in the inventory are modified, we set the new ID, durability (to "repair" an item) and the amount
        # of the item for each item in our Array
        i = 0
        for _ in savefiles[shash]["savedata"]["_inventory"]["v"]["secondary_inventory"]["v"]:
            d = savefiles[shash]["savedata"]["_inventory"]["v"]["secondary_inventory"]["v"][i]["v"]
            d["id"] = modifyvaluetype(shash, d["id"], data["subinventory"][i]["id"])
            d["_params"]["v"]["_durability"] = modifyvaluetype(shash, d["_params"]["v"]["_durability"], data["subinventory"][i]["durability"])
            i += 1

    # If the user wants to complete the techtree, we replace all objects related to it with our previously extracted objects
    if data["switches"]["techtree"]:

        # Iterate the lists which we change for quicker access
        lists = ["unlocked_works", "unlocked_techs", "unlocked_perks", "unlocked_crafts", "revealed_techs"]
        for l in lists:
            savefiles[shash]["savedata"][l] = jsongamedata[l]

            # Many of those technologies are indexed strings, meaning we have to add the ones which aren't included yet
            # into the serializer
            for string in savefiles[shash]["savedata"][l]["v"]:
                if string["type"] == Types.String_Indexed.value:

                    if string["v"] not in savefiles[shash]["serializer"]:
                        savefiles[shash]["serializer"].append(string["v"])

        currentinlist = list(map(lambda x: x["v"],savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"]))

        for entry in jsongamedata["attributelist"]:
            if entry in currentinlist:
                savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][currentinlist.index(entry)] = {"type": 19, "v": 1}
            else:
                savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"].append({"type": 10, "v": entry})
                savefiles[shash]["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"].append({"type": 19, "v": 1})


    # In the following block World Game Objects are iterated
    # For us specifically interesting are all storage units + workers and bodies to modify the items in them
    i2 = 0  # Index of the storage unit in our storage unit array
    i = 0  # Index of the WGO

    # Indexes of WGO's we want to remove,  we can't do that during iteration, so we do it after iteration
    delete_indexes = []

    for _ in savefiles[shash]["savedata"]["map"]["v"]["_wgos"]["v"]:

        convertemptygrave = False

        # To have shorter variable names
        it = savefiles[shash]["savedata"]["map"]["v"]["_wgos"]["v"][i]["v"]

        # Check if the object id is the id of a storage unit, if so modify the values
        if it["obj_id"]["v"] in gamedata["storage"]:

            # Like in the player inventory we have to create / remove items depending on the amount of items in the
            # inventory
            difference = len(data["additionalstorage"][i2]["items"]) - len(it["-1126421579"]["v"]["inventory"]["v"])

            # if more items were added in the editor we copy the last item in the inventory until the amount of items
            # in the old inventory and in the new is the same
            # In the case of an empty inventory we load a fallback item which was copied before as a random item in the
            # inventory
            if difference > 0:
                while difference != 0:
                    if len(it["-1126421579"]["v"]["inventory"]["v"]) > 0:
                        it["-1126421579"]["v"]["inventory"]["v"].append(deepcopy(it["-1126421579"]["v"]["inventory"]["v"][-1]))
                    else:
                        it["-1126421579"]["v"]["inventory"]["v"].append(deepcopy(fallback_item))
                    difference -= 1

            # If the new inventory has less items, we just delete the last n items
            if difference < 0:
                while difference != 0:
                    del it["-1126421579"]["v"]["inventory"]["v"][-1]
                    difference += 1

            # Set the inventory size to the new value - the modification of this was removed in the ui because it seems
            # that most if not all storage units have a fixed size which can not be changed in the save file
            it["-1126421579"]["v"]["_params"]["v"]["_res_v"]["v"][0] = modifyvaluetype(shash, it["-1126421579"]["v"]["_params"]["v"]["_res_v"]["v"][0], data["additionalstorage"][i2]["size"])

            # Iterate and modify the items in the specific storage unit
            i3 = 0  # Item index in Storage unit
            for _ in it["-1126421579"]["v"]["inventory"]["v"]:
                d = it["-1126421579"]["v"]["inventory"]["v"][i3]["v"]
                d["id"] = modifyvaluetype(shash, d["id"], data["additionalstorage"][i2]["items"][i3]["id"])
                d["_params"]["v"]["_durability"] = modifyvaluetype(shash, d["_params"]["v"]["_durability"], data["additionalstorage"][i2]["items"][i3]["durability"])
                d["value"] = modifyvaluetype(shash, d["value"], data["additionalstorage"][i2]["items"][i3]["amount"])
                i3 += 1
            i2 += 1

        # If workers should be turned into perfect workers we replace their inventory (which is used to calculate the
        # efficiency with a perfect inventory
        if data["switches"]["workers"] and it["obj_id"]["v"] == "worker_zombie_1":
            # We keep the last item of the old inventory, because that is the used backpack which still might contain
            # items
            it["-1126421579"]["v"]["inventory"]["v"] = jsongamedata["inventory"]+[it["-1126421579"]["v"]["inventory"]["v"][-1]]

        # If the donkey should be replaced with a working one we just replace it but store and restore the unique id the
        # donkey had
        if data["switches"]["donkey"] and it["obj_id"]["v"] == "donkey":
            previousuniqueid = it["unique_id"]["v"]
            savefiles[shash]["savedata"]["map"]["v"]["_wgos"]["v"][i] = jsongamedata["working_donkey"]
            savefiles[shash]["savedata"]["map"]["v"]["_wgos"]["v"][i]["v"]["unique_id"]["v"] = previousuniqueid

        # If empty graves should be turned into perfect graves we first change the id to a normal grave and then
        # use the code for perfect body and perfect decoration to also transform this grave into a perfect grave
        if data["switches"]["emptygrave"] and it["obj_id"]["v"] == "grave_empty_place":
            convertemptygrave = True
            it["obj_id"]["v"] = "grave_ground"
            it["-1126421579"]["v"]["id"]["v"] = "grave_ground"

        # If bodies in graves should be turned into perfect bodies we replace their inventory
        if (data["switches"]["gravebodies"] or convertemptygrave) and it["obj_id"]["v"] == "grave_ground":

            # If the grave is empty we add a body to it
            if len(it["-1126421579"]["v"]["inventory"]["v"]) == 0:
                it["-1126421579"]["v"]["inventory"]["v"].append({"type": 250, "v": jsongamedata["body"]})

            # We iterate the items until we found the body and then change the inventory of the body
            for item in it["-1126421579"]["v"]["inventory"]["v"]:
                if item["v"]["id"]["v"] == "body":
                    item["v"]["inventory"]["v"] = jsongamedata["inventory"]
                    item["v"]["_params"]["v"]["_durability"]["v"] = 1
                    break

        # If the graves should get perfect decorations we replace the current ones
        if (data["switches"]["decorations"] or convertemptygrave) and it["obj_id"]["v"] == "grave_ground":

            # We iterate the items to delete all but the body so we can add the new ones
            it["-1126421579"]["v"]["inventory"]["v"][:] = [x for x in it["-1126421579"]["v"]["inventory"]["v"]
                                                           if x["v"]["id"]["v"] == "body"]
            it["-1126421579"]["v"]["inventory"]["v"].append(jsongamedata["fence"])
            it["-1126421579"]["v"]["inventory"]["v"].append(jsongamedata["decoration"])
            it["-1126421579"]["v"]["_params"]["v"]["_res_type"] = jsongamedata["_res_type"]
            it["-1126421579"]["v"]["_params"]["v"]["_res_v"] = jsongamedata["_res_v"]

        # If NPC got stuck in the church, we can just remove their entity entirely from the save
        if data["switches"]["removechurchvisitors"] and it["obj_id"]["v"] == "npc_church_visitor":
            delete_indexes.append(i)

        i += 1

    offset = 0
    for delete in delete_indexes:
        # Delete the queued WGO
        del savefiles[shash]["savedata"]["map"]["v"]["_wgos"]["v"][delete-offset]

        # We deleted one in front, so we need to decrease the index which is  because an element is missing
        offset += 1

    # Clear the drop data when requested
    if len(data["drops"]) < len(savefiles[shash]["savedata"]["drops"]["v"]):

        # First go through the drops to see if we need to adjust the morgue body count (because we remove bodies)
        reduce = 0.0
        for drop in savefiles[shash]["savedata"]["drops"]["v"]:
            if drop["v"]["res"]["v"]["id"]["v"] == "body":
                reduce+=1

        # If the morgue counter needs to be reduced do so
        if reduce > 0:
            # Get the previous value
            change_value = get_parameter_value(savefiles[shash]["savedata"]["_inventory"] ,"cur_bodies_count")

            # Only save changes when there was a value before
            if change_value != None:
                change_value["v"] = max(0 , change_value["v"]-reduce)
                # Set the new value
                set_parameter_value(shash, savefiles[shash]["savedata"]["_inventory"] ,"cur_bodies_count", change_value)

        savefiles[shash]["savedata"]["drops"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["drops"], [])
        # Check first if they exist
        if "1968591194" in savefiles[shash]["savedata"]["map"]["v"]:
            savefiles[shash]["savedata"]["map"]["v"]["1968591194"] = modifyvaluetype(shash, savefiles[shash]["savedata"]["map"]["v"]["1968591194"], [])

    if data["switches"]["resetmorgue"]:
        set_parameter_value(shash, savefiles[shash]["savedata"]["_inventory"] ,"cur_bodies_count", {"v": 0.0, "type": 5})


# Made for the basic types, not made for Vector2, Vector3, ...
# For those just process the original value (The encoder itself checks if Vector2_00 changed to f.e. Vector2_11
def modifyvaluetype(shash, value, newvalue):
    t = value["type"]

    # Extract the new value depending on the supplied type (simple value or a dictionary containing the value) to v
    if type(newvalue) == dict and "v" in newvalue:
        v = newvalue["v"]
    else:
        v = newvalue

    # Depending on the type change the type to the correct type. F.e. if the value was 0.0 before and now is 23.8 the
    # type changes from 0 value Float to normal Float
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
            # If the string was changed and is not in the string array we add to it
            if v not in savefiles[shash]["serializer"]:
                savefiles[shash]["serializer"].append(v)

    # return the new value in the same way it was supplied (either a simple value or a dict)
    if type(newvalue) == dict and "v" in newvalue:
        newvalue["type"] = t
        return newvalue
    elif type(newvalue) != dict:
        value["type"] = t
        value["v"] = newvalue
        return value
    else:
        return newvalue


# When closing the window of a specific save slot editor, unload this save file
@eel.expose
def unloadsave(shash):
    shash = str(shash)
    if type(savefiles[shash]) == dict:
        del savefiles[shash]
        print("Unloading Save File")
    # In the case of it not having a specific shash for the file (meaning if it was loaded from a custom .dat or .json)
    # we first check if the file is also referenced in a different window
    else:
        file = savefiles[shash]
        length = 0
        for dat in savefiles:
            if type(savefiles[dat]) == str:
                if savefiles[dat] == file:
                    length += 1
        # If there is only 1 instance of the save file, delete it
        if length == 1:
            del savefiles[file]
            print("Unloading Save File")
        # Just remove the "link" to the actual save file
        del savefiles[shash]


# Extract the values we can edit from the save file
def editablevalues(shash):
    # Load the data from our shash
    data = savefiles[shash]
    obj = dict()
    obj["hash"] = shash

    # Extract the simple values from the save
    obj["money"] = data["savedata"]["_inventory"]["v"]["_params"]["v"]["_money"]["v"]
    obj["hp"] = data["savedata"]["_inventory"]["v"]["_params"]["v"]["_hp"]["v"]
    obj["time"] = {
        "day": data["savedata"]["day"]["v"],
        "timeofday": data["savedata"]["_serialized_time_of_day"]["v"]["time_of_day"]["v"]
    }


    # Additionally add the localisation info to the save file, so the ui can easily access it
    obj["locals"] = id_to_name
    obj["perks"] = []
    # The following is currently just a placeholder, but could be added in the future
    obj["technologies1"] = []
    obj["relationships"] = []
    obj["inventory"] = []
    obj["bugs"] = {}
    obj["additionalstorage"] = []
    obj["subinventory"] = []


    # The values which are in the player inventory and can be iterated for easier extraction
    mod = ["r", "g", "b", "inventory_size", "energy"]

    i = 0
    for k in data["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_type"]["v"]:
        key = k["v"]
        # If the value is in our list of perks, we append the perk to our editable perks
        if key in gamedata["perks"]:
            obj["perks"].append({"v": key, "s": i})
        # If the value is for a relationship with a NPC we append it to our relationships list
        elif key.startswith("_rel_npc_"):
            obj["relationships"].append({"v": key, "s": i, "cur": data["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][i]["v"]})
        # If the value is in our list of exisiting technologies we append it to our technologieslist
        elif key in gamedata["technologies1"]:
            obj["technologies1"].append({"v": key, "s": i})
        # If the value is one of the mod values we simply change the top level property to the value of the save file
        elif key in mod and key not in obj:
            obj[key] = {"v": key, "s": i, "cur": data["savedata"]["_inventory"]["v"]["_params"]["v"]["_res_v"]["v"][i]["v"]}
        i += 1

    # If our mod value was not in our save, we create a placeholder with a s value -1 to indicate it had no position in
    # the save and didn't exist
    for k in mod:
        if k not in obj:
            obj[k] = {"v": k, "s": -1, "cur": 0}

    i = 0
    # in the world game object with the id "storage_builddesk" your fame is stored - do we want to add an option to modify it?

    # We iterate all World Game Objects
    for _ in data["savedata"]["map"]["v"]["_wgos"]["v"]:

        # shorten the variable name
        it = data["savedata"]["map"]["v"]["_wgos"]["v"][i]["v"]

        # If we have the id saved as storage unit we extract the inventory of the storage to be able to edit it
        if it["obj_id"]["v"] in gamedata["storage"]:
            inv = dict()
            inv["type"] = it["obj_id"]["v"]
            inv["items"] = getinventory(it["-1126421579"]["v"]["inventory"]["v"])
            inv["size"] = it["-1126421579"]["v"]["_params"]["v"]["_res_v"]["v"][0]["v"]
            obj["additionalstorage"].append(inv)
        i += 1

    # We load the items in the inventory of the player
    obj["inventory"] = getinventory(data["savedata"]["_inventory"]["v"]["inventory"]["v"])
    # Since the update were you can put tools in the tool slot, we have an additional secondary inventory
    # We also add a check if the object even exists so that we don't cause errors in older save files / game versions
    if "secondary_inventory" in data["savedata"]["_inventory"]["v"]:
        obj["subinventory"] = getinventory(data["savedata"]["_inventory"]["v"]["secondary_inventory"]["v"])

    obj["drops"] = list()
    # To display the objects which will get deleted when you clear the drops we extract them
    for drop in data["savedata"]["drops"]["v"]:
        obj["drops"].append(drop["v"]["res"]["v"]["id"]["v"])

    # Check first if the entry actually exists
    if "1968591194" in data["savedata"]["map"]["v"]:
        for drop in data["savedata"]["map"]["v"]["1968591194"]["v"]:
            types = ["Red points", "Blue points", "Green points"]
            obj["drops"].append(types[drop["v"]["type"]["v"]["1826761547"]["v"]])

    # Variables to determine if all bodies in the graves / all workers get turned into perfect bodies / workers
    obj["switches"] = {
        "workers": False,
        "gravebodies": False,
        "decorations": False,
        "emptygrave": False,
        "techtree": False,
        "donkey": False,
        "resetmorgue": False,
        "removechurchvisitors": False
    }

    return obj


# Function to simplify loading the items in an inventory of a game object
def getinventory(inv):
    i = 0
    out = []
    # For every item we extract the id, amount and durability (to be able to repair it)
    for _ in inv:
        item = dict()
        item["id"] = inv[i]["v"]["id"]["v"]
        item["durability"] = inv[i]["v"]["_params"]["v"]["_durability"]["v"]
        item["amount"] = inv[i]["v"]["value"]["v"]
        out.append(item)
        i += 1
    return out


# Function to return a parameter from an inventory, exists to simplify it
def get_parameter_value(inventory, parameter):
    params = inventory["v"]["_params"]["v"]

    # The position of our value
    index = -1
    i = 0
    # Get it in the list
    for type in params["_res_type"]["v"]:
        
        # Break when found
        if type["v"] == parameter:
            index = i
            break

        i+=1

    # Return empty value if non existant
    if index == -1:
        return None
    
    # Otherwise return result
    return params["_res_v"]["v"][index]


# Set a specific parameter of an inventory
def set_parameter_value(shash, inventory, parameter, value):
    
    params = inventory["v"]["_params"]["v"]

    # The position of our value
    index = -1
    i = 0
    # Get it in the list
    for type in params["_res_type"]["v"]:
        
        # Break when found
        if type["v"] == parameter:
            index = i
            break

        i+=1

    # The value doesn't exist, so we add it to the list
    if index == -1:
        params["_res_type"]["v"].append(modifyvaluetype(shash, {"v": "Old Parameter Name", "type":10}, parameter))
        params["_res_v"]["v"].append(value)
    # Otherwise set the value
    else:
        params["_res_v"]["v"][index] = modifyvaluetype(shash, params["_res_v"]["v"][index], value)


# Call on page load of the main page (with the save slots)
@eel.expose
def siteloaded():

    # If there is an update we call the JavaScript Function to display information about the new update
    if newversion != currentversion:
        eel.checkVersion(currentversion, newversion)

    elif newiversion != currentiversion:
        eel.checkiVersion(currentiversion, newiversion)


# Make it possible for the ui to open a folder select dialogue for the save files
@eel.expose
def get_folder(initial=""):
    if initial == "":
        initial = None
    tkinter_gain_focus()
    folder = filedialog.askdirectory(title="Select the savegame folder of Graveyard Keeper", initialdir=initial)
    root.withdraw()
    return folder


# Try to automatically populate the default folder, at least for known systems
@eel.expose
def get_default_path():
    if sys.platform in ['win32', 'win64']:
        return os.path.expandvars("C:\\Users\\%username%\\AppData\\LocalLow\\Lazy Bear Games\\Graveyard Keeper")
    elif sys.platform.startswith('linux'):
        return os.path.expanduser('~/.config/unity3d/Lazy Bear Games/Graveyard Keeper/')
    elif sys.platform == 'darwin':
        return os.path.expandvars("/Users/$USER/Library/Application Support/unity.LazyBearGames.GraveyardKeeper/")
    return ""

# Function exposed to the ui to save changed settings
@eel.expose
def set_settings(settings):
    global options
    options = settings
    
    if "path" in options:
        options["path"] = os.path.expandvars(options["path"])
    
    with open("./data/settings", "w") as f:
        json.dump(settings, f)
    return True


# Function exposed to the ui to get the current settings
@eel.expose
def get_settings():
    return options


# Configuration for the Chrome instance, we use a fixed size and port 0 on first initialisation so that there
# is no conflicting port
web_app_options = {
    'mode': "chrome-app",
    'port': 0,
    'chromeFlags': ["--window-size=800,1000"]
}


# We use a tkinter instance for the file dialogues and also set our icon
root = Tk()

# For some linux version which can't load it correctly
try:
    root.iconbitmap("./data/html/favicon.ico")
except Exception:
    try:
        root.iconphoto(True, PhotoImage(file="./data/html/favicon.png"))
    except Exception:
        print("Unable to set icon, just skipping it")
# Hide the tkinter instance
root.withdraw()
root.overrideredirect(True)
root.geometry('0x0+0+0')


# Allow file dialogs to gain focus
def tkinter_gain_focus():
    root.deiconify()
    root.lift()
    root.focus_force() 

def run():
    global web_app_options

    # Check if the application is run the first time - if so show the settings dialogue, if not start the normal
    # application
    if os.path.isfile("./data/settings"):
        loadsettings()
        eel.start("loadsavefile.html", options=web_app_options)
    else:
        eel.start("no settings.html", options=web_app_options)


# A try except statement, so that the console window doesn't close on error so that it is easier for users to report
# errors
try:

    if __name__ == "__main__":

        # Our folder with the HTML data
        eel.init("./data/html")

        # First try running it normally using chrome
        try:
            run()
        # if it doesn't work (f.e. chrome not installed) run using the default browser
        except Exception:
            web_app_options["mode"] = ""
            run()


except Exception as e:
    print("Following exception occured: ")
    print(format_exc())
    # Pause on exception before closing
    input("Press Enter to close the application")
    exit()
