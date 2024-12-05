import math
import subprocess
from functools import partial
from PIL import Image, ImageTk

import data_download as dd
import data_plotting as dplt
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from constants import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from pandas import DataFrame


def image_to_icon(file: str, min_x=20, min_y=20) -> ImageTk.PhotoImage:
    """
    Изменение размера картинки для иконки.
    :param file: Имя файла.
    :param min_x: Размер по горизонтали.
    :param min_y: Размер по вертикали.
    :return: Объект ImageTk.PhotoImage.
    """
    im = Image.open(file)
    im = im.resize((min_x, min_y))
    return ImageTk.PhotoImage(im)


def query_data(ticker: str, period: str) -> DataFrame:
    """
    Запрос данных с Yahoo Finance с использованием фреймворка yfinance
    :param ticker: Название тикета, может принимать значения ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    :param period: Период предоставления данных:
                   ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    :return: Объект класса DataFrame (pandas)
    """
    # Получить данных
    stock_data = dd.fetch_stock_data(ticker, period)

    # Добавить скользящее среднее значение к данным
    stock_data = dd.add_moving_average(stock_data)

    # Добавить дополнительные технические индикаторы: RSI и MACD
    stock_data = dd.add_rsi_macd(stock_data)

    return stock_data


class Ticker:
    """
    Класс GUI со всеми элементами и методами окна
    """
    def __init__(self, win: tk.Tk):
        self.win = win
        self.win.option_add("*tearOff", FALSE)

        self.icon_save = image_to_icon(ICON_SAVE)
        self.file_menu = tk.Menu()
        self.file_menu.add_command(label=' Сохранить в CSV',
                                   command=self.save_csv,
                                   image=self.icon_save,
                                   compound=LEFT)
        self.file_menu.add_command(label=' Сохранить как...',
                                   command=partial(self.save_csv, True),
                                   image=self.icon_save,
                                   compound=LEFT)

        self.main_menu = tk.Menu()
        self.main_menu.add_cascade(label='Файл', menu=self.file_menu)
        self.main_menu.add_command(label='О программе', command=self.show_info)
        # self.win.bind_all('<F1>', self.show_info)

        self.win.title('Анализ и визуализация данных об акциях')
        try:
            self.win.iconbitmap(default="./Media/favicon.ico")
            # TODO Для компиляции с помощью auto-py-to-exe заменить строку выше на:
            # self.win.iconbitmap(default=os.path.join(sys._MEIPASS, "./Media/favicon.ico"))
        except:
            pass
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x = (screen_width / 2) - 400
        y = (screen_height / 2) - 200
        self.win.geometry('%dx%d+%d+%d' % (800, 400, x, y))
        self.win.minsize(700, 250)
        self.win.config(menu=self.main_menu)

        self.frame2 = tk.Frame(self.win, padx=5, pady=5, relief=RIDGE, border=1)
        self.frame2.pack(fill="both", expand=False)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        # self.frame2.rowconfigure(4, weight=1)

        self.lab4 = tk.Label(self.frame2, text="Введите тикер акции (например, «AAPL» для Apple Inc):", justify='right')
        self.lab4.grid(row=0, column=0, sticky=E)

        self.lab5 = tk.Label(self.frame2, text="Введите период для данных:", justify='right')
        self.lab5.grid(row=1, column=0, sticky=E)

        self.lab5 = tk.Label(self.frame2, text="Введите значение порога колебания цены,\n"
                                               "при котором следует уведомлять пользователя (в %):", justify='right')
        self.lab5.grid(row=2, column=0, sticky=E)

        self.tik_entry = ttk.Combobox(self.frame2, width=50, values=LIST_TIK)
        self.tik_entry.grid(row=0, column=1, sticky=W, padx=2, pady=1)
        self.tik_entry.insert(0, LIST_TIK[1])

        self.period_entry = ttk.Combobox(self.frame2, width=50, values=LIST_PERIOD)
        self.period_entry.grid(row=1, column=1, sticky=W, padx=2, pady=1)
        self.period_entry.insert(0, LIST_PERIOD[3])

        validate_digit_command = self.win.register(self.__validate_digit_input)
        self.fluctuations_entry = tk.Entry(self.frame2, width=20, validate='key',
                                           validatecommand=(validate_digit_command, '%P'))
        self.fluctuations_entry.grid(row=2, column=1, sticky=W, padx=2)
        self.fluctuations_entry.insert(0, str(FLUCTUATIONS_DEFAULT))

        self.icon_chart = image_to_icon(ICON_CHART)
        self.button_plot = tk.Button(self.frame2,
                                     text=" Построить график ", #width=110, height=25,
                                     command=self.button_plot_click,
                                     image=self.icon_chart,
                                     compound=LEFT)
        self.button_plot.grid(row=3, column=0, padx=5, pady=5)
        # self.button_plot.bind('<Return>', self.button_plot_click)

        self.icon_mean = image_to_icon(ICON_CALC)
        self.button_mean = tk.Button(self.frame2,
                                     text=" Посчитать среднюю цену на закрытие ", #width=35, height=2,
                                     command=self.button_mean_click,
                                     image=self.icon_mean,
                                     compound=LEFT)
        self.button_mean.grid(row=3, column=1, padx=5, pady=5)

        ticker = self.tik_entry.get().upper()
        period = self.period_entry.get()
        self.stock_data = query_data(ticker, period)

        self.table = ttk.Treeview(columns=['data'] + self.stock_data.columns.values, show="headings")
        self.column_ = ['Data', *self.stock_data.columns.values]
        self.__set_table()
        self.scrollbar = tk.Scrollbar(self.win, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.table.pack(side=TOP, fill=BOTH, expand=True)
        # self.win.after_idle(self.show_info)

    def show_info(self):
        """
        Показать информацию о приложении
        """
        mb.showinfo(title='Добро пожаловать!', message=INFO)

    def __validate_digit_input(self, new_value: str) -> bool:
        """
        Метод для валидации ввода значения в поле порога уведомления
        """
        if new_value == "":
            return True
        elif new_value.isdigit() or new_value.count('.') < 2:
            return True
        else:
            return False

    def __set_table(self):
        """
        Метод для обновления значений таблицы, вызывается после внесения изменений
        в self.stock_data
        Также производит проверку на колебание цены закрытия за выбранный период
        """
        # self.table = ttk.Treeview(columns=['data'] + self.stock_data.columns.values, show="headings")
        for i in self.table.get_children():
            self.table.delete(i)

        for col in range(len(self.column_)):
            self.table.heading(col, text=self.column_[col])
            self.table.column(col, width=20)
        for row in range(len(self.stock_data.values)):
            self.table.insert('', END, values=[(str(self.stock_data.index[row]).split()[0])] +
                                              [round(i, 2) for i in self.stock_data.values[row]])
        threshold = float(self.fluctuations_entry.get())
        message = dplt.notify_if_strong_fluctuations(self.stock_data, threshold)
        if message:
            mb.showwarning('Предупреждение!!!', message)

    def save_csv(self, file_dlg: bool = False):
        """
        Экспортировать данные в CSV формате
        :param file_dlg: Флаг вывода диалогового окна перед сохранением файла
        """
        ticker = self.tik_entry.get().upper()
        period = self.period_entry.get()
        self.stock_data = query_data(ticker, period)
        self.__set_table()
        filename = (f"{ticker}_{str(self.stock_data.index[0]).split()[0]}"
                    f"-{str(self.stock_data.index[-1]).split()[0]}_data.csv")
        if file_dlg:
            filename = fd.asksaveasfilename(filetypes=[('CSV Files', '*.csv'), ('Text Files', '*.txt')],
                                            initialdir='./', initialfile=filename)
            if filename == '':
                return
        else:
            filename = None
        err = dplt.export_data_to_csv(self.stock_data, filename=filename, ticker=ticker)
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
        ticker = self.tik_entry.get().upper()
        period = self.period_entry.get()
        self.stock_data = query_data(ticker, period)
        reply = dplt.create_and_save_plot(self.stock_data, ticker, period, filename=False)
        if reply:
            mb.showinfo(message=reply, title='Инфо')
        self.__set_table()

    def button_mean_click(self):
        """
        Метод, вызываемый при нажатии на кнопку button_mean
        Расчет и вывод среднего за выбранный период значения по столбцу 'Close' -
        среднее на момент закрытия торгов
        """
        ticker = self.tik_entry.get().upper()
        period = self.period_entry.get()
        self.stock_data = query_data(ticker, period)
        mean_close = dplt.calculate_and_display_average_price(self.stock_data)
        if math.isnan(mean_close):
            mb.showerror('Ошибка!', 'Не удалось определить среднюю цену закрытия.')
        else:
            mb.showinfo(message=f'Среднее цена закрытия: {mean_close:.4f}', title='Инфо')
        self.__set_table()


if __name__ == "__main__":
    window = tk.Tk()
    tik = Ticker(window)
    # tik.win.after_idle(tik.show_info)
    window.mainloop()
