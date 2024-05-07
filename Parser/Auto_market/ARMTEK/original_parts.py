from service import get_suggestion_list, get_content
from copy import deepcopy


def get_search_info(sess, config, shop, part, suggestion) -> None:
    """Функция для получения характеристик поиска и характеристик оригинальной детали
     от API Armtek"""
    content = get_content(sess, config.preliminary_search_url,config.headers_search,
                          config.preliminary_search_data)
    parts_data = content["data"]['articlesData'][0]
    suggestions = parts_data['SUGGESTIONS']
    art_id = list(set(i['ARTID'] for i in suggestions))[0]
    keyzaks = [i['KEYZAK'] for i in suggestions]
    shop.original_parts = part(parts_data['BRAND'], parts_data['PIN'], parts_data['NAME'], art_id, keyzaks=keyzaks)
    parts_list = get_suggestion_list(suggestion, suggestions)
    shop.original_parts.suggestions = parts_list


def get_related_parts_info(sess, config, shop, suggestion) -> None:
    """Функция для получения списка предложений оригинальных деталей"""
    final_data = deepcopy(config.final_search_data)
    final_data['artId'] = shop.original_parts.artid
    final_data['keyzaks'] = shop.original_parts.keyzaks
    content_data = get_content(sess, config.final_search_url, config.headers_search,
                               config.final_search_data)['data']
    parts_list = get_suggestion_list(suggestion, content_data)
    shop.original_parts.suggestions.extend(parts_list)


if __name__ == '__main__':
    from armtek_config import Armtek_Config
    from requests import Session

    from shemas import Shop, Part, Suggestion
    from pprint import pprint

    session = Session()
    Arm: Shop = Shop("armtek")

    get_search_info(session, Armtek_Config, Arm, Part, Suggestion)
    get_related_parts_info(session, Armtek_Config, Arm, Suggestion)

    pprint(Arm)
