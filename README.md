Graveyard-Keeper-Savefile-Editor
================================
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a save editor for [Graveyard Keeper](https://store.steampowered.com/app/599140/Graveyard_Keeper/).

The python version works on Windows, Linux and macOS.
For Windows there is a .exe version available too.

It can load and save *.dat files.
Additionally you can export the loaded save to a .json file, which has a similar structure to the original .json save files.
(The difference is, that information about types of variables is saved in the file, meaning every value is wrapped in an object).

The Application uses a webbrowser as a GUI (by default Chrome in App Mode).

I want to add I am not responsible if you break your save file, I try to mantain this editor in a way, in which it can't break save files (or not by mistake) but it is still possible that this editor produces a bugged save file (if you f.e. add an item in a quality in which the item doesn't exist.)
That is why you always should backup your save files. (In the settings of the editor you can also set the number of backups the editor should create (which are zipped) - on saving the editor all backups are shifted by one, so if set it to 3 backups and save 4 times, your oldest backup is lost).

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
  * Setting the worker efficiency to the highest possible level
  * Turning the graves into perfect graves
  * Complete the entire tech tree
  * Fix if the donkey is stuck

## Screenshot

![Preview](https://i.imgur.com/XZdmo3Z.png)

## Installation

* Download this as zip and extract it to the folder where you want it to be
* Get Python (>=3.3)
* If you are using a macOS/Linux system where `python` is by default python 2.x, replace `python` with `python3`. Also instead of creating a .bat file, create a .sh file.
* Install dependencies using `python -m pip install -r requirements.txt`.
* Execute the file with `python main.py` (in the console with the folder where main.py resides as working directory - to simplify this just create a `run.bat` in the directory with the same content)
* Enjoy

**OR**

Download a [frozen release](https://github.com/NetroScript/Graveyard-Keeper-Savefile-Editor/releases) for windows (so you don't need to install python).

## Usage

Considering the application has a GUI it should be self explanatory.
If a name autocompletes to undefined, the item has no internal name or my localisation files are missing translations.
If you know a item exists, but it doesn't appear in the autocompletion box, leave me a message, this means I forgot some items in my list with items.
Same if an item doesn't have a preview image - if that happens please leave me a message with the internal id (written in parentheses) and a screenshot of the item in game (so I know which item in the spritesheet is the id)


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
Notably all the image files in the /data/html/rsc folder. These are by [Lazy Bear Games](http://lazybeargames.com/). And were (to big parts) extracted from the [Wiki](https://graveyardkeeper.gamepedia.com/Graveyard_Keeper_Wiki) (for information on how I did it, check [misc.py](https://github.com/NetroScript/Graveyard-Keeper-Savefile-Editor/blob/0.1.0/data/misc.py))
Additionally [jQuery](https://jquery.com/) and [Materialize](https://materializecss.com/) are also used. Their original licenses are still included.
This application uses extracted strings like f.e. localisation files. These are also by [Lazy Bear Games](http://lazybeargames.com/) and might be incorrect. (Because of my horrible way of extracting them)
If you find any bugs / mistakes, feel free to open issues, or if you know how to fix it yourself, feel free to create a pull request.

## Building

For those interested, here is the command I use to generate the folder which I then zip and upload as release:

(I have this saved as build.bat in the same folder)

```batch
python -m eel main.py "./data/html" -n "Graveyard Keeper Savefile Editor" -i "./data/html/favicon.ico" --exclude PyQt5 --exclude win32com --exclude pydoc --exclude lib2to3 -y

copy "%cd%\data\hashes" "%cd%\dist\Graveyard Keeper Savefile Editor\data\hashes" /Y
copy "%cd%\data\locals.json" "%cd%\dist\Graveyard Keeper Savefile Editor\data\locals.json" /Y
copy "%cd%\data\perfectbody.json" "%cd%\dist\Graveyard Keeper Savefile Editor\data\data.json" /Y
copy "%cd%\data\version" "%cd%\dist\Graveyard Keeper Savefile Editor\data\version" /Y
copy "%cd%\data\itemversion" "%cd%\dist\Graveyard Keeper Savefile Editor\data\itemversion" /Y

pause
```
