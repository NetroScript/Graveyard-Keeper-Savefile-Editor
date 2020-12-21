Graveyard-Keeper-Savefile-Editor
================================
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a save editor for [Graveyard Keeper](https://store.steampowered.com/app/599140/Graveyard_Keeper/).

The python version works on Windows, Linux and macOS.
For Windows a .exe version available too.

It can load and save *.dat files.
Additionally you can export the loaded save to JSON, which has a similar structure to the original .json save files.
(The difference is, that information about types of variables is saved in the file, meaning every value is wrapped in an object).
When exporting to JSON you can also choose .html to have a website where you can relatively easily edit the save in the browser console and then export it again.

**The Application uses a webbrowser as a GUI** (by default Chrome in App Mode, but during development FireFox was tried too - f.e. Opera should work too, but watch out for your Opera version - see [Issue #54](https://github.com/NetroScript/Graveyard-Keeper-Savefile-Editor/issues/54)).

I want to add I am not responsible if you break your save file, I try to mantain this editor in a way, in which it can't break save files (or not by mistake) but it is still possible that this editor produces a bugged save file (if you for example add an item in a quality in which the item doesn't exist. - although in non expert mode the editor will prevent saving your file when a non existant item is selected).

That is why you always should **backup your save files**. (In the settings of the editor you can also set the number of backups the editor should create (which are zipped) - on saving the editor all backups are shifted by one, so if set it to 3 backups and save 4 times, your oldest backup is lost).

But I want to mention the last time someone asked for help due to a save broken by the save editor was in september 2018 and since then I also took additional measures.

**This Editor supports the DLCs (Stranger Sins + Game Of Crone) - in the editor you have toggles to enable or disable DLC Support**

## Currently Editable

* Money
* Red, green, blue technology points
* HP
* Energy
* Current Time
* Your inventory size
* Your inventory items
* Inventories of all (or at least most) storage units
* Your relationships with NPC's (only if you interacted with them before and have more than 0)
* Additionally utilities like:
  * Removing all drops
  * Setting the worker efficiency 40%
  * Turning the graves into perfect graves
  * Complete the entire tech tree (state is pre DLC)
  * Fix if the donkey is stuck
  * Reset the morgue body counter should it be broken
  * Remove stuck church goes
  * Reset your dungeon

## Screenshot

![Preview](https://i.imgur.com/XZdmo3Z.png)

## Installation

* Download this as zip and extract it to the folder where you want it to be
* Get Python (>=3.4)
* If you are using a macOS/Linux system where `python` is by default python 2.x, replace `python` with `python3`. Also instead of creating a .bat file, create a .sh file. Additionally according to users you might also need to install `python-tk` if it is not yet included in your distribution.
* Install dependencies using `python -m pip install -r requirements.txt`.
* Execute the file with `python main.py` (in the console with the folder where main.py resides as working directory - to simplify this just create a `run.bat` in the directory with the same content)
* Enjoy

**OR**

Download a [frozen release](https://github.com/NetroScript/Graveyard-Keeper-Savefile-Editor/releases) for windows (so you don't need to install python).

## Save File Locations

Linux / Ubuntu:

* `/home/$USER/.config/unity3d/Lazy Bear Games/Graveyard Keeper/`

MacOS:

* `/Users/$USER/Library/Application Support/unity.LazyBearGames.GraveyardKeeper/`

Windows:

* `C:\Users\%username%\AppData\LocalLow\Lazy Bear Games\Graveyard Keeper`


**Warning**: 
The application supports variables in the path starting with 0.1.17. If you use an earlier version manually fill in your user name for the variables. 

## Usage

Considering the application has a GUI it should be self explanatory.
If a red border appears around an item, it means the save editor doesn't have this item indexed. Either because the item doesn't exist, or it was added in an update which wasn't included yet in the editor.
Same if an item doesn't have a preview image.

If you want to manually edit save files, when you change values, watch out if you change the type of the variable. F.e. if you would change a value from 0 to 1, the type would change and you would need to manually change the type to the correct one.
For information about the possible types, check types.py in the data folder.


## Changelog

Check it [here](https://github.com/NetroScript/Graveyard-Keeper-Savefile-Editor/blob/master/changelog.md).


## Thanks to

* Reddit user [aMannus](https://www.reddit.com/user/aMannus) for supplying me a save to implement worker efficiency
* All contributers to this repository

## Misc

If you want to know about some stuff which you could do if you export the savefile to json check this file [here](https://github.com/NetroScript/Graveyard-Keeper-Savefile-Editor/blob/master/saves.md).


## The application is not working?

Supply me a screenshot with the console output (or the copied text).
If you are using the compiled windows version and a black window appears and then disappears it means the application crashes because of some error.
To view the error code to be able to send it to me:
In the folder where you have the .exe file, Shift + Rightclick in a free space and in the context menu there should be an option like "Open Command Prompt here" or "Open Powershell here", click that, begin writing "Graveyard" and then press tab to autocomplete and enter to execute - now you should start the application using that console window. This time the window won't close after execution, meaning you have time to make a screenshot of the error.

## Notice

This repository contains content which I do not own.
Notably all the image files in the /data/html/rsc folder. These are by [Lazy Bear Games](http://lazybeargames.com/).
Additionally [jQuery](https://jquery.com/) and [Materialize](https://materializecss.com/) are also used. Their original licenses are still included.
This application uses extracted strings like f.e. localisation files. These are also by [Lazy Bear Games](http://lazybeargames.com/).
If you find any bugs / mistakes, feel free to open issues, or if you know how to fix it yourself, feel free to create a pull request.

## Building

For those interested, here is the command I use to generate the folder which I then zip and upload as release:

(I have this saved as build.bat in the same folder)

```batch
python -m eel main.py "./data/html" -n "Graveyard Keeper Savefile Editor" -i "./data/html/favicon.ico" --exclude PyQt5 --exclude win32com --exclude pydoc --exclude lib2to3 -y

copy "%cd%\data\hashes" "%cd%\dist\Graveyard Keeper Savefile Editor\data\hashes" /Y
copy "%cd%\data\locals.json" "%cd%\dist\Graveyard Keeper Savefile Editor\data\locals.json" /Y
copy "%cd%\data\data.json" "%cd%\dist\Graveyard Keeper Savefile Editor\data\data.json" /Y
copy "%cd%\data\version" "%cd%\dist\Graveyard Keeper Savefile Editor\data\version" /Y
copy "%cd%\data\itemversion" "%cd%\dist\Graveyard Keeper Savefile Editor\data\itemversion" /Y

pause
```
