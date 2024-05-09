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
        return None

    top_matches.sort(key=lambda x: x[1], reverse=True)
    logger.debug([(i[0]['quote'], i[1]) for i in top_matches[:top_n]])

    return top_matches


def answer_with_quote(user_input: str,
                      data: list,
                      threshold: float = 0.6,
                      top_n: int = 20,
                      model_name='cointegrated/rubert-tiny2') -> dict:
    model = SentenceTransformer(model_name)
    embedded_user_input = model.encode(user_input)
    top_matches = semantic_search(embedded_user_input, data, threshold, top_n)
    selected_match = random.choice(top_matches)
    best_match, best_score = selected_match

    if top_matches:
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
