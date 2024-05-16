from service import get_suggestion_list, get_content
from copy import deepcopy


def get_search_info(sess, config, shop, part, suggestion) -> None:
    """Функция для получения от API Armtek с основными предложениями по парт-номеру
    детали, а также внутреннего актикула Armtek для дальнейшего поиска деталей с таким
    же парт-номером и аналогов"""
    content = get_content(sess, config.preliminary_search_url, config.headers_search,
                          config.preliminary_search_data)
    parts_data = content["data"]['articlesData'][0]
    # suggestions = parts_data['SUGGESTIONS']
    art_id = parts_data['ARTID']
    shop.original_parts = part(parts_data['BRAND'], parts_data['PIN'], parts_data['NAME'], art_id)


def get_related_parts_info(sess, config, shop, suggestion) -> None:
    """Функция для получения полного списка предложений по искомому парт-номеру."""
    final_data = deepcopy(config.final_search_data)
    final_data['artId'] = shop.original_parts.artid
    content_data = get_content(sess, config.final_search_url, config.headers_search,
                               config.final_search_data)['data']
    parts_list = get_suggestion_list(suggestion, content_data)
    shop.original_parts.suggestions.extend(parts_list)


def get_original_parts(sess, config, shop, part, suggestion ):
    get_search_info(sess, config, shop, part, suggestion)
    get_related_parts_info(sess, config, shop, suggestion)


if __name__ == '__main__':
    from armtek_config import Armtek_Config
    from requests import Session

    from shemas import Shop, Part, Suggestion
    from pprint import pprint

    session = Session()
    Arm: Shop = Shop("armtek")

    get_original_parts(session, Armtek_Config, Arm, Part, Suggestion)

    pprint(Arm)
