import json
import logging
from pathlib import Path

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

logger = logging.getLogger('app.' + __name__)


def main(inp: Path = Path('data/verses.json'),
         out: Path = Path('data/verses_with_embeddings.json'),
         model_name: str = 'cointegrated/rubert-tiny2'):
    logger.info('embedding quotes... ⚗')
    model = SentenceTransformer(model_name)

    with open(inp, encoding='utf-8') as f:
        data = json.load(f)

    for entry in tqdm(data, leave=False):
        entry['embedding'] = [float(i) for i in model.encode(entry['quote'])]

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
