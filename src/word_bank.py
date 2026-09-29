"""Local word bank loader — no network calls at runtime.

Loads answers and valid words from local text files in data/.
Paths are relative to this module so the game works from any CWD.
"""

from pathlib import Path

def load_word_bank(length=5):
    """Load word bank from local files.

    Returns
    -------
    (answers_tuple, valid_frozenset)
        Answers for picking the secret word, and the full valid-word set
        (answers ∪ valid_words) for guess validation.
    """
    base = Path(__file__).resolve().parent.parent / "data"
    answers = _load_lines(base / "answers.txt", length)
    valid_words = _load_lines(base / "valid_words.txt", length)

    if not answers or not valid_words:
        #console.print("[bold red]No word bank found. Please run `make data` to download the word lists.[/bold red]")
        return (tuple(None), frozenset(None))

    valid_set = set(valid_words) | set(answers)
    return (tuple(answers), frozenset(valid_set))



def _load_lines(path, length):
    """Return uppercase alpha words of the given length from a text file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [
                line.strip().upper()
                for line in f
                if line.strip()
                and len(line.strip()) == length
                and line.strip().isalpha()
            ]
    except (OSError, IOError):
        return []