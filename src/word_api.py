"""Helper for fetching today's Wordle answer from the NYT endpoint.

Not used by the game at runtime; the game loads word lists from local files
via src.word_bank. Kept for scripts and tests that need the daily answer.
"""
import logging
from datetime import date

import requests

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10  # seconds


def today_word():
    """Return today's Wordle answer in uppercase, or None on any failure."""
    today = date.today()
    url = f"https://www.nytimes.com/svc/wordle/v2/{today:%Y-%m-%d}.json"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        solution = response.json()["solution"]
        logger.debug("Answer: %s", solution)
        return solution.upper()
    except (requests.RequestException, KeyError, ValueError, AttributeError):
        logger.warning("Could not fetch today's word", exc_info=True)
        return None