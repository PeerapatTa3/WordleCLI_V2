"""Data access helpers for saving and loading Wordle data."""

import json
from pathlib import Path


DEFAULT_WORD_POOL = [
    "APPLE",
    "BRAVE",
    "CLOUD",
    "GRAPE",
    "LIGHT",
    "MUSIC",
    "PEARL",
    "STONE",
    "SWORD",
    "TIGER",
]


def save_data(filepath, data):
    """Save data to a JSON file and return True on success."""
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except (OSError, TypeError, ValueError):
        return False


def load_data(filepath):
    """Load data from a JSON file and return an empty list if missing."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError, TypeError):
        return []


def load_word_pool(filepath):
    """Load the word pool, creating a default list if the file does not exist."""
    words = load_data(filepath)
    if words:
        return words
    save_data(filepath, DEFAULT_WORD_POOL)
    return DEFAULT_WORD_POOL.copy()


