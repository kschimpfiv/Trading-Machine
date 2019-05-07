# Graphical User Interface (GUI) FIle


# Imports
import tkinter as tk
from tkinter import ttk # CSS for tkinter
import sqlite3 as sqlite3
import backtest as backtest

# Import 'query.py' module
import query as query

# CONSTANTS AND STYLES
TITLE_FONT = ("Verdana", 18)
LARGE_FONT = ("Verdana", 12)

# Column Label Constants
COLUMNS = ['Date', 'Ticker', 'TimeBarStart','FirstTradePrice', 'HighTradePrice', 'LowTradePrice',
          'LastTradePrice', 'VolumeWeightPrice', 'Volume', 'TotalTrades']


class BackTestApp(tk.Tk):
    """
    This class is used to generate a
    Tkinter gui that allows the user to input
    a stock ticker, capital amount, time period,
    and risk value to execute the financial thesis
    carried out in the 'iterate' function within
    the 'backtest.py' module
    """

    # Constructor
    def __init__(self):

        tk.Tk.__init__(self)

        # GUI Title
        tk.Tk.wm_title(self, "Algorithmic Trading Machine")

        # Setting up container for the Tkinter GUI
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Setting up menu bar for TKinter GUI
        menubar = tk.Menu(container)

        # Add the StartPage Frame to the TKinter window
        tk.Tk.config(self, menu=menubar)
        self.frames = {}
        frame = StartPage(container, self)
        self.frames[0] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

# StartPage Class/Frame
class StartPage(tk.Frame):
    """
    This class is the main TKinter frame which executes
    and displays the financial thesis. Additionally, it
    is the primary visualization the user will interact
    with in the window
    """

    def __init__(self, parent, controller):
        """
        Constructor for the StartPage TKinter Frame
        :param parent: TKinter container
        :param controller: Tk object
        """
        tk.Frame.__init__(self, parent)

        # Backtest object instance variable
        self.test = None

        # Title Labels
        title_label = tk.Label(self, text="ALGORITHMIC TRADING MACHINE", font=TITLE_FONT)
        title_label.grid(row=0, column=3,columnspan=2, padx=10)

        # Ticker Labels and Entries
        ticker_label = tk.Label(self, text="Ticker Symbol:", font=LARGE_FONT)
        ticker_label.grid(row=1, column=0, pady=10, sticky="E")
        self.ticker_entry = tk.Entry(self)
        self.ticker_entry.grid(row=1, column=1, pady=10)

        # Capital Labels and Entries
        capital_label = tk.Label(self, text="Capital:", font=LARGE_FONT)
        capital_label.grid(row=2, column=0, pady=10, sticky="E")
        self.capital_entry = tk.Entry(self)
        self.capital_entry.grid(row=2, column=1, pady=10)

        # Time Period Labels and Entries
        time_label = tk.Label(self, text="Time Period:", font=LARGE_FONT)
        time_label.grid(row=3, column=0, pady=10, sticky="E")
        self.time_entry = tk.Entry(self)
        self.time_entry.grid(row=3, column=1, pady=10)

        # Risk Labels and Entries
        risk_label = tk.Label(self, text="Risk:", font=LARGE_FONT)
        risk_label.grid(row=4, column=0, pady=10, sticky="E")
        self.risk_entry = tk.Entry(self)
        self.risk_entry.grid(row=4, column=1, pady=10)

        # Execute Button
        execute_button = ttk.Button(self, text="Execute", command=lambda: performBacktest())
        execute_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="N")

        # Refresh Button
        refresh_button = ttk.Button(self, text="Refresh", command=lambda: refresh())
        refresh_button.grid(row=5, column=2, columnspan=2, pady=10, sticky="N")

        # Ticker Instructions and Placement
        ticker_instructions = tk.Label(self,text="Please choose a ticker symbol from the "
                                          "25 symbols provided in the link below")
        ticker_instructions.grid(row=1, column=3, pady=10, sticky="W")

        # Capital Instructions and Placement
        capital_instructions = tk.Label(self, text="Amount of capital for trades"
                                                  " (e.g. 1000000)")
        capital_instructions.grid(row=2, column=3, pady=10, sticky="W")

        # Time Period Instructions and Placement
        time_instructions = tk.Label(self, text="Time period to backtest trading algorithm"
                                                   "(e.g. 20150514, 20150527)")
        time_instructions.grid(row=3, column=3, pady=10, sticky="W")

        # Risk Value Instructions and Placement
        risk_instructions = tk.Label(self, text="Percentage of capital used on a given trade"
                                                    "(e.g. 0.2)")
        risk_instructions.grid(row=4, column=3, pady=10, sticky="W")

        # Ticker list and Placement
        ticker_list1 = tk.Label(self,text="List of Symbols: CVX, XOM, GE, LMT, AMZN, HD, PEP, MMM, "
                                          "JNJ, UNH, GS")
        ticker_list1.grid(row=6, column=3, columnspan=4, sticky="W")
        ticker_list2 = tk.Label(self, text="MS, GOOGL, ITNC, VZ, CMCSA, DUK, D, SPG, AMT, WRK, AA,"
                                           " TSLA, AAPL, JPM")
        ticker_list2.grid(row=7, column=3, columnspan=4, sticky="W")

        # Output instance variables
        self.total_profit = None
        self.total_trades = None
        self.total_won = None

        def getParameters():
            """
            This functions retrieves the user inputs
            for the 4 parameters typed in by the user
            :return: Dictionary of input labels and
            associated user responses
            """

            # Create and fill parameters dictionary
            parameters = {}
            parameters['Ticker'] = self.ticker_entry.get()
            parameters['Capital'] = int(self.capital_entry.get())
            time_parameters = self.time_entry.get().split(',')
            parameters['Time'] = list(map(int, time_parameters))
            parameters['Risk'] = float(self.risk_entry.get())

            return parameters

        def performBacktest():
            """
            This function creates a backtest object when the user
            presses the GUI 'Execute' Button and runs the 'iterate'
            function from the 'backtest.py' module to determine the user
            success and profit utilizing the financial thesis for the
            given inputs
            :return:
            """
            # Retrieve parameters from GUI
            parameters = getParameters()

            # Connect to the 'trading.db' database
            connection = sqlite3.connect('trading.db')

            # Create SQLite cursor
            cursor = connection.cursor()

            # Query data from the 'trading.db' SQLite database
            data = query.readFromDB(parameters['Ticker'], parameters['Time'][0], parameters['Time'][1], cursor)

            # Construct a backtest object using 'backtest.py' module
            self.test = backtest.Backtest(data, COLUMNS, parameters['Capital'], 0.05, parameters['Risk'], 100)

            # Fill the Pandas DataFrame with indicator parameters
            self.test.fillTable(50, 200, 9, 13, 26, 14)

            # Execute the financial thesis using the 'backtest.py' module 'iterate' function
            self.test.iterate()

            # Call the 'StartPage' analysis function to display results in the GUI
            analysis(self.test)


        def analysis(test):
            """
            This function displays the total profit, total number of trades, and the
            profitable trades returned by the 'iterate' function from the 'backtest.py' module
            :param test: 'backtest.py' object created in performBacktest function
            :return:
            """
            self.total_profit = tk.Label(self, text="Profit: " + str(test.total_profit), font=LARGE_FONT)
            self.total_profit.grid(row=6, column=0, pady=10, sticky="E")
            self.total_trades = tk.Label(self, text="Total Trades: " + str(test.won + test.lost), font=LARGE_FONT)
            self.total_trades.grid(row=7, column=0, pady=10, sticky="E")
            self.total_won = tk.Label(self, text="Profitable Trades: " + str(test.won), font=LARGE_FONT)
            self.total_won.grid(row=8, column=0, pady=10, sticky="E")

        def refresh():
            """
            Refreshes the test object and profit labels to
            execute another backtest analysis on a different
            set of data
            :return:
            """
            # Destroy previous profit and trade labels
            self.total_profit.destroy()
            self.total_trades.destroy()
            self.total_won.destroy()

            # Set the instance variable labels to none
            self.total_profit = None
            self.total_trades = None
            self.total_won = None
            self.test = None

