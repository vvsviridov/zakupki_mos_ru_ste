import logging
import os
from tkinter import messagebox, Tk, Button, filedialog

from parsing import parser


logging.getLogger(__name__)


def parser_process():
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
    start_btn = Button(
        window,
        text="Старт",
        command=lambda: parser_process(),
        width=25,
        height=2
    )
    start_btn.place(relx=0.19, rely=0.4)
    window.mainloop()
