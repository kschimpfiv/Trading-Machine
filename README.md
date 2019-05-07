TITLE:
Developing an Algorithmic Trading Machine

INTRODUCTION:
This project creates a Graphical User interface to allow a user
to test a financial thesis I constructed using three statistical
indicators to determine profitable trades for twenty-five different
stocks over two years of historical data.

INTERNAL FILES: **add line about each file
backtest.py
database.py
gui.py
indicators.py
main.py
signals.py

LANGUAGES:
This program is written in Python 3.7

Python Libraries:
Glob
OS
Pandas
SQLite
TKinter


DATASET:
THis program utilizes an SQLite database and constructs a Pandas DataFrame
from a specific query that takes user input on ticker symbol and time period

**DISCLAIMER**
The data set was too large in size to upload to the GitHub repository and
therefore the user must utilize their own database in order to execute this
program. Additionally, the database must be created using the database.py
function and established in the project directory. For more information on table
labels and values, see the documentation in the database.py file in the project.

LAUNCH:
This project must be run using an IDE and was implemented using PyCharm. Open the
file within an IDE and run the Main.py file. A TKinter window will open and ask for
user input to execute the financial thesis. I am currently working on making this
accessible from the terminal

PROJECT STATUS:
Currently the program is running but not yielding high profits. This is most likely
due to under-optimized technical indicators that are implemented in indicators.py.
Additionally, the 'iterate' function implemented in the backtest.py file must also be
examined and refined.

SIGNALS/INDICATORS USED:
Simple Moving Average Crossover (50, 200)
Moving Average Converge Divergence (13, 26)
Relative Strength Index (14)


