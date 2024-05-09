import argparse
import json
from pathlib import Path
from pprint import pprint

from preprocessing.embed_quotes import embed_quotes
from preprocessing.parse_books import parse_books
from process_query import semantic_search
from sentence_transformers import SentenceTransformer


def main(user_input: str):
    model1 = 'cointegrated/rubert-tiny2'
    model2 = 'finetuning/models/rbt2-10052024_021936'

    if not Path('data/verses.json').exists():
        parse_books()

    for c, model_name in enumerate([model1, model2]):
        if not Path(f'data/{c}.json').exists():
            embed_quotes(out=f'data/{c}.json', model_name=model_name)

        with open(Path(f'data/{c}.json'), encoding='utf-8') as f:
            verses = json.load(f)

        model = SentenceTransformer(model_name)
        embedded_user_input = model.encode(user_input)
        top_matches = semantic_search(embedded_user_input, verses, 0.6, 20)
        print()
        print()
        print(model_name)
        pprint([(i[0]['quote'], i[1]) for i in top_matches])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="️")
    parser.add_argument('-i', '--user_input', type=str, required=True)
    args = parser.parse_args()

    main(**vars(args))
