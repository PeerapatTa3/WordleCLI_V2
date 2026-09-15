"""Helpers for fetching valid 5-letter words from a public API."""

import requests

DEFAULT_API_URL = "https://random-word-api.vercel.app/api?words=1&length=5"


def fetch_random_word(length=5, url=DEFAULT_API_URL):
    """Fetch a random word of the requested length from the API."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            word = data[0]
        elif isinstance(data, dict):
            word = data.get("word") or data.get("wordText")
        else:
            return None

        word = str(word).strip().upper()
        if len(word) == length and word.isalpha():
            return word
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
