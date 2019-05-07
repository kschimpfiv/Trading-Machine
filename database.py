# Database Construction File

# Imports
import sqlite3 as sqlite3
import pandas as pandas
import os
import glob


# Create connection and cursor
connection = sqlite3.connect('trading.db')
cursor = connection.cursor()

# Create table for trading.db
def create_table():
    """
    Create a SQLite table to be converted to a Pandas DataFram
    :return:
    """
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS Algo_Trading(Date INTEGER, Ticker TEXT, TimeBarStart REAL, FirstTradePrice REAL, HighTradePrice REAL, LowTradePrice REAL, LastTradePrice REAL, VolumeWeightPrice REAL, Volume INTEGER, TotalTrades INTEGER)')
    except:
        print("Table not created")


# Create 'Algo_Trading' table
create_table()


# ***ONLY NEEDED IF TABLE NEEDS TO BE REMOVED***

#cursor.execute('drop table if exists Algo_Trading')

# Trading data directory paths
rootdir2015 = '2015/2015/**'
rootdir2016 = '2016/**'

# Import 2015 data to trading.db (Algo_Trading table)
# for filename in glob.iglob(rootdir2015, recursive=True):
#     if os.path.isfile(filename): # filter directories
#         df = pandas.read_csv(filename)
#         df.to_sql('Algo_Trading', connection, if_exists='append', index=False)

# Import 2016 data to trading.db (Algo_Trading table)
# for filename in glob.iglob(rootdir2016, recursive=True):
#     if os.path.isfile(filename): # filter subdirectories
#         df = pandas.read_csv(filename)
#         df.to_sql('Algo_Trading', connection, if_exists='append', index=False)



