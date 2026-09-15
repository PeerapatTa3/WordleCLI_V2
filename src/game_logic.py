"""Business logic for the Wordle CLI game."""


class WordleGame:
    """Domain model for a single game session."""

    def __init__(self, secret_word, word_length=5):
        self.secret_word = secret_word.upper()
        self.word_length = word_length
        self.attempts = 0

    def evaluate_guess(self, guess):
        """Return feedback for a guess using Wordle-like rules."""
        return calculate_feedback(guess, self.secret_word)


def calculate_feedback(guess, secret_word):
    """Compute a Wordle-like feedback result for a single guess."""
    guess = guess.upper()
    secret = secret_word.upper()
    result = ["x"] * len(guess)
    remaining = {}

    for i, (g_char, s_char) in enumerate(zip(guess, secret)):
        if g_char == s_char:
            result[i] = "✓"
        else:
            remaining[s_char] = remaining.get(s_char, 0) + 1

    for i, g_char in enumerate(guess):
        if result[i] == "✓":
            continue
        if remaining.get(g_char, 0) > 0:
            result[i] = "-"
            remaining[g_char] -= 1

    return result


def search_history(history, keyword):
    """Search guess_history by matching a keyword in guess strings."""
    keyword = (keyword or "").strip().upper()
    if not keyword:
        return history

    return [item for item in history if keyword in str(item.get("guess", "")).upper()]


def filter_history(history, condition):
    """Filter history by a given condition such as correct guesses."""
    if condition == "correct":
        return [item for item in history if bool(item.get("correct"))]
    if condition == "incorrect":
        return [item for item in history if not bool(item.get("correct"))]
    return history
