import data_download as dd
import data_plotting as dplt
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox as mb


def query_data(ticker, period):
    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    return stock_data


def create_win():

    def button_plot_click():
        ticker = tik_entry.get().upper()
        period = period_entry.get()
        stock_data = query_data(ticker, period)
        reply = dplt.create_and_save_plot(stock_data, ticker, period)
        mb.showinfo(message=reply, title='Инфо')

    def button_mean_click():
        ticker = tik_entry.get().upper()
        period = period_entry.get()
        stock_data = query_data(ticker, period)
        mean_rez = dplt.calculate_and_display_average_price(stock_data)
        mb.showinfo(message=f'Среднее цена закрытия: {mean_rez:.4f}', title='Инфо')

    window = tk.Tk()
    # window.configure()
    window.title('Анализ и визуализация данных об акциях')
    try:
        window.iconbitmap(default="./favicon.ico")
        # TODO Для компиляции с помощью auto-py-to-exe заменить строку выше на:
        # window.iconbitmap(default=os.path.join(sys._MEIPASS, "./favicon.ico"))
    except:
        pass
    window.geometry("800x250")
    window.minsize(650, 220)

    frame1 = tk.Frame(
        window,
        padx=10,
        pady=10,
        # relief=SUNKEN,
        # border=1
    )
    frame1.pack()

    number2 = tk.Label(frame1, text="Добро пожаловать в инструмент получения и построения графиков "
                                    "биржевых данных.", justify='center')
    number2.grid(row=1, column=1)

    number1 = tk.Label(frame1, text="Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: "
                                    "AAPL (Apple Inc), \nGOOGL (Alphabet Inc), MSFT (Microsoft Corporation), "
                                    "AMZN (Amazon.com Inc), TSLA (Tesla Inc).", justify='center')
    number1.grid(row=2, column=1)

    number3 = tk.Label(frame1, text="Общие периоды времени для данных о запасах включают: \n1д, 5д, 1мес, 3мес, 6мес, "
                                    "1г, 2г, 5г, 10л, с начала года, макс.", justify='center')
    number3.grid(row=3, column=1)

    frame2 = tk.Frame(
        window,
        padx=5,
        pady=5,
        relief=RIDGE,
        border=1
    )
    frame2.pack(fill="both", expand=True)

    # frame2.columnconfigure(0, weight=1)
    frame2.columnconfigure(1, weight=1)
    frame2.rowconfigure(0, weight=1)

    number4 = tk.Label(frame2, text="Введите тикер акции (например, «AAPL» для Apple Inc):", justify='right')
    number4.grid(row=0, column=0, sticky=E)

    number5 = tk.Label(frame2, text="Введите период для данных (например, '1mo' для одного месяца):", justify='right')
    number5.grid(row=1, column=0, sticky=E)

    tik_entry = tk.Entry(frame2, width=50)
    tik_entry.grid(row=0, column=1, sticky=W)
    txt = 'GOOGL'
    tik_entry.insert(0, txt)

    list_period = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    period_entry = ttk.Combobox(frame2, width=50, values=list_period)
    period_entry.grid(row=1, column=1, sticky=W)
    txt = '1mo'
    period_entry.insert(0, txt)

    button_plot = tk.Button(frame2, text="Отправить запрос", width=20, height=2,
                            command=button_plot_click)
    button_plot.grid(row=2, column=0)

    button_mean = tk.Button(frame2, text="Посчитать среднюю цену по столбцу", width=30, height=2,
                            command=button_mean_click)
    button_mean.grid(row=2, column=1, padx=5, pady=5)

    window.mainloop()


def main():
    create_win()


if __name__ == "__main__":
    main()
