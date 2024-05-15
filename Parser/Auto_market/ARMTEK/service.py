from datetime import date


def get_current_time(raw_string_date: str) -> str | int:
    """Функция для вычисления времени доставки"""
    if len(raw_string_date) < 8:
        return 'n/d'
    raw_date = f'{raw_string_date[:4]}-{raw_string_date[4:6]}-{raw_string_date[6:8]}'
    current_date = date.fromisoformat(raw_date)
    delta_days = (current_date - date.today()).days
    return delta_days


def get_content(sess, url: str, headers: dict, json_data: dict) -> dict:
    """Функция для запроса данных от API методом POST"""
    content = sess.post(url, headers=headers, json=json_data).json()
    return content


def get_suggestion_list(inp_cls, content: list) -> list:
    """Функция для формирования списка предложений поставки детали с информацией о цене, количестве
    доступном для заказа, максимальной и минимальной даты поставки"""
    parts_list = [inp_cls(float(pred['PRICES1']), pred['RVALUE'], get_current_time(pred['DLVDT'])
                          , get_current_time(pred['WRNTDT'])) for pred in content]
    return parts_list


def get_analog_info(data, shop, part):
    """Функция для получения основных параметров аналогов оригинального артикула:
    фирма-производитель, каталожный номер производителя, наименование детали, внутренний артикул Armtek -
    для дальнейшего поиска ценовых предложений"""
    for part_info in data['data']['articlesData']:
        shop.analog_parts.append(part(part_info['BRAND'], part_info['PIN'], part_info['NAME'], part_info['ARTID']))
