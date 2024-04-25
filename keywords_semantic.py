import random
from collections import Counter

import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Example user message in Russian
user_message = 'Я чувствую себя потерянным и нуждаюсь в направлении.'

# Example Bible verses in Russian (replace with actual verses)
bible_verses = [
    'Господь - Пастырь мой: мне не будет недостатка. (Псалом 23:1)',
    'Уповай на Господа от всего сердца твоего, и не надейся на собственный разум. (Притчи 3:5)',
    'Придите ко Мне, все труждающиеся и обремененные, и Я дам вам покой. (Матфея 11:28)'
]

# Load spaCy model for Russian
nlp_ru = spacy.load('ru_core_news_md')

# Tokenize and preprocess user message
stop_words = set(stopwords.words('russian'))
user_tokens = [token.lemma_ for token in nlp_ru(user_message) if token.lemma_ not in stop_words]

# Tokenize and preprocess Bible verses
bible_tokens = []
for verse in bible_verses:
    verse_tokens = [token.lemma_ for token in nlp_ru(verse) if token.lemma_ not in stop_words]
    bible_tokens.append(verse_tokens)

# Keyword search
keyword_matches = []
for idx, verse_tokens in enumerate(bible_tokens):
    for word in user_tokens:
        if word in verse_tokens:
            keyword_matches.append(idx)

# Calculate semantic similarity between user message and Bible verses
similarities = []
for verse_tokens in bible_tokens:
    verse_text = ' '.join(verse_tokens)
    verse_similarity = nlp_ru(user_message).similarity(nlp_ru(verse_text))
    similarities.append(verse_similarity)

# Determine which method performed better
if keyword_matches and similarities:
    avg_similarity = sum(similarities) / len(similarities)
    if len(keyword_matches) >= avg_similarity:
        best_matching_verse_index = random.choice(keyword_matches)
        print('Response (Keyword Search):', bible_verses[best_matching_verse_index])
    else:
        best_matching_verse_index = similarities.index(max(similarities))
        print('Response (Semantic Similarity):', bible_verses[best_matching_verse_index])
elif keyword_matches:
    best_matching_verse_index = random.choice(keyword_matches)
    print('Response (Keyword Search):', bible_verses[best_matching_verse_index])
elif similarities:
    best_matching_verse_index = similarities.index(max(similarities))
    print('Response (Semantic Similarity):', bible_verses[best_matching_verse_index])
else:
    print('No matching verse found.')
