import requests
from pprint import pprint
import json

from get_token import get_token

from armtek_config import Armtek_Config

session = requests.Session()

Armtek_Config.headers_search['authorization'] = get_token(session, Armtek_Config)


def get_search_info(sess, config) -> dict:
    """Функция для получения характеристик поиска от API Ar"""
    content = sess.post(config.preliminary_search_url,
                        headers=config.headers_search,
                        json=config.preliminary_search_data).json()
    search_info = {}
    parts_info = content["data"]  # ["data"]['articlesData'])
    search_info['cacheKey'] = parts_info['cacheKey']
    suggestion = parts_info['articlesData'][0]['SUGGESTIONS']
    search_info['keyzaks'] = [i['KEYZAK'] for i in suggestion]
    search_info['artId'] = list(set(i['ARTID'] for i in suggestion))[0]
    return search_info


# Armtek_Config


def get_original_parts_info(sess, config):
    content = sess.post(config.final_search_url,
                        headers=config.headers_search,
                        json=config.final_search_data).json()
    try:
        with open('armtek_proba', 'w', encoding='utf-8') as file:
            json.dump(content, file)
        print('mission compliant')
    except:
        print('Ooops')


if __name__ == '__main__':
    search_params = get_search_info(session, Armtek_Config)
    Armtek_Config.final_search_data['artId'] = search_params['artId']
    Armtek_Config.final_search_data['keyzaks'] = search_params['keyzaks']
    get_original_parts_info(session, Armtek_Config)
    # print(Armtek_Config)

