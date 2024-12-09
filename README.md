# Анализ и визуализация данных об акциях
## В разработке...


• Графический и консольный интерфейс приложения.  
• Вывод графика на экран.  
• Сохранение графика в файл.  
• Расчет средней цены закрытия.  
• Выбор периода из списка.  
• Выбор тикета из списка.  
• Отображение результата в виде таблицы в GUI версии.  
• ООП подход при создании окна GUI интерфейса.  
• Добавлена документация функций и классов.  
• Добавлена аннотация переменных и функций.  
• Добавлено уведомление пользователя, если цена акций колебалась более чем на заданный процент за период.  
• Организовано меню приложения.  
• Информация о приложении вынесена в отдельный пункт меню `О программе`.  
• Исправлен вывод значений средней цены закрытия в случае невозможности ее вычисления.  
• Добавлена возможность экспортировать данные в CSV формате через меню `Файл/Сохранить в CSV` с выводом результата экспорта пользователю.  
• Добавлена возможность выбора имени файла через стандартное диалоговое окно при сохранении данных в CSV формате через меню `Файл/Сохранить как...`  
• После выгрузки данных открывает блокнот с сохраненным CSV файлом.  
• Добавлены иконки на кнопки и пункты меню.  
• Реализована функция для расчёта и отображения на графике дополнительных технических индикаторов RSI и MACD.  
• Добавлено обновление таблицы в случае изменений данных в полях ввода. Изменения отслеживаются при каждом выходе из любого поля ввода.  
• Добавлен выбор интервала данных.  
• Переопределены методы `parse_date(self)`, `__init__(self)` и `_validate_date(self)` класса `ateEntry` из модуля `tkcalendar` с целью возможности ввода пустых дат.  
• Добавлен выбор конкретных дат периода расчета.  
• **(NEW)** Добавлен исполняемый файл в папку `output`.  
• **(NEW)** Добавлена возможность выбора стиля оформления графиков.  

Для консольной версии запустите `main.py`  
Для GUI-версии запустите `main_win.py`  

### Окно приветствия - информация о приложении:
![img01](https://github.com/Topotun77/stock_data_analysis/blob/master/ScreenShots/n001.jpg?raw=true)
### Меню и интерфейс приложения:
![img01](https://github.com/Topotun77/stock_data_analysis/blob/master/ScreenShots/n005.jpg?raw=true)
### График с RSI и MACD (исторический момент - 05.12.2024 стоимость биткойна обновила исторический максимум, превысив $100 тыс.):
![img01](https://github.com/Topotun77/stock_data_analysis/blob/master/ScreenShots/n006.jpg?raw=true)
### Сообщение в случае превышения порога уведомления о разнице цен:
![img01](https://github.com/Topotun77/stock_data_analysis/blob/master/ScreenShots/n004.jpg?raw=true)

### Консольный вывод приложения:
```
Добро пожаловать в инструмент получения и построения графиков биржевых данных.
Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).
Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.
Введите тикер акции (например, «AAPL» для Apple Inc): aapl
Введите период для данных (например, '1mo' для одного месяца): 3mo
График сохранен как AAPL_3mo_stock_price_chart.png
Среднее цена закрытия: 227.5798
Введите значение порога колебания цены, при котором следует уведомлять пользователя: 10
Цена акций колебалась более чем на 10.0 % за выбранный период.
Максимальная цена: 242.39999389648438
Минимальная цена: 216.082275390625
Колебание составило: 12.18 %
Данные сохранены в файл: AAPL_2024-09-03-2024-12-03_data.csv.
```