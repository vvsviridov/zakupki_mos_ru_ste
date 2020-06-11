import logging
import os
from api import api_post, api_get
from xl import read_xl, save_xl


logging.getLogger(__name__)


def get_ctes(keyword, count):
    url_post = 'https://old.zakupki.mos.ru/api/Cssp/Sku/PostQuery'
    result = []
    query = {
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
        "take": f"{count}",
        "skip": 0,
        "order": [{"field": "relevance", "desc": True}],
        "withCount": True
    }
    response = api_post(url_post, query)
    if response.get('count', 0) == 0:
        logging.warn('Пост-запрос вернул 0 записей!')
        return ['По ключевому слову ничего не найдено!']
    else:
        for item in response.get('items', []):
            item_id = item.get("id", 0)
            url_get = ('https://old.zakupki.mos.ru'
                       f'/api/Cssp/Sku/GetEntity?id={item_id}')
            item_data = api_get(url_get)
            logging.info(
                (f'Для id {item_id} get item data вернул'
                 f' {item_data.get("id", "id не найден!")}'))
            result.append(
                [
                    keyword,
                    item.get('name', 'Не найдено'),
                    item.get('id', 'Не найдено'),
                    item.get('offersCount', 'Не найдено'),
                    item_data.get('minPrice', 'Не найдено'),
                    item_data.get('maxPrice', 'Не найдено'),
                    item_data.get('medianPrice', 'Не найдено'),
                    (f"{item.get('productionCode', 'Не найдено')} - "
                     f" {item.get('productionDirectoryName', 'Не найдено').upper()}"),
                ]
            )
        logging.info(f'Всего нашлось {len(result)} записей.')
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
            'Минимальная цена',
            'Максимальная цена',
            'Средняя цена',
            'КПГЗ'
        ]
    )
    return added_rows, saved_file
