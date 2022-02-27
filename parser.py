from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Optional


def parse_toy_info(info_list: List[str]) -> Dict[str, Optional[str]]:
    info = {'age': None, 'pieces': None, 'rating': None}

    for item in info_list:
        if '+' in item:
            info['age'] = item
        elif '.' in item:
            info['rating'] = item
        else:
            info['pieces'] = item
    return info
