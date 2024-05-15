from copy import deepcopy

from service import get_content, get_analog_info, get_suggestion_list


def get_analog_list(class_config, sess, shop, part):
    """Функция для получения основной информации о возможных аналогах парт-номера с одной страницы сайта"""
    class_config.headers_search['authority'] = 'restapi.armtek.ru'
    content = get_content(sess, class_config.preliminary_search_url, class_config.headers_search,
                          class_config.related_parts_search_data)
    get_analog_info(content, shop, part)


def get_pages_count(class_config, sess) -> int:
    """Функция для получения количества страниц с заменителями оригинального артикула"""
    response = get_content(sess, class_config.preliminary_search_url, class_config.headers_search,
                           class_config.related_parts_search_data)

    return response['data']['pagination']['pageCount']


def get_all_analog_parts_product(sess, config, shop, part):
    """Функция для получения основной информации о возможных аналогах парт-номера"""
    pages_count = get_pages_count(config, sess)
    for page_number in range(1, pages_count + 1):
        conf = deepcopy(config)
        conf.related_parts_search_data['page'] = page_number
        get_analog_list(conf, sess, shop, part)


def get_analog_parts_suggestions(sess, config, shop, suggestion) -> None:
    """Функция для получения информации о цене и сроках поставки всех аналогов парт-номера."""
    for part in shop.analog_parts:
        json_data = deepcopy(config.final_search_data)
        json_data['artId'] = part.artid
        content = get_content(sess, config.final_search_url, config.headers_search, json_data)['data']
        suggestions_list = get_suggestion_list(suggestion, content)
        part.suggestions = suggestions_list


def get_analog_parts(sess, config, shop, parts, suggestion):
    """Функция для получения полной информации о возможных аналогов основного парт-номера."""
    get_all_analog_parts_product(sess, config, shop, parts)
    get_analog_parts_suggestions(sess, config, shop, suggestion)


if __name__ == '__main__':
    import requests
    from pprint import pprint
    from shemas import Shop, Part, Suggestion
    from armtek_config import Armtek_Config

    requests_session = requests.Session()

    Arm = Shop("Armtek")

    get_analog_parts(requests_session, Armtek_Config, Arm, Part, Suggestion)

    pprint(Arm)
