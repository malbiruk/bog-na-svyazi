import logging
import random

import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

logger = logging.getLogger('app.' + __name__)


def compute_similarity(embedding1, embedding2):
    return 1 - cosine(embedding1, embedding2)


def semantic_search(user_embedding, data, threshold: float, top_n: int) -> tuple:
    top_matches = []

    for entry in data:
        quote_embedding = np.array(entry["embedding"])
        similarity_score = compute_similarity(user_embedding, quote_embedding)

        if similarity_score > threshold:
            top_matches.append((entry, similarity_score))

    if not top_matches:
        return None, None

    top_matches.sort(key=lambda x: x[1], reverse=True)
    selected_match = random.choice(top_matches[:top_n])
    logger.debug([(i[0]['quote'], i[1]) for i in top_matches[:top_n]])

    return selected_match[0], selected_match[1]


def answer_with_quote(user_input: str, data: list,
                      threshold: float = 0.6, top_n: int = 20) -> dict:
    model = SentenceTransformer('cointegrated/rubert-tiny2')
    embedded_user_input = model.encode(user_input)
    best_match, best_score = semantic_search(embedded_user_input, data, threshold, top_n)

    if best_match:
        return {
            'quote': '"' + best_match['quote'] + '"',
            'from': best_match['from'],
            'score': best_score
        }
    best_match, best_score = semantic_search(embedded_user_input, data, -1, 1)
    return {
        'quote': '"' + best_match['quote'] + '"',
        'from': best_match['from'],
        'score': best_score
    }
