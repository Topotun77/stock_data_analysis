import yfinance as yf
from pandas import DataFrame, merge
import pandas_ta as ta


def fetch_stock_data(ticker: str, period='1mo') -> DataFrame:
    """
    Запрос данных
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param period: Период предоставления данных:
                   ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    :return: Данные в формате DataFrame
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data: DataFrame, window_size=5) -> DataFrame:
    """
    Добавить столбец со средним в окне к данным
    :param data: DataFrame данные
    :param window_size: Размер окна для расчета среднего (по умолчанию 5 дней)
    :return: Обновленные данные в формате DataFrame
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def add_rsi_macd(data: DataFrame) -> DataFrame:
    """
    Добавить столбцы RSI и MACD, отражающие технические индикаторы:
    отношение восходящих движений цены к нисходящим за определённый период времени (RSI)
    индикатор схождения-расхождения скользящих средних (MACD)
    :param data: DataFrame данные
    :return: Обновленные данные в формате DataFrame
    """
    data['RSI'] = ta.rsi(data['Close'])
    macd = ta.macd(data['Close'])
    if not macd is None:
        data = merge(data, macd, left_index=True, right_index=True)
    return data
