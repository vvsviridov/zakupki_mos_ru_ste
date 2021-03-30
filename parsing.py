import logging
import os

from json import dumps
from api import api_get
from xl import read_xl, save_xl
from config import get_config_value
from time import sleep
from urllib.parse import urlencode


logging.getLogger(__name__)


def get_url(skip=0):
    return urlencode(
        {"queryDto": dumps({
            "filter": {
                "typeIn": [1],
                "publishDateGreatEqual": f"{get_config_value('start')} 00:00:00",
                "publishDateLessEqual": f"{get_config_value('end')} 23:59:59",
                "auctionSpecificFilter": {"stateIdIn": [19000004, 19000003]},
                "needSpecificFilter": {},
                "tenderSpecificFilter": {}
            },
            "order": [{"field": "relevance", "desc": True}],
            "withCount": True,
            "take": 50,
            "skip": skip
        })}
    )


def check_bets(bets):
    min_bets = get_config_value('bet_from')
    max_bets = get_config_value('bet_to')
    if min_bets == 0 and max_bets == 0:
        return True
    if min_bets <= bets and max_bets >= bets:
        return True
    return False


def get_page(page_num):
    skip = page_num * 50
    url = 'https://old.zakupki.mos.ru/api/Cssp/Purchase/Query?' + get_url(skip)
    while True:
        response_tuple = api_get(url)
        if response_tuple[1] == 200:
            return response_tuple[0]
        else:
            sleep(get_config_value("keyword_pause"))


def page_iterations():
    result = []
    response = get_page(0)
    if response.get('count', 0) == 0:
        logging.warn('Запрос вернул 0 записей!')
        return [['Ничего не найдено!']]
    else:
        count = response.get("count", 0)
        logging.info(f'Всего {count} закупок.')
        logging.info(f'Получено {len(response.get("items", []))} закупок.')
        total_pages = count // 50 + 1
        logging.info(f'Всего страниц {total_pages}.')
        items = response.get('items', [])
        result += page_handler(items)
        for page_num in range(1, total_pages):
            response = get_page(page_num)
            items = response.get('items', [])
            result += page_handler(items)
    return result


def page_handler(items):
    result = []
    for item in items:
        item_id = item.get("auctionId", 0)
        s_date = item.get('beginDate', '01.01.1970 00:00:00').split(' ')[0]
        e_date = item.get('endDate', '01.01.1970 00:00:00')[:-3]
        bets = item.get('offerCount', 0)
        state = item.get('stateId', 'Не найдено')
        if check_bets(bets) or state == 19000003:
            result.append(
                [
                    item_id,
                    item.get('name', 'Не найдено'),
                    f'https://zakupki.mos.ru/auction/{item_id}',
                    item.get('startPrice', 'Не найдено'),
                    bets,
                    item.get('federalLawName', 'Не найдено'),
                    item.get('regionName', 'Не найдено'),
                    f'с {s_date} до {e_date}',
                    'Интеграция с РИС' if item.get(
                        'isExternalIntegration', False) else 'Работа на портале',
                ]
            )
    logging.info(f'Всего нашлось {len(result)} записей.')
    return result


def parser():
    save_to = os.path.join(
        os.getcwd(),
        'parsed_zakup_procedure.xlsx'
    )
    items = page_iterations()
    added_rows = len(items)
    saved_file = save_xl(
        save_to,
        items,
        [
            '№',
            'Наименование',
            'Ссылка',
            'Начальная цена',
            'Ставки',
            'Закон',
            'Регион',
            'Время проведения',
            'Работа/интеграция'
        ]
    )
    return added_rows, saved_file
