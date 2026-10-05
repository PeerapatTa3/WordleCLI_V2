"""Script for fetching Wordle word lists from public APIs at build time.

This is a build-time script, not used at runtime. The game uses
the local word lists in data/valid_words.txt and data/answers.txt.
"""

import random
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
