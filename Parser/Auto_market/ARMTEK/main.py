import requests

from pprint import pprint

from armtek_config import Armtek_Config
from shemas import Shop, Part, Suggestion
from original_parts import get_original_parts
from analog_parts import get_analog_parts

session = requests.Session()

Arm: Shop = Shop("armtek")
Armtek_Config.preliminary_search_data['query'] = Armtek_Config.preliminary_search_data['filters']['text'] = \
    Armtek_Config.related_parts_search_data['query'] = Armtek_Config.related_parts_search_data['filters'][
    'text'] = input(
    "Введите парт-номер детали для поиска:_")

get_original_parts(session, Armtek_Config, Arm, Part, Suggestion)
get_analog_parts(session, Armtek_Config, Arm, Part, Suggestion)
pprint(Arm)
