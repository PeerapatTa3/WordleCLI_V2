"""Data access helpers for saving and loading Wordle data."""

import json
import os
from pathlib import Path

# Keep history outside the installed package so it persists across upgrades
# and can be written regardless of the current working directory.
HISTORY_PATH = Path(
    os.environ.get(
        "WORDLE_HISTORY_PATH",
        str(Path.home() / ".wordle" / "history.json"),
    )
).expanduser().resolve()


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
    """Load history records from a JSON file.

    Returns an empty list when the file is missing, unreadable, corrupted, or
    does not contain a JSON list. Non-dict entries inside the list are dropped
    so callers can always treat the result as a list of records.

    ``path`` defaults to ``HISTORY_PATH`` when omitted.
    """
    try:
        with open(HISTORY_PATH if path is None else path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError, TypeError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    return [record for record in data if isinstance(record, dict)]
