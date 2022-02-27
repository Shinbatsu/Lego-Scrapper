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


def parse_price(toy: BeautifulSoup) -> Tuple[str, Optional[str]]:
    price_text = toy.find('div', {'data-test': 'product-leaf-price-row'}).text
    price = toy.find('span', {'data-test': 'product-leaf-price'}).text

    if '%' in price_text:
        discount = toy.find('span', {'data-test': 'product-leaf-discounted-price'}).text
        return price, discount
    return price, None


def parse_toys(soup: BeautifulSoup, collection: str = 'Marvel') -> List[Dict[str, str]]:
    toys = soup.find_all('li', {'data-test': 'product-item'})
    result = []

    for toy in toys:
        name = toy.find('h3').text.strip()

        attr_tags = toy.find('div', {'data-test': 'product-leaf-attributes-row'}).find_all('span')
        attributes = [tag.text.strip() for tag in attr_tags]
        toy_info = parse_toy_info(attributes)

        price, discount = parse_price(toy)

        result.append({
            'name': name,
            'collection': collection,
            'age': toy_info['age'],
            'pieces': toy_info['pieces'],
            'rating': toy_info['rating'],
            'price': price,
            'discount': discount or '0'
        })

    return result
