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

if __name__ == '__main__':
    themes_soup = get_soup(THEMES_URL)
    themes = parse_themes(BASE_URL, themes_soup)
    save_csv(themes, 'themes.csv')

    collection_name = 'marvel'
    collection_url = f'{THEMES_URL}/{collection_name}'
    soup = get_soup(collection_url)
    _, pages = get_total_pages(soup)

    all_toys = []
    for page in range(1, pages + 1):
        page_soup = get_soup(collection_url, page=page)
        toys = parse_toys(page_soup, collection=collection_name.capitalize())
        all_toys.extend(toys)

    save_csv(all_toys, 'toys_data.csv')