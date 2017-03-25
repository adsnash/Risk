Thank you for taking the time to view my Risk simulation I built in Python to practice programming. I hope you enjoy it! 

If you have any questions, comments, concerns, or would like to hire me, please feel free to contact me. 

HOW TO INSTALL

If you plan to use the source code, you will need RiskGUI.py and Risk2.py as well as the images masterMap.png and RedR.png (or delete the lines pertaining to RedR.png). You will need Python 3.5 as well as the Pygame library, which can be installed with pip. 

I am including the cx_Freeze setup file (you can also install cx_Freeze with pip) to make the game an executable (or an app for Mac users). You will need to make sure that RiskGUI.py, Risk2.py, masterMap.png, RedR.png are all in the same directory before using it. 
Additionally, you must also have the .ttf files for freesansbold in the directory as well. Once you have installed Pygame, you can find it at C:/path/to/python/Lib/Site-packages/pygame. Copy the file freesansbold.ttf and place it in the same directory as the other files.
You will need to alter the a few lines in the cx_FreezeSetup.py file. Where it says "path/to/python" use the path to where Python is on your machine.
Then from the command line/terminal, once you've cd'd into the directory with the files, execute "python cx_FreezeSetup.py build" This will create a build folder with all the necessary files and folders.
There are a number of folders and files that cx_Freeze will create that are simply unnecessary and can be deleted (not sure if they're the same on Mac). The necessary folders are: collections, encodings, logging, and pygame. 
The necessary files are freesansbold.ttf, masterMap.png, python35.dll, python35.zip (these may be different depending on your version of Python. I used 3.5.2), README.txt (not completely necessary but good to have), RedR.png, RiskGUI.exe, and VCRUNTIME140.dll.

HOW TO PLAY

This Risk simulation functions much like the classic board game Risk (with a few exceptions). If you are unfamiliar with the rules of Risk, please visit: http://www.hasbro.com/common/instruct/risk.pdf

Please take note of the changes I have made that deviate from the original rules:

Country and troop placement is randomized.
Cards have been simplified. You may cash your cards when you have 3 or 4. Cards are automatically cashed when you have 5 or more.
Attacking and defending is set to use the maximum number of units and dice.
If an invasion is successful, only one unit MUST be placed into the new territory, regardless of how many units were attacking. Said unit will be placed automatically. Any additional troops can be placed in either territory at the player’s discretion. 

PRO TIP: When placing units, the left click will place them 1 at a time while the right click will place them 5 at a time. If the right click is pressed when there are less than 5 units, the remaining units will be placed. 

PLEASE NOTE: the button to advance to the next phase of your turn will have the next available action written on it. It will be red when active (meaning available to use) or grey if action must be taken (such as placing units).

HOW IT WORKS

RiskGUI.py is the main Python file which will produce the game when run, but it relies on Risk2.py, masterMap.png, and RedR.png. RiskGUI.py holds all the code relating to the GUI and the majority of the functions to run the game loop and update the display. 

Risk2.py holds data structures that keep track of who owns which territory and how many units are there (terr), which territory's touch which (touch), player information regarding total units, territories, and cards, as well as coordinates for placing troop numbers and connecting lines on the map (cords and alt cords). It also holds a number of sub functions as well which RiskGUI.py relies on to work. 

RedR.png is just a logo for the game. It won't affect the game in any meaningful way and can be deleted. A few lines must be removed from RiskGUI.py so that it won't crash. 

masterMap.png, the main map photo, has very specific RGB values. For the countries, the G value is 150, the B value is 100, and the R value is a number between 1 and 42 (corresponding to the 42 risk territories). My code changes their color based on the territory's owner by looping through each pixel and altering the color if it corresponds to a country. If masterMap.png is altered, the map may not display properly.  

LEGAL DISCLAIMER

Risk is a registered trademark of Parker Brothers. This simulation is for educational purposes only. I do not claim to own any of Parker Brothers’ intellectual property. Please don’t sue me!
