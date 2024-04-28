import json
import logging
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

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


def answer_with_quote(user_input: str, data: list) -> dict:
    model = SentenceTransformer('cointegrated/rubert-tiny2')
    embedded_user_input = model.encode(user_input)
    best_match, best_score = semantic_search(embedded_user_input, data)

    if best_match:
        return {
            'quote': '"' + best_match['quote'] + '"',
            'from': best_match['from'],
            'score': best_score
        }
    return None
