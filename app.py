'''
This is the main script
'''
import logging
from pathlib import Path

from preprocessing.embed_quotes import main as embed_quotes
from preprocessing.get_quotes import main as get_quotes


def initialize_logging(level=logging.INFO, folder: str = '.'):
    '''
    initialize logging (default to file 'out.log' in folder and to stdout)
    '''
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler = logging.FileHandler(f'{folder}/out.log')
    filehandler.setLevel(level)
    filehandler.setFormatter(formatter)
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(level)
    logger_.addHandler(filehandler)
    logger_.addHandler(streamhandler)
    return logger_


logger = initialize_logging()


def main():
    if not Path('data/quotes.json').exists():
        get_quotes()
    if not Path('data/quotes_with_embeddings.json').exists():
        embed_quotes()


if __name__ == '__main__':
    main()
