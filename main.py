import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Dict, Tuple

from parse import parse_toys, parse_themes

BASE_URL = 'https://www.lego.com'
THEMES_URL = f'{BASE_URL}/en-us/themes'

def get_soup(url: str, page: int = 1) -> BeautifulSoup:
    if page > 1:
        url = f'{url}?page={page}&offset=0'

    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')