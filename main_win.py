import math
import subprocess
from functools import partial
from datetime import date

import data_download as dd
import data_plotting as dplt
import data_export as dexp
import data_processing as dp
from utilities import image_to_icon

import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from constants import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkcalendar import DateEntry
from pandas import DataFrame


def query_data(ticker: str, period: str = PERIOD_DEFAULT, interval: str = INTERVAL_DEFAULT,
               date_start=None, date_end=None) -> DataFrame:
    """
    Запрос данных с Yahoo Finance с использованием фреймворка yfinance
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param period: Период предоставления данных:
                   ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    :param interval: Интервал предоставления данных:
                     ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    :param date_start: Дата начала периода расчета.
    :param date_end: Дата окончания периода расчета.
    :return: Объект класса DataFrame (pandas)
    """
    # Получить данных
    stock_data = dd.fetch_stock_data(ticker, period=period, interval=interval,
                                     date_start=date_start, date_end=date_end)

    if type(stock_data) != DataFrame:
        return stock_data

    # Добавить скользящее среднее значение к данным
    stock_data = dd.add_moving_average(stock_data)

    # Добавить дополнительные технические индикаторы: RSI и MACD
    stock_data = dd.add_rsi_macd(stock_data)

    # Добавить дополнительные технические индикаторы: ATR
    stock_data = dd.add_ATR(stock_data)

    return stock_data


class DateEntryNone(DateEntry):
    """
    Переопределяем методы для возможности ввода пустой даты
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_parse_date = self.parse_date
        self.parse_date = self.new_parse_date

    def _validate_date(self):
        if not self.get():
            return True
        return super()._validate_date()

    def new_parse_date(self, text):
        if not text:
            return date.today()
        else:
            return self.old_parse_date(text)


class Ticker:
    """
    Класс GUI со всеми элементами и методами окна
    """

    def __init__(self, win: tk.Tk):
        self.win = win
        self.win.option_add("*tearOff", FALSE)

        """Список столбцов для интерактивного графика"""
        self.col_list_to_inter_chart = []

        self.icon_save = image_to_icon(ICON_SAVE)
        self.icon_chart = image_to_icon(ICON_CHART)
        self.icon_mean = image_to_icon(ICON_CALC)

        self.file_menu = tk.Menu()
        self.file_menu.add_command(label=' Сохранить в CSV',
                                   command=self.save_csv,
                                   image=self.icon_save,
                                   compound=LEFT)
        self.file_menu.add_command(label=' Сохранить как...',
                                   command=partial(self.save_csv, True),
                                   image=self.icon_save,
                                   compound=LEFT)

        self.menu_chart = tk.Menu()
        self.menu_chart.add_command(label=' Основной график',
                                    command=self.button_plot_click,
                                    image=self.icon_chart,
                                    compound=LEFT)
        self.menu_chart.add_command(label=' Дополнительный график',
                                    command=self.button_plot_click_2,
                                    image=self.icon_chart,
                                    compound=LEFT)
        self.menu_chart.add_separator()
        self.menu_chart.add_command(label=' Стандартный интерактивный график',
                                    command=self.button_plot_inter_click,
                                    image=self.icon_chart,
                                    compound=LEFT)
        self.menu_chart.add_command(label=' Интерактивный график по выбранным столбцам',
                                    command=partial(self.button_plot_inter_click,
                                                    self.col_list_to_inter_chart),
                                    image=self.icon_chart,
                                    compound=LEFT)

        self.main_menu = tk.Menu()
        self.main_menu.add_cascade(label='Файл', menu=self.file_menu)
        self.main_menu.add_cascade(label='Построение графиков', menu=self.menu_chart)
        self.main_menu.add_command(label='О программе', command=self.show_info)
        # self.win.bind_all('<F1>', self.show_info)

        self.win.title('Анализ и визуализация данных об акциях')
        try:
            self.win.iconbitmap(default="./Media/favicon.ico")
            # TODO Для компиляции с помощью auto-py-to-exe заменить строку выше на:
            # self.win.iconbitmap(default=path.join(sys._MEIPASS, "./Media/favicon.ico"))
        except:
            pass
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x = (screen_width / 2) - 450
        y = (screen_height / 2) - 250
        self.win.geometry('%dx%d+%d+%d' % (900, 500, x, y))
        self.win.minsize(700, 250)
        self.win.config(menu=self.main_menu)

        self.frame_general = tk.Frame(self.win, padx=5, pady=5, border=1)
        self.frame_general.pack(fill="both", expand=False)
        self.frame_general.columnconfigure(0, weight=1)
        # self.frame2.rowconfigure(4, weight=1)

        """ Левая панель """
        self.frame_left = tk.Frame(self.frame_general, border=1)
        self.frame_left.grid(row=0, column=0, padx=5, pady=5)
        self.frame_left.columnconfigure(1, weight=1)

        self.lab4 = tk.Label(self.frame_left, text="Введите тикер акции:")
        self.lab4.grid(row=0, column=0, sticky=E)

        self.lab5 = tk.Label(self.frame_left, text="Введите период для данных:")
        self.lab5.grid(row=1, column=0, sticky=E)

        self.lab6 = tk.Label(self.frame_left, text="Введите интервал для данных:")
        self.lab6.grid(row=2, column=0, sticky=E)

        self.tik_entry = ttk.Combobox(self.frame_left, width=25, values=LIST_TIK)
        self.tik_entry.grid(row=0, column=1, sticky=W, padx=2, pady=3)
        self.tik_entry.bind("<<ComboboxSelected>>", self._set_table)
        self.ticker = TIK_DEFAULT
        self.tik_entry.insert(0, self.ticker)

        self.period_entry = ttk.Combobox(self.frame_left, width=20, values=LIST_PERIOD)
        self.period_entry.grid(row=1, column=1, sticky=W, padx=2, pady=3)
        self.period_entry.bind("<<ComboboxSelected>>", self._set_table)
        self.period = PERIOD_DEFAULT
        self.period_entry.insert(0, self.period)

        self.interval_entry = ttk.Combobox(self.frame_left, width=20, values=LIST_INTERVAL)
        self.interval_entry.grid(row=2, column=1, sticky=W, padx=2, pady=3)
        self.interval_entry.bind("<<ComboboxSelected>>", self._set_table)
        self.interval = INTERVAL_DEFAULT
        self.interval_entry.insert(0, self.interval)

        """ Правая панель """
        self.frame_right = tk.Frame(self.frame_general, border=2, relief=GROOVE)
        self.frame_right.grid(row=0, column=1, sticky=EW, pady=2)
        self.frame_right.columnconfigure(0, weight=1)

        self.lab8 = tk.Label(self.frame_right, text="Дата начала периода:", justify=CENTER)
        self.lab8.grid(row=0, column=0, sticky=E)
        self.data_start_entry = DateEntryNone(self.frame_right, borderwidth=2, date_pattern="dd-mm-y")
        self.data_start_entry.grid(row=0, column=1, padx=20, pady=3, sticky=W)
        self.data_start_entry.bind("<<DateEntrySelected>>", self._set_table)
        self.data_start = None
        self.data_start_entry.delete(0, END)

        self.lab9 = tk.Label(self.frame_right, text="Дата окончания периода:", justify=CENTER)
        self.lab9.grid(row=1, column=0, sticky=E)
        self.data_end_entry = DateEntryNone(self.frame_right, borderwidth=2, date_pattern="dd-mm-y")
        self.data_end_entry.grid(row=1, column=1, padx=20, pady=3, sticky=W)
        self.data_end_entry.bind("<<DateEntrySelected>>", self._set_table)
        self.data_end = None
        self.data_end_entry.delete(0, END)

        self.button_mean = tk.Button(self.frame_right,
                                     text=" Посчитать среднюю цену на закрытие ",
                                     command=self.button_mean_click,
                                     image=self.icon_mean,
                                     compound=LEFT)
        self.button_mean.grid(row=2, column=0, padx=5, pady=5, rowspan=1, columnspan=2)

        """ Левая панель 2 """
        self.frame_left_2 = tk.Frame(self.frame_general)
        self.frame_left_2.grid(row=1, column=0, pady=1)
        self.frame_left_2.columnconfigure(1, weight=1)

        self.lab7 = tk.Label(self.frame_left_2, text="Значение порога колебания цены для \n"
                                                     "уведомления пользователя (в %):")
        self.lab7.grid(row=0, column=0, sticky=E, padx=5)

        validate_digit_command = self.win.register(self._validate_digit_input)
        self.fluctuations_entry = tk.Entry(self.frame_left_2, width=10, validate='key',
                                           validatecommand=(validate_digit_command, '%P'))
        self.fluctuations_entry.grid(row=0, column=1, padx=2, sticky=E)
        self.fluctuations_entry.insert(0, str(FLUCTUATIONS_DEFAULT))

        """ Правая панель 2 """
        self.frame_right_2 = tk.Frame(self.frame_general, relief=GROOVE, border=2)
        self.frame_right_2.grid(row=1, column=1, sticky=EW, pady=2)
        self.frame_right_2.columnconfigure(1, weight=1)

        self.lab10 = tk.Label(self.frame_right_2, text='Стиль графиков: ')
        self.lab10.grid(row=0, column=0, sticky=E, padx=2, pady=1)
        style_list = [x for x in plt.style.available if x[0] != '_']
        self.style_entry = ttk.Combobox(self.frame_right_2, width=35, values=style_list)
        self.style_entry.grid(row=0, column=1, sticky=W, padx=1, pady=3)
        style = list(filter(lambda x: "seaborn" in x, style_list))[0]
        self.style_entry.insert(0, style)

        self.button_plot = tk.Button(self.frame_right_2,
                                     text=" Основной график ",
                                     command=self.button_plot_click,
                                     image=self.icon_chart,
                                     compound=LEFT)
        self.button_plot.grid(row=1, column=0, padx=1, pady=5)

        self.button_plot_2 = tk.Button(self.frame_right_2,
                                       text=" Дополнительный график ",
                                       command=self.button_plot_click_2,
                                       image=self.icon_chart,
                                       compound=LEFT)
        self.button_plot_2.grid(row=1, column=1, padx=1, pady=5)

        """ Средняя панель """
        self.lab11 = tk.Label(self.frame_general, text=INTER_TEXT_LINE1, foreground='blue')
        self.lab11.grid(row=7, column=0, rowspan=1, columnspan=2, sticky=W, padx=5)
        self.lab12 = tk.Label(self.frame_general, text=INTER_TEXT_LINE2+'нет выбранных столбцов')
        self.lab12.grid(row=8, column=0, rowspan=1, columnspan=2, sticky=W, padx=5)

        ticker = self.tik_entry.get().upper()
        period = self.period_entry.get()

        """Запрос данных"""
        self.stock_data = query_data(ticker, period)

        self.table = ttk.Treeview(columns=['data'] + self.stock_data.columns.values, show="headings")
        self.column_ = ['Data', *self.stock_data.columns.values]
        self._set_table(flag_start=True)
        self.scrollbar = tk.Scrollbar(self.win, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        # self.table.bind('<Button-1>', self._change_column)
        self.table.pack(side=TOP, fill=BOTH, expand=True)

    def show_info(self):
        """
        Показать информацию о приложении
        """
        mb.showinfo(title='Добро пожаловать!', message=INFO)

    def _validate_digit_input(self, new_value: str) -> bool:
        """
        Метод для валидации ввода значения в поле порога уведомления
        """
        if new_value == "":
            return True
        elif new_value.isdigit() or new_value.count('.') < 2:
            return True
        else:
            return False

    def _chk_change(self) -> bool:
        """
        Проверить были ли изменения в полях ввода, если изменения были,
        то повторить запрос с новыми данными
        :return: истина/ложь
        """
        ticker = self.tik_entry.get().upper()
        period = self.period_entry.get()
        interval = self.interval_entry.get()
        data_start = self.data_start_entry.get_date()
        if self.data_start_entry.get() == '':
            data_start = None
        data_end = self.data_end_entry.get_date()
        if self.data_end_entry.get() == '':
            data_end = None

        if (not data_start and data_end) or (data_start and not data_end):
            mb.showinfo(title='Внимание!', message='Введите даты начала и окончания периода. Либо удалите обе даты.')
            return False
        elif data_start and data_end:
            if data_start > date.today():
                data_start = date.today()
                self.data_start_entry.set_date(data_start)
            if data_end > date.today():
                data_end = date.today()
                self.data_end_entry.set_date(data_end)
            if data_start >= data_end:
                mb.showerror(title='Внимание!', message='Дата начала периода больше или равна дате окончания.')
                return False

        if (ticker != self.ticker or period != self.period or interval != self.interval
                or data_start != self.data_start or data_end != self.data_end):
            # запрос данных здесь
            self.stock_data = query_data(ticker, period=period, interval=interval,
                                         date_start=data_start, date_end=data_end)
            if type(self.stock_data) != DataFrame:
                mb.showerror(str(self.stock_data))
            if len(self.stock_data) == 0:
                mb.showinfo(title='Предупреждение!', message='Нет данных за указанный период!')
            self.ticker, self.period, self.interval = ticker, period, interval
            self.data_start, self.data_end = self.data_start_entry.get_date(), self.data_end_entry.get_date()
            return True
        return False

    def _set_table(self, *args, flag_start=False):
        """
        Метод для обновления значений таблицы, вызывается после внесения изменений
        в self.stock_data
        Также производит проверку на колебание цены закрытия за выбранный период
        :param flag_start: Флаг первоначальной загрузки таблицы при инициализации приложения.
        """
        # self.table = ttk.Treeview(columns=['data'] + self.stock_data.columns.values, show="headings")
        if flag_start or self._chk_change():
            for i in self.table.get_children():
                self.table.delete(i)

            for col in range(len(self.column_)):
                self.table.heading(col, text=self.column_[col],
                                   command=partial(self._change_column, col))
                self.table.column(col, width=20)
            for row in range(len(self.stock_data.values)):
                if self.interval in INTERVAL_NOT_TIME:
                    self.table.column(0, width=50)
                    values = ([(str(self.stock_data.index[row]).split()[0])] +
                              [round(i, 2) for i in self.stock_data.values[row]])
                else:
                    self.table.column(0, width=120)
                    values = ([self.stock_data.index[row]] +
                              [round(i, 2) for i in self.stock_data.values[row]])
                self.table.insert('', END, values=values)
            threshold = float(self.fluctuations_entry.get())
            message = dp.notify_if_strong_fluctuations(self.stock_data, threshold)
            if message:
                mb.showwarning('Предупреждение!!!', message)

    def _change_column(self, column: int):
        """
        Выбрать/удалить столбец в список выбранных
        :param column: Номер столбца
        """
        if not column:
            return
        column = self.column_[column]
        if column in self.col_list_to_inter_chart:
            self.col_list_to_inter_chart.remove(column)
        else:
            self.col_list_to_inter_chart.append(column)
        self.lab12.configure(text=INTER_TEXT_LINE2 + '  '.join(self.col_list_to_inter_chart))

    def save_csv(self, file_dlg: bool = False):
        """
        Экспортировать данные в CSV формате
        :param file_dlg: Флаг вывода диалогового окна перед сохранением файла
        """
        self._set_table()
        filename = (f"{self.ticker}_{str(self.stock_data.index[0]).split()[0]}"
                    f"-{str(self.stock_data.index[-1]).split()[0]}_data.csv")
        if file_dlg:
            filename = fd.asksaveasfilename(filetypes=[('CSV Files', '*.csv'), ('Text Files', '*.txt')],
                                            initialdir='./', initialfile=filename)
            if filename == '':
                return
        else:
            filename = None
        err = dexp.export_data_to_csv(self.stock_data, filename=filename, ticker=self.ticker)
        if not err[0]:
            mb.showerror(title='Ошибка!', message=err[1])
        else:
            mb.showinfo(title='Файл сохранен', message=f'Данные сохранены в файл: {err[1]}.')
            print(filename[:filename.rfind("\\")])
            subprocess.Popen(f'notepad {filename}')

    def button_plot_click(self):
        """
        Метод, вызываемый при нажатии на кнопку self.button_plot
        Запрос данных и печать графика
        """
        self._set_table()
        style = self.style_entry.get()
        reply = dplt.create_and_save_plot(self.stock_data, self.ticker, self.period, filename=False, style=style)
        if reply:
            mb.showinfo(message=reply, title='Инфо')

    def button_plot_click_2(self):
        """
        Метод, вызываемый при нажатии на кнопку self.button_plot_2
        Запрос данных и печать графика
        """
        self._set_table()
        style = self.style_entry.get()
        reply = dplt.create_any_plot(self.stock_data, col_list=['ATR', 'MACD_12_26_9', 'MACDs_12_26_9'],
                                     ticker=self.ticker, style=style)
        if reply:
            mb.showinfo(message=reply, title='Инфо')

    def button_plot_inter_click(self, col_list: list = None):
        """
        Метод, вызываемый при нажатии на кнопку self.button_plot_inter
        Запрос данных и вывод интерактивного графика
        """
        if col_list == []:
            mb.showinfo(title='Информация', message='Пожалуйста, выберите столбцы для визуализации.')
        self._set_table()
        reply = dplt.create_interactive_chart(self.stock_data, ticker=self.ticker, col_list=col_list)
        if reply:
            mb.showinfo(message=reply, title='Информация')

    def button_mean_click(self):
        """
        Метод, вызываемый при нажатии на кнопку button_mean
        Расчет и вывод среднего за выбранный период значения по столбцу 'Close' -
        среднее на момент закрытия торгов
        """
        self._set_table()
        mean_close = dd.calculate_and_display_average_price(self.stock_data)
        if math.isnan(mean_close):
            mb.showerror('Ошибка!', 'Не удалось определить среднюю цену закрытия.')
        else:
            mb.showinfo(message=f'Среднее цена закрытия: {mean_close:.4f}', title='Инфо')


if __name__ == "__main__":
    window = tk.Tk()
    tik = Ticker(window)
    window.mainloop()
