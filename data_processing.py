import pandas as pd
from pandas import DataFrame
from datetime import date


def date_start_end(data: DataFrame) -> tuple[date, date]:
    """
    Определить дату начала и дату конца периода.
    :param data: Объект класса DataFrame с данными для расчета.
    :return: Дата начала периода, дата окончания периода
    """
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            return dates[0], dates[-1]
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
            return data['Date'][0], data['Date'][-1]


def notify_if_strong_fluctuations(data: DataFrame, threshold: float, col='Close') -> str | None:
    """
    Метод анализирует данные и уведомляет пользователя, если цена акций колебалась
    более чем на заданный процент за период.
    :param data: Объект класса DataFrame с данными для расчета.
    :param threshold: Порог превышения, при котором следует уведомлять пользователя
    :param col: Столбец для подсчета колебания
    :return: Уведомление пользователю
    """
    max_value = data[col].max(axis=0)
    min_value = data[col].min(axis=0)
    price_fluctuation = (max_value - min_value) / min_value * 100
    if price_fluctuation > threshold:
        return (f'Цена акций колебалась более чем на {threshold} % за выбранный период.\n'
                f'Максимальная цена: {max_value}\n'
                f'Минимальная цена: {min_value}\n'
                f'Колебание составило: {price_fluctuation:.2f} %')
    else:
        return None

