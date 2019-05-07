# Backtest Object File

# Imports
import pandas as pandas
import signals as signals
import indicators as indicators

# Backtest Class
class Backtest:
    """
    This class does the majority of executing and backtesting the
    financial thesis. This class utilizes the 'signals.py' and
    'indicators.py' modules to construct a Pandas DataFrame and
    run the 'iterate' function to determine the success of the
    financial thesis on historical data
    """
    # Class constructor
    def __init__(self, query, columns, capital, stop_loss, percentage, risk):
        """
        Constructs a backtest object to run the class's 'fillTable' and
        'iterate' functions

        :param query: Query object from 'query.py' module
        :param columns: List of column labels for the Pandas DF
        :param capital: Integer Amount of capital used in back testing the thesis
        :param stop_loss: float percentage value at which a current trade will be left
        :param percentage: float value that is the
        Maximum amount of capital used on any given trade
        :param risk: Waiting period time until position is entered after signal confirmation
        """

        # Instance Variables
        self.data = query
        self.df = pandas.DataFrame(data=self.data, columns=columns)
        self.capital = capital
        self.roi = 0.00
        self.inPosition = False
        self.percentage = percentage
        self.stop_loss = stop_loss
        self.investment = 0
        self.entrance = 0.00
        self.current = 0.00
        self.risk = risk
        self.shares = 0
        self.profit = 0.00
        self.total_profit = 0.00
        self.won = 0
        self.lost = 0
        self.trades = 0
        self.sma_fast = None
        self.sma_slow = None
        self.ema = None
        self.rsi = None

    def fillTable(self, sma_fast, sma_slow, ema, macd_fast, macd_slow, rsi_period):
        """
        The parameters passed into this function create new columns in the Pandas
        DataFrame 'self.df' to be utilized by the 'signals.py' module. Additionally,
        all of the parameters used in this function are based off personal analysis
        from my written financial thesis.

        **All of the parameters take only integer values**

        :param sma_fast: Fast simple moving average value (50)
        :param sma_slow: Slow simple moving average value (200)
        :param ema: Exponential moving average value (9)
        :param macd_fast: Fast moving average convergence divergence value (13)
        :param macd_slow: Slow moving average convergence divergence value (26)
        :param rsi_period: Relative strength index value (14)
        :return: Updated Pandas DataFrame
        """
        # Name the DataFrame Columns Appropriately
        self.sma_fast = "SMA"+str(sma_fast)
        self.sma_slow = "SMA"+str(sma_slow)
        self.ema_fast = "EMA" + str(ema)

        # Fill the Pandas DataFrame columns using 'signals.py' module functions
        indicators.simpleMA(self.df, sma_fast)
        indicators.simpleMA(self.df, sma_slow)
        indicators.exponentialMA(self.df, ema)
        indicators.movingAverageConvergence(self.df, macd_fast, macd_slow)
        indicators.rsi(self.df, rsi_period)

    def takePosition(self, column):
        """
        This function enters a trade when signals are met and calculates
        the specific analysis instance variables used to determine the profitability
        of the financial thesis
        :param column: Pandas DataFrame column
        :return:
        """
        self.entrance = column['VolumeWeightPrice']
        self.investment = self.capital * self.percentage
        self.shares = self.investment//self.entrance
        self.capital -= (self.entrance * self.shares)
        self.inPosition = True
        self.entrance = column['VolumeWeightPrice']
        self.trades += 1

    def leavePosition(self, column):
        """
        This function enters a trade when signals are met and calculates
        the specific analysis instance variables used to determine the profitability
        of the financial thesis
        :param column: Pandas DataFrame Column
        :return:
        """
        # Update instance variables
        self.capital += self.roi
        self.profit = ((self.current-self.entrance)* self.shares)
        self.total_profit += self.profit
        self.inPosition = False

        # Check if a trade was profitable
        if self.profit > 0:
            self.won += 1

        # Check if a trade was unprofitable
        if self.profit < 0:
            self.lost += 1

        # Reset instance variables for the next trade
        self.roi = 0.00
        self.shares = 0
        self.entrance = 0.00
        self.trades += 1
        self.profit = 0.00

    def iterate(self):
        """
        This function iterates through the entirety of a Pandas
        DataFrame and determines proper entrance and exit positions
        and executes historical trades based on technical indicator signals
        :return: Total profit for specific time period and ticker passed by user
        """
        exit_price = None
        period = 0
        # Loop through the rows and columns of the Pandas DF
        for row, column in self.df.iterrows():
            # Check if technical indicator signals have identified an entrance position
            if signals.positionEntrance(column[self.sma_slow], column[self.sma_fast], column['MACD'], column['RSI']):
                period += 1
                # If signals have been confirmed and currently not in a position, enter the position
                if not self.inPosition and period >= 70:
                    self.takePosition(column)
                    # Create stop loss value
                    exit_price = column['VolumeWeightPrice'] * (1.0 - self.stop_loss)
                if self.inPosition:
                    # Determine current profit for position being held
                    self.current = column['VolumeWeightPrice']
                    self.roi = self.current * self.shares

            # Check if technical indicator signals have identified an exit position
            if self.inPosition:
                if exit_price >= column['VolumeWeightPrice'] or signals.positionExit(column['MACD'], column['RSI']):
                    # Calculate ROI and profit as well as leave current position
                    self.current = column['VolumeWeightPrice']
                    self.roi = self.current * self.shares
                    self.leavePosition(column)
                    period = 0

        # Round total profit to two decimal places
        self.total_profit = round(self.total_profit, 2)

    def removeData(self):
        """
        This function removes pre-market and post-market
        data from the Pandas DataFrame
        :return:
        """
        for row, column in self.df.iterrows():
            time = str(column['TimeBarStart'])
            time = time.replace(":", "")
            time = int(time)
            if time < 930 or time > 1600:
                self.df.drop(row, inplace=True)
