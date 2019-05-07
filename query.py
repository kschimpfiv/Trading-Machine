# Query File

# This python file creates a query
# to retrieve data from 'trading.db'
# for back testing the financial thesis

def readFromDB(ticker, start, end, cursor):
    """
    This function queries a specific dataset from the
    'trading.db' SQLite database based on user inputs in
    the 'gui.py' module and turns the query into a Pandas
    DataFrame in the 'backtest.py' module

    :param ticker: String ticker symbol (e.g. AAPL)
    :param start: Integer starting date
    :param end: Integer ending date
    :param cursor: SQLite cursor
    :return:
    """
    cursor.execute('SELECT * FROM Algo_Trading WHERE Ticker=? AND Date>=? AND DATE<=? ORDER BY Date ASC', (ticker, start, end))
    data = cursor.fetchall()
    return data


