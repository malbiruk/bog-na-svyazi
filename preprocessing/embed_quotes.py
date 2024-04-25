import json
import logging
from pathlib import Path

from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

logger = logging.getLogger('__main__')


def main(inp: Path = Path('data/quotes.json'),
         out: Path = Path('data/quotes_with_embeddings.json'),
         model_name: str = 'cointegrated/rubert-tiny2'):
    model = SentenceTransformer(model_name)

    with open(inp, encoding='utf-8') as f:
        data = json.load(f)

    logger.info('embedding quotes... ⚗')
    for entry in tqdm(data, leave=False):
        entry['embedding'] = [i.tolist() for i in model.encode(
            sent_tokenize(entry['quote'].lower()))]

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main(inp=Path('../data/quotes.json'),
         out=Path('../data/quotes_with_embeddings.json'))
