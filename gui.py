import logging
import os
from tkinter import *
from tkinter import messagebox, Tk, Button, filedialog
from config import save_config, get_config_value


from parsing import parser


logging.getLogger(__name__)


def parser_process(kw_text, st_text):
    save_config(int(kw_text.get()), int(st_text.get()))
    filename = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx")])
    logging.info(f'Выбран файл: {filename}.')
    if os.path.isfile(filename):
        result = parser(filename)
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
    window.title("Укажите Excel файл:")
    window.geometry('300x400+300+300')
    window.resizable(False, False)
    kw_pause_txt = StringVar(value=get_config_value("keyword_pause"))
    st_pause_txt = StringVar(value=get_config_value("ste_pause"))
    Label(window, text='Пауза между \nключевыми словами (сек):').place(
        relx=0.1, rely=0.13)
    kw_text = Entry(textvariable=kw_pause_txt)
    kw_text.place(
        relx=0.1, rely=0.23)
    Label(window, text='Пауза между офферами (сек):').place(
        relx=0.1, rely=0.33)
    st_text = Entry(textvariable=st_pause_txt)
    st_text.place(
        relx=0.1, rely=0.43)
    Button(
        window,
        text="Старт",
        command=lambda: parser_process(kw_text, st_text),
        width=25,
        height=2
    ).place(
        relx=0.1, rely=0.53)
    window.mainloop()
