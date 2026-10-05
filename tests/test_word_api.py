"""Tests for the build-time word API module (now in scripts/).

These tests verify the API helpers that were moved from src/word_api.py
to scripts/word_api.py.  The runtime game no longer uses network calls.
"""

import scripts.word_api as word_api


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_fetch_random_word_accepts_api_list_response(monkeypatch):
    monkeypatch.setattr(
        "scripts.word_api.requests.get",
        lambda url, timeout: FakeResponse(["apple"]),
    )
    assert word_api.fetch_random_word() == "APPLE"


def test_fetch_random_word_rejects_wrong_length(monkeypatch):
    monkeypatch.setattr(
        "scripts.word_api.requests.get",
        lambda url, timeout: FakeResponse(["pear"]),
    )
    assert word_api.fetch_random_word() is None


def test_fetch_random_word_accepts_common_datamuse_words(monkeypatch):
    monkeypatch.setattr(
        "scripts.word_api.requests.get",
        lambda url, timeout: FakeResponse(
            [
                {"word": "apple", "score": 5000},
                {"word": "qzxjk", "score": 10},
            ]
        ),
    )
    assert word_api.fetch_random_word() == "APPLE"


def test_fetch_valid_words_returns_all_common_words(monkeypatch):
    monkeypatch.setattr(
        "scripts.word_api.requests.get",
        lambda url, timeout: FakeResponse(
            [
                {"word": "apple", "score": 5000},
                {"word": "grape", "score": 4000},
                {"word": "qzxjk", "score": 10},
            ]
        ),
    )
    assert word_api.fetch_valid_words() == ["APPLE", "GRAPE"]


def test_fetch_random_word_returns_none_on_request_failure(monkeypatch):
    import requests

    def raise_request_error(url, timeout):
        raise requests.RequestException("network unavailable")

    monkeypatch.setattr("scripts.word_api.requests.get", raise_request_error)
    assert word_api.fetch_random_word() is None
