import datetime
import logging
from unittest.mock import MagicMock, patch

import requests

from src.word_api import today_word


@patch("src.word_api.requests.get")
@patch("src.word_api.date")
def test_today_word_success(mock_date, mock_get, caplog):
    """Successful retrieval returns the uppercase solution."""
    # Patching the name `date` in src.word_api leaves datetime.date untouched,
    # so this is still a real date and formats correctly in the f-string.
    mock_date.today.return_value = datetime.date(2026, 9, 29)

    mock_response = MagicMock()
    mock_response.json.return_value = {"solution": "cigar"}
    mock_get.return_value = mock_response

    with caplog.at_level(logging.DEBUG, logger="src.word_api"):
        result = today_word()

    expected_url = "https://www.nytimes.com/svc/wordle/v2/2026-09-29.json"
    mock_get.assert_called_once_with(expected_url, timeout=10)
    mock_response.raise_for_status.assert_called_once()
    assert "Answer: cigar" in caplog.text
    assert result == "CIGAR"


@patch("src.word_api.requests.get")
def test_today_word_request_exception(mock_get):
    """Connection errors and timeouts return None."""
    mock_get.side_effect = requests.ConnectionError("Network failure")

    assert today_word() is None


@patch("src.word_api.requests.get")
def test_today_word_http_error(mock_get):
    """A non-2xx response (e.g. 404) returns None."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404")
    mock_get.return_value = mock_response

    assert today_word() is None


@patch("src.word_api.requests.get")
def test_today_word_invalid_json(mock_get):
    """A response without a 'solution' key returns None."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": "Not found"}
    mock_get.return_value = mock_response

    assert today_word() is None


@patch("src.word_api.requests.get")
def test_today_word_non_json_body(mock_get):
    """A response body that isn't valid JSON returns None."""
    mock_response = MagicMock()
    mock_response.json.side_effect = ValueError("No JSON object could be decoded")
    mock_get.return_value = mock_response

    assert today_word() is None