import logging
import os
from api import api_post
from xl import read_xl, save_xl
from config import get_config_value
from time import sleep
from tkinter import messagebox


logging.getLogger(__name__)


def get_ctes(keyword, count):
    logging.info(f'Ключевое слово: {keyword}')
    url_sku = 'https://old.zakupki.mos.ru/api/Cssp/Sku/PostQuery'
    url_offer = 'https://old.zakupki.mos.ru/api/Cssp/Offer/PostQuery'
    result = []
    output = []
    query_cte = {
        "filter": {
            "nameLike": None,
            "costPerUnitGreatEqual": None,
            "costPerUnitLessEqual": None,
            "regionPaths": [],
            "okpdPaths": [],
            "vendorCodeLike": None,
            "offersCountGreatEqual": None,
            "offersCountLessEqual": None,
            "keyword": keyword,
            "partNumberLike": None,
            "productionPaths": [],
            "productionDirectoryPaths": [],
            "characteristicFilter": [],
            "vendorIdIn": None,
            "hasOffers": None,
            "state": "actual",
            "entityStateIn": [1]
        },
        "take": count,
        "skip": 0,
        "order": [{"field": "relevance", "desc": True}],
        "withCount": True
    }
    query_offers = {
        "filter": {
            "offerStateIdIn": [2],
            "skuIdIn": [18800324],
            "onlyMyOffer": False
        },
        "order": [{"field": "costPerUnit", "desc": False}],
        "withCount": True,
        "take": 10,
        "skip": 0
    }
    while True:
        response_tuple = api_post(url_sku, query_cte)
        if response_tuple[1] == 200:
            response = response_tuple[0]
            break
        else:
            sleep(get_config_value("keyword_pause"))
    if response.get('count', 0) == 0:
        logging.warn('Пост-запрос вернул 0 записей!')
        return [[keyword, 'По ключевому слову ничего не найдено!']]
    else:
        logging.info(f'Всего {response.get("count", 0)} СТЕ.')
        logging.info(f'Получено {len(response.get("items", []))} СТЕ.')
        for item in response.get('items', []):
            item_id = item.get("id", 0)
            item_offer_count = item.get("offersCount", 0)
            offers = []
            if item_offer_count != 0:
                query_offers['filter']['skuIdIn'] = [item_id]
                query_offers['take'] = item_offer_count
                while True:
                    offers_resp_tuple = api_post(url_offer, query_offers)
                    if offers_resp_tuple[1] == 200:
                        offers_resp = offers_resp_tuple[0]
                        break
                    else:
                        sleep(get_config_value("ste_pause"))
                for offer in offers_resp.get('items', []):
                    offers.append(
                        [
                            offer.get('supplierName', 'Не найдено'),
                            offer.get('supplierInn', 'Не найдено'),
                            offer.get('costPerUnit', 'Не найдено'),
                            ', '.join(offer.get('regionNames', 'Не найдено')),
                        ]
                    )
            result.append(
                [
                    keyword,
                    item.get('name', 'Не найдено'),
                    item.get('id', 'Не найдено'),
                    item.get('offersCount', 'Не найдено'),
                    offers,
                    (f"{item.get('productionCode', 'Не найдено') or ''} - "
                     f" {item.get('productionDirectoryName', 'Не найдено').upper()}"),
                ]
            )
        logging.info(f'Всего нашлось {len(result)} записей.')
        output = merge_output(result)
        return output


def merge_output(items):
    result = []
    for item in items:
        if len(item[4]) == 0:
            result.append(item[:4] + ['']*4 + [item[5]])
        if len(item[4]) >= 1:
            result.append(item[:4] + item[4][0] + [item[5]])
        if len(item[4]) > 1:
            for offer in item[4][1:]:
                result.append(['']*4 + offer + [''])
    return result


def parser(filename):
    save_to = os.path.join(
        os.getcwd(),
        f'parsed_{os.path.split(filename)[-1]}'
    )
    items = []
    rows = read_xl(filename)
    for row in rows:
        items += get_ctes(*row)
    added_rows = len(items)
    saved_file = save_xl(
        save_to,
        items,
        [
            'Ключевое слово',
            'Наименование',
            'ID СТЕ',
            'Количество предложений',
            'Поставщик',
            'ИНН',
            'Цена',
            'Регион поставки',
            'КПГЗ'
        ]
    )
    return added_rows, saved_file
