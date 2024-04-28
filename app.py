'''
This is the main script
'''
from pathlib import Path
import json

from config import initialize_logging
from flask import Flask, jsonify, request, render_template
from preprocessing.embed_quotes import main as embed_quotes
from preprocessing.parse_books import main as parse_books
from process_query import answer_with_quote

logger = initialize_logging()

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    with open(Path('data/verses_with_embeddings.json'),
              encoding='utf-8') as f:
        verses = json.load(f)

    data = request.get_json()
    user_input = data['query']
    quote = answer_with_quote(user_input, verses)
    return jsonify(quote)


def generate_data_files():
    if not Path('data/verses.json').exists():
        parse_books()
    if not Path('data/verses_with_embeddings.json').exists():
        embed_quotes()


def main():
    generate_data_files()


if __name__ == '__main__':
    main()
    app.run(debug=True)
