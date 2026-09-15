"""Helpers for fetching valid 5-letter words from a public API."""

import random

import requests

DEFAULT_API_URL = "https://api.datamuse.com/words?sp=?????&max=1000"
MIN_WORD_SCORE = 1000


def fetch_random_word(length=5, url=DEFAULT_API_URL):
    """Fetch a random common word of the requested length from Datamuse."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        candidates = data if isinstance(data, list) else [data]
        valid_words = []
        for candidate in candidates:
            if isinstance(candidate, dict):
                word = candidate.get("word") or candidate.get("wordText")
                score = candidate.get("score", MIN_WORD_SCORE)
                if isinstance(score, (int, float)) and score < MIN_WORD_SCORE:
                    continue
            elif isinstance(candidate, str):
                word = candidate
            else:
                continue

            word = str(word).strip().upper()
            if len(word) == length and word.isalpha() and word not in valid_words:
                valid_words.append(word)

        return random.choice(valid_words) if valid_words else None
    except (requests.RequestException, ValueError, TypeError, IndexError):
        return None

    return None


def fetch_word_pool(count=10, length=5):
    """Fetch a list of valid words from the API, with duplicates removed."""
    words = []
    while len(words) < count:
        word = fetch_random_word(length)
        if word and word not in words:
            words.append(word)
        if len(words) >= count:
            break
    return words
