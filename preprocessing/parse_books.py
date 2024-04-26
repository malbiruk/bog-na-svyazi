import json
import logging
from pathlib import Path

from tqdm import tqdm

logger = logging.getLogger('app.' + __name__)


def parse_text(text: str) -> list:
    # pylint: disable = unsubscriptable-object
    quotes = []

    current_book = None
    current_section = None
    current_verse = None

    def add_quote(verse_text, current_book, current_section, verse_number):
        quote = {
            "quote": verse_text,
            "from": f"{current_book} {current_section}:{verse_number}"
        }
        if not (verse_text.endswith('?') or verse_text=='Вот, Я наперед сказал вам.'):
            quotes.append(quote)

    def handle_verse(verse_number, verse_text):
        nonlocal current_verse
        if verse_text[-1] not in '.!?':
            current_verse = (verse_number, verse_text)
        else:
            add_quote(verse_text, current_book, current_section, verse_number)
            current_verse = None

    for line in tqdm(text.split('\n'), leave=False):
        line = line.strip().split()
        if not line:
            continue

        if not line[0].isdigit():
            current_book = ' '.join(line)
            current_section = None
            current_verse = None
        elif len(line) == 1 and line[0].isdigit():
            current_section = line[0]
            current_verse = None
        else:
            if not current_verse:
                verse_number, verse_text = line[0], ' '.join(line[1:])
                handle_verse(verse_number, verse_text)
            else:
                verse_number = current_verse[0]
                verse_text = current_verse[1] + ' ' + ' '.join(line[1:])
                handle_verse(verse_number, verse_text)

    return quotes


def main(inp: Path = Path('data/Автор_неизвестен_Библия_Новый_Завет_royallib_com.txt'),
         out: Path = Path('data/verses.json'),
         inp_encoding='WINDOWS-1251'):

    logger.info(f'parsing {inp.name}... ⏳')
    with open(inp, encoding=inp_encoding) as f:
        text = f.read()
    verses = parse_text(text)

    with open(out, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
