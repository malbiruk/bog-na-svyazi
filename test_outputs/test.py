import json
import logging
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# import sys
# sys.path.append('/home/klim/.virtualenvs/bog_na_svyazi/lib/python3.11/site-packages/')

logger = logging.getLogger('app.' + __name__)


def compute_similarity(embedding1, embedding2):
    return 1 - cosine(embedding1, embedding2)


def semantic_search(user_embedding, data):
    best_match = None
    best_score = -1

    for entry in data:
        quote_embedding = np.array(entry["embedding"])
        similarity_score = compute_similarity(user_embedding, quote_embedding)

        if similarity_score > best_score:
            best_score = similarity_score
            best_match = entry

    return best_match, best_score


def answer_with_quote(embedded_user_input: np.array, data: list) -> dict:
    best_match, best_score = semantic_search(embedded_user_input, data)

    if best_match:
        return {
            'quote': best_match['quote'],
            'from': best_match['from'],
            'score': best_score
        }
    return None


def main():
    logger.info('getting outputs... ⏳')
    with open(Path('data/verses_with_embeddings.json'),
              encoding='utf-8') as f:
        verses = json.load(f)

    with open(Path('data/quotes_with_embeddings.json'),
              encoding='utf-8') as f:
        quotes = json.load(f)

    with open('test_outputs/inputs.txt', encoding='utf-8') as f:
        inputs = f.read().strip().split('\n')

    outputs = []
    for user_input in tqdm(inputs, leave=False):
        result = {}
        result['input'] = user_input
        model = SentenceTransformer('cointegrated/rubert-tiny2')
        embedded_user_input = model.encode(user_input)
        result['quotes'] = answer_with_quote(embedded_user_input, quotes)
        result['verses'] = answer_with_quote(embedded_user_input, verses)
        outputs.append(result)

    with open('test_outputs/outputs.json', 'w', encoding='utf-8') as f:
        json.dump(outputs, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
