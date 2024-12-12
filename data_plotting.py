import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from matplotlib import pylab
from pandas import DataFrame
from constants import FINANCIAL_CRISIS_LIST
from data_processing import date_start_end


def MACD_color(data: DataFrame):
    """
    Составление таблицы цветов для прорисовки графика MACD
    """
    color_list = []
    for i in range(0, len(data)):
        if data.iloc[i]['MACDh_12_26_9'] > data.iloc[i-1]['MACDh_12_26_9']:
            color_list.append(True)
        else:
            color_list.append(False)
    return color_list


def mark_financial_crises(ax: plt.Axes, date_start=None, date_end=None):
    """
    Разметить финансовые кризисы на графике (серые зоны).
    :param ax: Объект Axes отдельного (вспомогательного) графика
    :param date_start: Дата начала разметки
    :param date_end: Дата окончания разметки
    """
    for date_per in FINANCIAL_CRISIS_LIST:
        if date_per[1] >= date_start.date() and date_per[0] <= date_end.date():
            ax.axvspan(date_per[0], date_per[1], alpha=0.3, color='grey')


def create_basic_chart(data: DataFrame, ticker: str, ax: plt.Axes):
    """
    Метод создает основной график по данным
    :param data: Объект класса DataFrame с данными для расчета.
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param ax: Объект Axes отдельного (вспомогательного) графика
    :return: None | error
    """
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            ax.plot(dates, data['Close'].values, label='Close Price', color='blue', linewidth=0.8)
            ax.plot(dates, data['Moving_Average'].values, label='Moving Average', color='red', linewidth=0.8)
        else:
            return "Информация о дате отсутствует или не имеет распознаваемого формата."
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        ax.plot(data['Date'], data['Close'], label='Close Price', color='blue', linewidth=0.8)
        ax.plot(data['Date'], data['Moving_Average'], label='Moving Average', color='red', linewidth=0.8)

    ax.set_title(f"{ticker} Цена акций с течением времени")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Цена")
    ax.legend()


def create_RSI_chart(data: DataFrame, ax: plt.Axes):
    """
    Метод создает RSI график по данным
    :param data: Объект класса DataFrame с данными для расчета.
    :param ax: Объект Axes отдельного (вспомогательного) графика
    :return: None | error
    """
    try:
        if 'Date' not in data:
            if pd.api.types.is_datetime64_any_dtype(data.index):
                dates = data.index.to_numpy()
                ax.plot(dates, data['RSI_14'].values, label='RSI', linewidth=0.5)
            else:
                return "Информация о дате отсутствует или не имеет распознаваемого формата."
        else:
            if not pd.api.types.is_datetime64_any_dtype(data['Date']):
                data['Date'] = pd.to_datetime(data['Date'])
            ax.plot(data['Date'], data['RSI_14'].values, label='RSI', linewidth=0.5)
        ax.set_ylabel("RSI")
    except:
        pass


def create_any_chart(data: DataFrame, col_list: list, ax: plt.Axes):
    """
    Метод создает RSI график по данным
    :param data: Объект класса DataFrame с данными для расчета.
    :param col_list: Список колонок для вывода на график
    :param ax: Объект Axes отдельного (вспомогательного) графика
    :return: None | error
    """
    try:
        if 'Date' not in data:
            if pd.api.types.is_datetime64_any_dtype(data.index):
                dates = data.index.to_numpy()
                for i in col_list:
                    ax.plot(dates, data[i].values, label=i, linewidth=0.5)
            else:
                return "Информация о дате отсутствует или не имеет распознаваемого формата."
        else:
            if not pd.api.types.is_datetime64_any_dtype(data['Date']):
                data['Date'] = pd.to_datetime(data['Date'])
            for i in col_list:
                ax.plot(data['Date'], data[i].values, label=i, linewidth=0.5)
        ax.legend()
    except:
        pass


def create_MACD_chart(data: DataFrame, ax: plt.Axes):
    """
    Метод создает MACD график по данным
    :param data: Объект класса DataFrame с данными для расчета.
    :param ax: Объект Axes отдельного (вспомогательного) графика
    :return: None | error
    """
    try:
        data['positive'] = MACD_color(data)
        if 'Date' not in data:
            if pd.api.types.is_datetime64_any_dtype(data.index):
                dates = data.index.to_numpy()
                ax.plot(dates, data['MACD_12_26_9'].values, label='MACD', color='blue', linewidth=0.5)
                ax.plot(dates, data['MACDs_12_26_9'].values, label='Signal', color='red', linewidth=0.5)
                ax.bar(data.index, 'MACDh_12_26_9', data=data, label='Vol',
                        color=data.positive.map({True: 'g', False: 'r'}), width=1, alpha=0.8)
            else:
                return "Информация о дате отсутствует или не имеет распознаваемого формата."
        else:
            if not pd.api.types.is_datetime64_any_dtype(data['Date']):
                data['Date'] = pd.to_datetime(data['Date'])
            ax.plot(data['Date'], data['MACD_12_26_9'].values, label='MACD', color='blue', linewidth=0.5)
            ax.plot(data['Date'], data['MACDs_12_26_9'].values, label='Signal', color='red', linewidth=0.5)
            ax.bar(data.index, 'MACDh_12_26_9', data=data, label='Vol',
                    color=data.positive.map({True: 'g', False: 'r'}), width=1, alpha=0.8)
        ax.axhline(0, color='black', linewidth=0.5, alpha=0.5)
        ax.set_ylabel("MACD")
        ax.legend()
    except:
        pass


def create_and_save_plot(data: DataFrame, ticker: str, period: str, filename: str | None | bool = None,
                         style='default', crises=True) -> str:
    """
    Метод создает 3 графика по данным и сохраняет их на диск
    :param data: Объект класса DataFrame с данными для расчета.
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param period: Период предоставления данных:
                   ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    :param filename: Имя файла для сохранения изображения с графиком, по умолчанию имя файла будет
                     формироваться автоматически
    :param style: Стиль графика.
    :param crises: Флаг отметки на графике финансовых кризисов
    :return: Сообщение с результатом выполнения функции
    """
    plt.style.use(style)
    plt.figure(figsize=(8, 8))
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title(f'Цена акций, RSI и MACD для {ticker} с отметками финансовых кризисов')

    # Создать основной график
    ax1 = plt.subplot2grid(shape=(11, 10), loc=(0, 0), rowspan=5, colspan=10)
    err = create_basic_chart(data=data, ticker=ticker, ax=ax1)
    if err:
        return err
    dt_start_end = date_start_end(data)
    if crises:
        mark_financial_crises(ax1, *dt_start_end)

    # Создать RSI график
    ax2 = plt.subplot2grid((11, 10), (5, 0), rowspan=3, colspan=10)
    err = create_RSI_chart(data=data, ax=ax2)
    if err:
        return err
    if crises:
        mark_financial_crises(ax2, *dt_start_end)

    # Создать MACD график
    ax3 = plt.subplot2grid((11, 10), (8, 0), rowspan=3, colspan=10)
    err = create_MACD_chart(data=data, ax=ax3)
    if err:
        return err
    if crises:
        mark_financial_crises(ax3, *dt_start_end)

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    msg = ''
    if filename:
        plt.savefig(filename)
        msg = f"График сохранен как {filename}"
    plt.tight_layout()
    plt.show()
    return msg


def create_any_plot(data: DataFrame, col_list: list, ticker: str, style='default', crises=True) -> str:
    """
    Метод создает 3 графика по данным и сохраняет их на диск.
    :param data: Объект класса DataFrame с данными для расчета.
    :param col_list: Список столбцов для вывода на график.
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param style: Стиль графика.
    :param crises: Флаг отметки на графике финансовых кризисов
    :return: Сообщение с результатом выполнения функции
    """
    plt.style.use(style)
    plt.figure(figsize=(8, 8))
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title(f'Цена акций и дополнительные индикаторы для {ticker} '
                                        f'с отметками финансовых кризисов')

    # Создать основной график
    ax1 = plt.subplot2grid(shape=(11, 10), loc=(0, 0), rowspan=5, colspan=10)
    err = create_basic_chart(data=data, ticker=ticker, ax=ax1)
    if err:
        return err
    dt_start_end = date_start_end(data)
    if crises:
        mark_financial_crises(ax1, *dt_start_end)

    # Создать график из списка столбцов
    ax2 = plt.subplot2grid((11, 10), (5, 0), rowspan=6, colspan=10)
    err = create_any_chart(data=data, col_list=col_list, ax=ax2)
    if err:
        return err
    if crises:
        mark_financial_crises(ax2, *dt_start_end)

    plt.tight_layout()
    plt.show()


def create_interactive_chart(data: DataFrame, ticker: str, col_list: list = None):
    """
    Создание интерактивного графика
    :param data: Объект класса DataFrame с данными для расчета.
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param col_list: Список столбцов, по которым следует строить график.
    """
    fig = go.Figure()
    if not col_list:
        fig.add_trace(go.Scatter(x=data.index, y=data['Open'],mode='lines', name='Цена открытия'))
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'],mode='lines', name='Цена закрытия'))
        fig.add_trace(go.Scatter(x=data.index, y=data['High'],mode='lines', name='Максимальная цена'))
        fig.add_trace(go.Scatter(x=data.index, y=data['Low'],mode='lines', name='Минимальная цена'))
        fig.update_layout(title=f"{ticker} График цен",
                          xaxis_title="Date", yaxis_title="Price", showlegend=True)
    else:
        for i in col_list:
            fig.add_trace(go.Scatter(x=data.index, y=data[i], mode='lines', name=i))
        fig.update_layout(title=f"{ticker} График по выбранным столбцам",
                          xaxis_title="Date", showlegend=True)
    fig.show()
