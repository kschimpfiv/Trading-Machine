# Signals File

# This python file contains the functions to
# to determine entrance and exit signals
# to test my financial thesis
# FUNCTIONS ARE UTILIZED IN main.py

# ENTRANCE SIGNALS
def goldenCrossEntrance(slow, fast):
    """
    Determines if the entrance signal for the golden crossover
    is met or not
    :param slow: Slow integer simple moving average value
    :param fast: Fast integer simple moving average value
    :return: Boolean value for whether or
    not the signal is met
    """
    if slow <= fast:
        return True
    else:
        return False


def macdEntrance(divergence):
    """
    Determines if the entrance signal for the Moving Average
    Convergence Divergence (MACD) is met or not
    :param divergence: float value for the macd divergence
    :return: Boolean value for whether or
    not the MACD signal is met
    """
    if divergence > 0:
        return True
    else:
        return False


def rsiEntrance(rsi):
    """
    Determines if the entrance signal for the Relative
    Strength Index is met or not
    :param rsi: integer rsi period value
    :return: Boolean value for whether or
    not the RSI signal is met
    """
    if rsi >= 55:
        return True
    else:
        return False


def positionEntrance(slow, fast, divergence, rsi):
    """
    This functions combines the goldenCrossEntrance, macdEntrance,
    and rsiEntrance functions to determine whether or not a position
    entrance can be identified
    :param slow: Slow integer simple moving average value
    :param fast: Fast integer simple moving average value
    :param divergence: float value for the macd divergence
    :param rsi: integer rsi period value
    :return: Boolean value for whether or
    not the finacial thesis signal is met
    """
    if goldenCrossEntrance(slow, fast) and macdEntrance(divergence) and rsiEntrance(rsi):
        return True
    else:
        return False


# EXIT SIGNALS
def macdExit(divergence):
    """
    Determines if the exit signal for the Moving Average
    Convergence Divergence (MACD) is met or not
    :param divergence: float value for the macd divergence
    :return: Boolean value for whether or
    not the MACD entrance signal is met
    """
    if divergence < 0:
        return True
    else:
        return False


def rsiExit(rsi):
    """
    Determines if the entrance signal for the Relative
    Strength Index is met or not
    :param rsi: integer rsi period value
    :return: Boolean value for whether or
    not the RSI signal is met
    """
    if rsi < 55:
        return True
    else:
        return False


def positionExit(divergence, rsi):
    """
    This functions combines the macdEntrance and rsiEntrance
    functions to determine whether or not a position
    exit can be identified
    :param divergence: float value for the macd divergence
    :param rsi: integer rsi period value
    :return: Boolean value for whether or
    not the finacial thesis exit signal is met
    """
    if macdExit(divergence) or rsiExit(rsi):
        return True
    else:
        return False

