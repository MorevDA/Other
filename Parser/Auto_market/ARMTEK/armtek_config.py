from dataclasses import dataclass
from requests import Session


@dataclass
class Config:
    session = Session()
    """Класс для хранения параметров поисковых запросов"""
    headers_auth: dict
    headers_search: dict
    preliminary_search_data: dict
    final_search_data: dict
    related_parts_search_data: dict
    get_token_url: str
    final_search_url: str
    preliminary_search_url: str
    analog_url: str

    def __post_init__(self):
        """Метод для получения jwt-токена для работы с API."""
        response_result = self.session.post(self.get_token_url, headers=self.headers_auth, json={})
        token_data = response_result.json()['data']['accessToken']
        authorization_token = f'Bearer {token_data}'
        self.headers_search['authorization'] = authorization_token


Armtek_Config = Config(
    headers_auth={'accept': 'application/json, text/plain, */*',
                  'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                  'origin': 'https://armtek.ru',
                  'referer': 'https://armtek.ru/',
                  'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                  'sec-ch-ua-mobile': '?0',
                  'sec-ch-ua-platform': '"Windows"',
                  'sec-fetch-dest': 'empty',
                  'sec-fetch-mode': 'cors',
                  'sec-fetch-site': 'same-site',
                  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/123.0.0.0 Safari/537.36',
                  'x-auth-system': 'AUTH_MICROSERVICE_V1_ARMTEK_RU',
                  'x-auth-token': 'nJhNK87gJOOU6dfr',
                  'x-ca-vkorg': '4000',
                  },
    headers_search={'accept': 'application/json, text/plain, */*',
                    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
                    'content-type': 'application/json',
                    'origin': 'https://armtek.ru',
                    'referer': 'https://armtek.ru/',
                    'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                  ' Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
                    'x-app-version': '1.5.2205',
                    'x-ca-vkorg': '4000',
                    },
    preliminary_search_data={'query': '1003AU134',
                             'queryType': 1,
                             'page': 1,
                             'filters': {
                                 'text': '1003AU134',
                             },
                             'userInfo': {
                                 'VKORG': '4000',
                                 'VSTELS_LIST': [
                                     'ME86',
                                 ],
                             },
                             'ZZSIGN': 'S', },
    final_search_data={
        'artId': 49207054,
        'userInfo': {
            'VKORG': '4000',
            'VSTELS_LIST': [
                'ME86',
            ],
        },
        'limitSuggestions': False,
        'keyzaks': [
            '0000002966',
            '0000008403',
            '0000026371',
        ], },
    related_parts_search_data={
        'query': '1003AU134',
        'queryType': 1,
        'page': 1,
        'artId': 49207054,
        'typeView': 'list',
        'filters': {
            'text': '1003AU134',
            'artId': 49207054,
        },
        'userInfo': {
            'VKORG': '4000',
            'VSTELS_LIST': [
                'PE90',
            ],
        },
        'ZZSIGN': 'S', }
    ,
    get_token_url='https://restapi.armtek.ru/rest/ru/auth-microservice/v1/guest',
    final_search_url='https://restapi.armtek.ru/rest/ru/search-microservice/v1/search/all-suggestions',
    preliminary_search_url='https://restapi.armtek.ru/rest/ru/search-microservice/v1/search',
    analog_url='https://restapi.armtek.ru/rest/ru/search-microservice/v1/search/by-related')
