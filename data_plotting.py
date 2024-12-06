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


def MACD_color(data):
    color_list = []
    for i in range(0, len(data)):
        if data.iloc[i]['MACDh_12_26_9'] > data.iloc[i-1]['MACDh_12_26_9']:
            color_list.append(True)
        else:
            color_list.append(False)
    return color_list


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
    plt.figure(figsize=(8, 8))
    ax1 = plt.subplot2grid(shape=(11, 10), loc=(0, 0), rowspan=5, colspan=10)

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            ax1.plot(dates, data['Close'].values, label='Close Price')
            ax1.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            return "Информация о дате отсутствует или не имеет распознаваемого формата."
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        ax1.plot(data['Date'], data['Close'], label='Close Price')
        ax1.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    ax1.set_title(f"{ticker} Цена акций с течением времени")
    ax1.set_xlabel("Дата")
    ax1.set_ylabel("Цена")
    ax1.grid()
    ax1.legend()

    try:
        ax2 = plt.subplot2grid((11, 10), (5, 0), rowspan=3, colspan=10)
        if 'Date' not in data:
            if pd.api.types.is_datetime64_any_dtype(data.index):
                dates = data.index.to_numpy()
                ax2.plot(dates, data['RSI_14'].values, label='RSI', linewidth=0.5)
            else:
                return "Информация о дате отсутствует или не имеет распознаваемого формата."
        else:
            if not pd.api.types.is_datetime64_any_dtype(data['Date']):
                data['Date'] = pd.to_datetime(data['Date'])
            ax2.plot(data['Date'], data['RSI_14'].values, label='RSI', linewidth=0.5)
        ax2.set_ylabel("RSI")
        ax2.grid()
        # ax2.legend()
    except:
        pass

    try:
        ax3 = plt.subplot2grid((11, 10), (8, 0), rowspan=3, colspan=10)
        data['positive'] = MACD_color(data)
        if 'Date' not in data:
            if pd.api.types.is_datetime64_any_dtype(data.index):
                dates = data.index.to_numpy()
                ax3.plot(dates, data['MACD_12_26_9'].values, label='MACD', color='blue', linewidth=0.5)
                ax3.plot(dates, data['MACDs_12_26_9'].values, label='Signal', color='red', linewidth=0.5)
                ax3.bar(data.index, 'MACDh_12_26_9', data=data, label='Vol',
                        color=data.positive.map({True: 'g', False: 'r'}), width=1, alpha=0.8)
            else:
                return "Информация о дате отсутствует или не имеет распознаваемого формата."
        else:
            if not pd.api.types.is_datetime64_any_dtype(data['Date']):
                data['Date'] = pd.to_datetime(data['Date'])
            ax3.plot(data['Date'], data['MACD_12_26_9'].values, label='MACD', color='blue', linewidth=0.5)
            ax3.plot(data['Date'], data['MACDs_12_26_9'].values, label='Signal', color='red', linewidth=0.5)
            ax3.bar(data.index, 'MACDh_12_26_9', data=data, label='Vol',
                    color=data.positive.map({True: 'g', False: 'r'}), width=1, alpha=0.8)
        ax3.axhline(0, color='black', linewidth=0.5, alpha=0.5)
        ax3.set_ylabel("MACD")
        ax3.grid()
        ax3.legend()
    except:
        pass

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    msg = ''
    if filename:
        plt.savefig(filename)
        msg = f"График сохранен как {filename}"
    plt.tight_layout()
    plt.show()
    return msg
