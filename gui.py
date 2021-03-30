import logging
import os
from tkinter import *
from tkinter import messagebox, Tk, Button, filedialog
from config import save_config, get_config_value
from tkcalendar import Calendar
from datetime import datetime


from parsing import parser


logging.getLogger(__name__)


def parser_process(st_text, start_cal, end_cal, bet_from_text, bet_to_text):
    save_config(int(st_text.get()),
                start_cal.get_date(), end_cal.get_date(),
                int(bet_from_text.get()), int(bet_to_text.get()))
    result = parser()
    if os.path.isfile(result[1]):
        messagebox.showinfo(
            title='Парсер',
            message=('Парсинг закончен\nОбработано строк:'
                     f' {result[0]}\nФайл сохранён\n{result[1]}')
        )
    else:
        messagebox.showerror(
            title='Парсер',
            message=('Парсинг закончен\nОбработано строк:'
                     f' {result[0]}\nФайл не сохранён!!!\n{result[1]}')
        )


def show_gui():
    window = Tk()
    window.title("Закупочные процедуры:")
    window.geometry('300x700+300+300')
    window.resizable(False, False)
    # kw_pause_txt = StringVar(value=get_config_value("keyword_pause"))
    st_pause_txt = StringVar(value=get_config_value("ste_pause"))
    bet_from_txt = StringVar(value=get_config_value("bet_from"))
    bet_to_txt = StringVar(value=get_config_value("bet_to"))
    start_date = datetime.strptime(
        get_config_value("start"), "%d.%m.%Y").timetuple()
    end_date = datetime.strptime(
        get_config_value("end"), "%d.%m.%Y").timetuple()

    # Label(window, text='Пауза между \nключевыми словами (сек):').pack(fill=X)
    # kw_text = Entry(textvariable=kw_pause_txt)
    # kw_text.pack(expand=YES)
    Label(window, text='Пауза между офферами (сек):').pack(expand=YES)
    st_text = Entry(textvariable=st_pause_txt)
    st_text.pack(expand=YES)

    Label(window, text='Ставок от:').pack(expand=YES)
    bet_from_text = Entry(textvariable=bet_from_txt)
    bet_from_text.pack(expand=YES)
    Label(window, text='Ставок до:').pack(expand=YES)
    bet_to_text = Entry(textvariable=bet_to_txt)
    bet_to_text.pack(expand=YES)

    Label(window, text='C:').pack(expand=YES)
    start_cal = Calendar(window, selectmode='day',
                         foreground='red',
                         selectforeground='red',
                         year=start_date[0],
                         month=start_date[1],
                         day=start_date[2])

    start_cal.pack(expand=YES)
    Label(window, text='По:').pack(expand=YES)
    end_cal = Calendar(window, selectmode='day',
                       foreground='red',
                       selectforeground='red',
                       year=end_date[0],
                       month=end_date[1],
                       day=end_date[2])

    end_cal.pack(expand=YES)
    Button(
        window,
        text="Старт",
        command=lambda: parser_process(
            st_text, start_cal, end_cal, bet_from_text, bet_to_text),
        width=25,
        height=2
    ).pack(expand=YES)
    window.mainloop()
