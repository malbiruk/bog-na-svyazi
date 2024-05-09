'''
This is the main script
'''
import json
import logging
from pathlib import Path

from config import initialize_logging
from flask import Flask, jsonify, render_template, request
from preprocessing.embed_quotes import main as embed_quotes
from preprocessing.parse_books import main as parse_books
from process_query import answer_with_quote

logger = initialize_logging(level=logging.INFO)

app = Flask(__name__)
app.static_folder = 'static'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/support')
def support():
    return render_template('support.html')


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/process', methods=['POST'])
def process_input():
    with open(Path('data/verses_with_embeddings.json'),
              encoding='utf-8') as f:
        verses = json.load(f)

    data = request.get_json()
    user_input = data['query']
    logger.debug(f'got input: {user_input}')
    quote = answer_with_quote(user_input, verses)
    logger.debug(f'quote: {quote["quote"]}\n'
                 f'from: {quote["from"]}\n'
                 f'score: {quote["score"]}')
    return jsonify(quote)


@app.route('/record-feedback', methods=['POST'])
def record_feedback():
    fb_path = Path('feedback/feedback.tsv')
    if not fb_path.exists():
        with open(fb_path, 'w', encoding='utf-8') as f:
            f.write('user_input\tquote\tfeedback\n')
    data = request.get_json()
    logger.debug(f'got feedback: {data}')
    with open(fb_path, 'a', encoding='utf-8') as f:
        f.write(f'{data["query"]}\t{data["quote"][1:-1]}\t{data["feedback"]}\n')
    return jsonify('OK')


def generate_data_files():
    if not Path('data/verses.json').exists():
        parse_books()
    if not Path('data/verses_with_embeddings.json').exists():
        embed_quotes()

if __name__ == '__main__':
    generate_data_files()
    # app.run(host='0.0.0.0')
