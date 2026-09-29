"""Data access helpers for saving and loading Wordle data."""

import json
from pathlib import Path

HISTORY_PATH = Path("data/history.json")

def save_data(data, path=None):
    """Save data to a JSON file and return True on success.

    ``path`` defaults to ``HISTORY_PATH`` when omitted.
    """
    try:
        path = Path(HISTORY_PATH if path is None else path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except (OSError, TypeError, ValueError):
        return False


def load_data(path=None):
    """Load data from a JSON file and return an empty list if missing.

    ``path`` defaults to ``HISTORY_PATH`` when omitted.
    """
    try:
        with open(HISTORY_PATH if path is None else path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError, TypeError):
        return []