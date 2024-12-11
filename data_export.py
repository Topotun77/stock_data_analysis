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
