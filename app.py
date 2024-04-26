'''
This is the main script
'''
from pathlib import Path

from config import initialize_logging
from preprocessing.embed_quotes import main as embed_quotes
from preprocessing.parse_books import main as parse_books

logger = initialize_logging()


def generate_data_files():
    if not Path('data/verses.json').exists():
        parse_books()
    if not Path('data/verses_with_embeddings.json').exists():
        embed_quotes('data/verses.json', 'data/verses_with_embeddings.json')


def main():
    generate_data_files()


if __name__ == '__main__':
    main()
