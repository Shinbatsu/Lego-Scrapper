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

def save_csv(data: List[Dict], filename: str) -> None:
    if not data:
        return

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
def get_total_pages(soup: BeautifulSoup) -> Tuple[int, int]:
    total_items = int(soup.select_one('span[data-value]')['data-value'])
    pages = (total_items + 17) // 18
    return total_items, pages
