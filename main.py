# -*- coding: utf-8 -*-
# pyinstaller main.py -F -w -i Apathae-Wren-Applications.ico
import logging
from gui import show_gui


logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.INFO,
    # level=logging.DEBUG,
    filename="cte_parser.log"
)


def main():
    show_gui()


if __name__ == "__main__":
    main()
