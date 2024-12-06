# Значение по умолчанию порога колебания цен
FLUCTUATIONS_DEFAULT = 25

# Иконки кнопок и пунктов меню
ICON_CALC = './Media/calc.png'
ICON_CHART = './Media/chart.png'
ICON_SAVE = './Media/save.png'

# Список и значение по умолчанию периодов для данных
LIST_TIK = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'BTC-USD']
TIK_DEFAULT = 'GOOGL'

# Список и значение по умолчанию периодов для данных
LIST_PERIOD = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
PERIOD_DEFAULT = '3mo'

# Список интервалов данных, значение по умолчанию и интервалы,
# для которых не требуется вывод времени
LIST_INTERVAL = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
INTERVAL_DEFAULT = '1d'
INTERVAL_NOT_TIME = ['1d', '5d', '1wk', '1mo', '3mo']

# Текст окна приветствия
INFO = """Добро пожаловать в инструмент получения и построения графиков биржевых данных.

Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть:
AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).

Общие периоды времени для данных о запасах включают:
1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5л, 10л, с начала года, макс.
"""