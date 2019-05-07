# Indicators file

# This python file contains the functions to
# calculate all of the statistical indicators
# to test my financial thesis
# FUNCTIONS ARE UTILIZED IN 'backtest.py'

# Import Pandas library
import pandas as pandas


def changeDate(df):
    """
    converts the date values in the Pandas DataFrame
    :param df: Pandas DataFrame
    :return:
    """
    df['Date'] = pandas.to_datetime(df['Date'])


def simpleMA(df, period):
    """
    Calculates the simple moving average for a given period on
    the price of a stock and adds the value to the proper column
    in the Pandas DataFrame

    :param df: Pandas DataFrame
    :param period: Integer value used for
    simple moving average calculation
    :return:
    """
    df['SMA'+str(period)] = df['VolumeWeightPrice'].rolling(window=period).mean()


def exponentialMA(df, period):
    """
    Calculates the exponential moving average for a given period on
    the price of a stock and adds the value to the proper column
    in the Pandas DataFrame
    :param df: Pandas DataFrame
    :param period: Integer value used for
    exponential moving average calculation
    :return:
    """
    df['EMA'+str(period)]= df['VolumeWeightPrice'].ewm(span=period, min_periods=period).mean()


def movingAverageConvergence(df, fast, slow):
    """
    Calculates the moving average convergence divergence (MACD) value
    for a given period on the price of a stock and adds the value to
    the proper column in the Pandas DataFrame
    :param df: Pandas DataFrame
    :param fast: Integer value used for
    fast exponential moving average calculation
    :param slow: Integer value used for
    slow exponential moving average calculation
    :return:
    """

    # Calculate slow EMA
    slow_ema = df['VolumeWeightPrice'].ewm(span=slow, min_periods=slow).mean()
    # Calculate fast EMA
    fast_ema = df['VolumeWeightPrice'].ewm(span=fast, min_periods=fast).mean()

    # Add MACD value to the Pandas DF
    df['MACD'] = fast_ema - slow_ema


def rsi(df, period):
    """
     Calculates the Relative Strength Index (RSI) for a given period on
    the price of a stock and adds the value to the proper column
    in the Pandas DataFrame
    :param df: Pandas DataFrame
    :param period: integer value used for rsi calculation
    :return:
    """

    # Find differences in prices between two periods
    delta = df['VolumeWeightPrice'].diff()

    # Copy the array twice
    gain = delta.copy()
    loss = delta.copy()

    # Calculate gains and losses
    gain[gain < 0] = 0
    loss[loss > 0] = 0

    # Calculate average gains and losses
    average_gain = gain.rolling(window=period).mean()
    average_loss = loss.rolling(window=period).mean().abs()

    # Calculate Relative Strength
    rs = average_gain/average_loss

    # Add RSI to the table
    df['RSI'] = 100 - (100/(1+rs))
