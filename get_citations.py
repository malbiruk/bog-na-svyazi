'''
This script is used to retrieve citations from citaty.info and save them to drive.
'''
import json
import logging

import httpx
from bs4 import BeautifulSoup
from tqdm import tqdm

logger = logging.getLogger(__name__)


def get_soup(url: str) -> BeautifulSoup:
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) '
                   'Gecko/20100101 Firefox/124.0'}
        with httpx.Client(timeout=5, headers=headers, follow_redirects=True) as client:
            response = client.get(url).raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error(f'failed to fetch the website 😞\n{url}\n%s', e)
        return None


def extract_citations_from_soup(soup: BeautifulSoup) -> list[dict[str, str]]:
    quotes = []
    for quote_div in soup.find_all('div', class_='node__content'):
        citation = quote_div.find('div', class_='field-name-body')
        citation = ' '.join(citation.text.strip().split())

        description = quote_div.find('div', class_='field-name-field-description')
        if description:
            description = (' '.join(description.text.strip().split())
                           .removeprefix('Пояснение к цитате: '))

        quotes.append({
            'quote': citation,
            'from': description,
        })
    return quotes


def main():
    quotes = []
    for i in tqdm(range(26)):
        soup = get_soup(f'https://citaty.info/book/bibliya-novyi-zavet?page={i}')
        quotes.extend(extract_citations_from_soup(soup))

    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
