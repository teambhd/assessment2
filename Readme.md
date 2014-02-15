This directory contains the source code for our Assessment 2 game, titled Don't Crash.

## Running the game

The easiest way to play the game is to visit https://teambhd.github.io/assessment2/ in your favourite web browser. The version on that site should (hopefully) be identical to that available for download on the team website.

To run the game on a local computer (for development, or for marking the submission) you can follow the instructions below:

* Open a terminal (command prompt) window. On Windows you can press *Win + R* and then type *cmd* and press enter. On a Mac open Terminal.app within the Applications folder. On the department Linux install, you can press *Alt + F2* and then type *xterm* and press enter, users of other desktop environments probably already know what to do!
* Run *cd [path]*, where [path] is the path to the directory containing this Readme file.
* Run *python server.py*. This sometimes causes a Windows Firewall message to appear, that box can safely be ignored.
* Open your favourite web browser (we've tested Safari, Chrome and Firefox; recent versions of Opera probably also work) and go to http://localhost:8000. Windows users may have to use http://127.0.0.1:8000 if the first address gives an error.

## Playing the game

Some instructions are provided on the Help screen, which is accessible from the main game menu. There is also a user manual linked from our team website, and provided with the zipped submission.

## Understanding the source code

Within this directory are several files and sub-folders, explanations of which are as follows:

The **code** folder contains the Python source code files specific to our game. Within the game itself, the file "main.py" is run initially, and includes other files as needed. Files beginning with "page-" perform a similar function for menu screens. Files beginning with "test-" contain automated tests for various components (these can be run using the automated tests link on the footer of the main menu screen) and the remaining files are modules that can be imported.

The **Lib** and **libs** folders contain modules within the Python standard library (plus a few browser-related extras within the browser folder), implemented in Python and JavaScript respectively.

The **.html** files in the root directory are page templates, with game.html being the main game, help.html the help screen and so on. The **stylesheets** and **images** folders contain static resources to be included by those templates.

**manual.pdf** is the latest published version of the user manual, which amalgamates information from this Readme and from the in-game help screens in a printable format. The .docx files used to create the PDF manual are located within the **manual** folder in the separate assessment2-extras repository.

Finally, the **legal** directory contains license agreements for various open-source components used by the game. These are linked to from the Attribution screen linked to from the main menu.
