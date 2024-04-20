import requests


from get_token import get_token
from armtek_config import Armtek_Config
from parse_armtek import get_parts_list

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


def get_original_parts_info(sess, config) -> list:
    """Функция для получения списка предложений оригинальных деталей"""
    content_data = sess.post(config.final_search_url,
                             headers=config.headers_search,
                             json=config.final_search_data).json()
    try:
        return get_parts_list(content_data)
    except:
        print('Ooops')


if __name__ == '__main__':
    search_params = get_search_info(session, Armtek_Config)
    Armtek_Config.final_search_data['artId'] = search_params['artId']
    Armtek_Config.final_search_data['keyzaks'] = search_params['keyzaks']
    print(get_original_parts_info(session, Armtek_Config))

