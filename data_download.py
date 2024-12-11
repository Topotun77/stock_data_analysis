import numpy as np
import pandas as pd
import yfinance as yf
from pandas import DataFrame, merge
import pandas_ta as ta


def fetch_stock_data(ticker: str, period='1mo', interval='1d',
                     date_start=None, date_end=None) -> DataFrame:
    """
    Запрос данных
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param period: Период предоставления данных:
                   ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    :param interval: Интервал предоставления данных:
                     ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    :param date_start: Дата начала периода.
    :param date_end: Дата конца периода.
    :return: Данные в формате DataFrame
    """
    stock = yf.Ticker(ticker)
    try:
        data = stock.history(period=period, start=date_start, end=date_end, interval=interval)
    except Exception as er:
        return er.args
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
    try:
        data.ta.rsi(close='close', append=True)
        data.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    except:
        pass
    return data


def add_ATR(data: DataFrame) -> DataFrame:
    """
    Добавить расчет параметра ATR (Average True Range) - средний истинный диапазон
    :param data: DataFrame данные
    :return: Обновленные данные в формате DataFrame
    """
    def atr(high, low, close, n=14):
        tr = np.amax(
            np.vstack(((high - low).to_numpy(), (abs(high - close)).to_numpy(), (abs(low - close)).to_numpy())).T,
            axis=1)
        return pd.Series(tr).rolling(n).mean().to_numpy()

    data['ATR'] = atr(data['High'], data['Low'], data['Close'], 14)
    return data


def calculate_and_display_average_price(data: DataFrame, col='Close'):
    """
    Расчет и вывод среднего за выбранный период значения по столбцу -
    среднее на момент закрытия торгов.
    :param data: Объект класса DataFrame с данными для расчета.
    :param col: Столбец, по которому следует рассчитать среднее.
    :return: Среднее по столбцу
    """
    return data[col].mean(axis=0)
