import math
import data_download as dd
import data_plotting as dplt
import data_export as dexp
import data_processing as dp


def main():
    """
    Основная функция консольного приложения. Запрашивает данные у пользователя, формирует запрос,
    в Yahoo Finance с использованием фреймворка yfinance, формирует график и
    рассчитывает среднюю цену закрытия за заданный период.
    """
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), "
          "GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, "
          "с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ").upper()
    # ticker = 'AAPL'
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")
    # period = '5d'

    # Получить данных
    stock_data = dd.fetch_stock_data(ticker, period)

    # Добавить скользящее среднее значение к данным
    stock_data = dd.add_moving_average(stock_data)

    # Добавить дополнительные технические индикаторы: RSI и MACD
    stock_data = dd.add_rsi_macd(stock_data)

    # Построить график
    print(dplt.create_and_save_plot(stock_data, ticker, period))

    # Найти среднюю цену закрытия
    mean_close = dd.calculate_and_display_average_price(stock_data)
    if math.isnan(mean_close):
        print('Не удалось определить среднюю цену закрытия.')
    else:
        print(f'Среднее цена закрытия: {mean_close:.4f}')

    # Проверить колебание цены закрытия за выбранный период
    threshold = float(input('Введите значение порога колебания цены, при котором следует уведомлять пользователя: '))
    message = dp.notify_if_strong_fluctuations(stock_data, threshold)
    if message:
        print(message)

    # Экспортировать данные в CSV формате
    err = dexp.export_data_to_csv(stock_data, ticker=ticker)
    if not err[0]:
        print('Ошибка! ' + err[1])
    else:
        print(f'Данные сохранены в файл: {err[1]}.')


if __name__ == "__main__":
    main()
