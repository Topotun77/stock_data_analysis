import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def export_data_to_csv(data: DataFrame, filename: str | None = None, ticker: str = ''):
    """
    Экспортировать данные в CSV формате
    :param data: Объект класса DataFrame с данными для экспорта.
    :param filename: Имя файла для экспорта, по умолчанию формируется автоматически.
    :param ticker: Название тикета.
    :return: Картеж (успех/неудача, сообщение пользователю)
    """
    if filename is None:
        filename = f"{ticker}_{str(data.index[0]).split()[0]}-{str(data.index[-1]).split()[0]}_data.csv"
    try:
        data.to_csv(filename, sep=',', encoding='utf-8')
        return True, f'{filename}'
    except Exception as er:
        return False, er.args


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


def calculate_and_display_average_price(data: DataFrame, col='Close'):
    """
    Расчет и вывод среднего за выбранный период значения по столбцу -
    среднее на момент закрытия торгов.
    :param data: Объект класса DataFrame с данными для расчета.
    :param col: Столбец, по которому следует рассчитать среднее.
    :return: Среднее по столбцу
    """
    return data[col].mean(axis=0)


def create_and_save_plot(data: DataFrame, ticker: str, period: str, filename: str | None | bool = None) -> str:
    """
    Метод создает график по данным и сохраняет его на диск
    :param data: Объект класса DataFrame с данными для расчета.
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param period: Период предоставления данных:
                   ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    :param filename: Имя файла для сохранения изображения с графиком, по умолчанию имя файла будет
                     формироваться автоматически
    :return: Сообщение с результатом выполнения функции
    """
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            return "Информация о дате отсутствует или не имеет распознаваемого формата."
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    plt.subplot(2, 1, 2)
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['RSI'].values, label='RSI')
        else:
            return "Информация о дате отсутствует или не имеет распознаваемого формата."
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['RSI'].values, label='RSI')

    plt.title(f"{ticker} RSI")
    plt.xlabel("Дата")
    plt.ylabel("Индекс относительной силы")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    msg = ''
    if filename:
        plt.savefig(filename)
        msg = f"График сохранен как {filename}"
    plt.tight_layout()
    plt.show()
    return msg
