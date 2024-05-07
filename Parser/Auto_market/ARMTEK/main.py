import requests

from pprint import pprint


from armtek_config import Armtek_Config
from shemas import Shop, Part, Suggestion
from original_parts import get_related_parts_info, get_search_info

session = requests.Session()


Arm: Shop = Shop("armtek")

get_search_info(session, Armtek_Config, Arm, Part, Suggestion)
get_related_parts_info(session, Armtek_Config, Arm, Suggestion)

pprint(Arm)

