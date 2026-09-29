"""Data access helpers for saving and loading Wordle data."""

import json
from pathlib import Path

HISTORY_PATH = Path("data/history.json")

def save_data(data):
    """Save data to a JSON file and return True on success."""
    try:
        path = Path(HISTORY_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except (OSError, TypeError, ValueError):
        return False


def load_data():
    """Load data from a JSON file and return an empty list if missing."""
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError, TypeError):
        return []

