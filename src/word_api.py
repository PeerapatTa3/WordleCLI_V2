"""Helpers for fetching valid 5-letter words from a public API."""

import random
from urllib.parse import quote

import requests

DEFAULT_API_URL = "https://api.datamuse.com/words?sp=?????&max=1000"
MIN_WORD_SCORE = 1000


def fetch_valid_words(length=5, url=DEFAULT_API_URL):
    """Fetch all common words of the requested length from Datamuse."""
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

        return valid_words
    except (requests.RequestException, ValueError, TypeError, IndexError):
        return []


def fetch_random_word(length=5, url=DEFAULT_API_URL):
    """Fetch a random common word of the requested length from Datamuse."""
    words = fetch_valid_words(length, url)
    return random.choice(words) if words else None

    return None


def is_valid_api_word(word, length=5):
    """Check an exact word against Datamuse when it is outside the main list."""
    normalized = str(word).strip().lower()
    if len(normalized) != length or not normalized.isalpha():
        return False

    url = f"https://api.datamuse.com/words?sp={quote(normalized)}&max=10"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return any(
            isinstance(item, dict)
            and str(item.get("word", "")).strip().lower() == normalized
            for item in data
        )
    except (requests.RequestException, ValueError, TypeError):
        return False


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
