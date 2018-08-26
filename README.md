Graveyard-Keeper-Savefile-Editor
================================
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a save editor for Graveyard Keeper.  

It can load and save *.dat files.  
Additionally you can export the loaded save to a .json file, which has a similar structure to the original .json save files.  
(The difference is, that information about types of variables is saved in the file, meaning every value is wrapped in an object).  

The Application uses your Browser (preferably Chrome) as a GUI.  

## Screenshot

![Preview](https://i.imgur.com/P5izmMi.png)

## Installation

* Download this as zip and extract it to the folder where you want it to be
* Get Python (>=3.3)
* If you don't have it installed, install Eel as module --> Type the following in a console `python -m pip install Eel`
* Execute the file with `python main.py` (in the console with the folder where main.py resides as working directory - to simplify this just create a `run.bat` in the directory with the same content)
* Enjoy

**OR**

Download a compiled release for windows.

## Usage

Considering the application has a GUI it should be self explanatory.  
If a name autocompletes to undefined, it might be that this item is not available in the game yet, or my localisation files are missing translations.


If you want to manually edit save files, when you change values, watch out if you change the type of the variable. F.e. if you would change a value from 0 to 1, the type would change and you would need to manually change the type to the correct one.  
For information about the possible types, check types.py in the data folder.  


## Notice

This repository contains content which I do not own.  
Notably all the image files in the /data/html/rsc folder. These are by [Lazy Bear Games](http://lazybeargames.com/). And were (to big parts) extracted from the [Wiki](https://graveyardkeeper.gamepedia.com/Graveyard_Keeper_Wiki) (for information on how I did it, check misc.py)  
Additionally [jQuery](https://jquery.com/) and [Materialize](https://materializecss.com/) are also used. Their original licenses are still included.
This application uses extracted strings like f.e. localisation files. These are also by [Lazy Bear Games](http://lazybeargames.com/) and might be incorrect. (Because of my horrible way of extracting them)  
If you find any bugs / mistakes, feel free to open issues, or if you know how to fix it yourself, feel free to create a pull request.