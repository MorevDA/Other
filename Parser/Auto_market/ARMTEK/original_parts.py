from service import get_suggestion_list


def get_search_info(sess, config, shop, part, suggestion) -> None:
    """Функция для получения характеристик поиска и характеристик оригинальной детали
     от API Armtek"""
    content = sess.post(config.preliminary_search_url,
                        headers=config.headers_search,
                        json=config.preliminary_search_data).json()
    parts_info = content["data"]
    parts_data = parts_info['articlesData'][0]
    suggestions = parts_data['SUGGESTIONS']
    art_id = list(set(i['ARTID'] for i in suggestions))[0]
    config.final_search_data['keyzaks'] = [i['KEYZAK'] for i in suggestions]
    config.final_search_data['artId'] = art_id
    shop.original_parts = part(parts_data['BRAND'], parts_data['PIN'], parts_data['NAME'], art_id)
    parts_list = get_suggestion_list(suggestion, suggestions)
    shop.original_parts.suggestions = parts_list


def get_related_parts_info(sess, config, shop, suggestion) -> None:
    """Функция для получения списка предложений оригинальных деталей"""
    content_data = sess.post(config.final_search_url,
                             headers=config.headers_search,
                             json=config.final_search_data).json()['data']
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
