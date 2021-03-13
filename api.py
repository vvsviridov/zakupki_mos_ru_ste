import logging
import requests


logging.getLogger(__name__)


def api_post(url, query):
    try:
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '474',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://old.zakupki.mos.ru',
            'referer': 'https://old.zakupki.mos.ru/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)\
                 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
                     Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        logging.info('===> post JSON <===')
        logging.info(query)
        response = requests.post(url, headers=headers, json=query)
        logging.debug(response.json())
        logging.info(f'Сервер вернул код {response.status_code}.')
        return response.json(), response.status_code
    except Exception as e:
        logging.critical(e)


# def api_get(url):
#     try:
#         headers = {
#             'accept': '*/*',
#             'accept-encoding': 'gzip, deflate, br',
#             'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#             'origin': 'https://old.zakupki.mos.ru',
#             'referer': 'https://old.zakupki.mos.ru/',
#             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)\
#                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 \
#                      Safari/537.36',
#         }
#         logging.info('===> get JSON <===')
#         logging.info(url)
#         response = requests.get(url, headers=headers)
#         logging.debug(response.json())
#         logging.info(f'Сервер вернул код {response.status_code}.')
#         return response.json(), response.status_code
#     except Exception as e:
#         logging.critical(e)
