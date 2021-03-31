# -*- coding: utf-8 -*-
# pyinstaller --hidden-import babel.numbers main.py -F -w -i Apathae-Wren-Applications.ico
import logging
from gui import show_gui


logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.INFO,
    # level=logging.DEBUG,
    filename="proc_parser.log"
)


def main():
    try:
        show_gui()
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    main()
