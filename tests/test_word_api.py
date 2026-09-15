import requests

from src.word_api import (
    fetch_random_word,
    fetch_valid_words,
    fetch_word_pool,
    is_valid_api_word,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_fetch_random_word_accepts_api_list_response(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse(["apple"]),
    )
    assert fetch_random_word() == "APPLE"


def test_fetch_random_word_rejects_wrong_length(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse(["pear"]),
    )
    assert fetch_random_word() is None


def test_fetch_random_word_accepts_common_datamuse_words(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse(
            [
                {"word": "apple", "score": 5000},
                {"word": "qzxjk", "score": 10},
            ]
        ),
    )
    assert fetch_random_word() == "APPLE"


def test_fetch_valid_words_returns_all_common_words(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse(
            [
                {"word": "apple", "score": 5000},
                {"word": "grape", "score": 4000},
                {"word": "qzxjk", "score": 10},
            ]
        ),
    )
    assert fetch_valid_words() == ["APPLE", "GRAPE"]


def test_is_valid_api_word_accepts_exact_meaningful_word(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse([{"word": "hello", "score": 147072}]),
    )
    assert is_valid_api_word("HELLO") is True


def test_is_valid_api_word_rejects_unknown_word(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse([{"word": "hello", "score": 147072}]),
    )
    assert is_valid_api_word("QZXJK") is False


def test_fetch_random_word_returns_none_on_request_failure(monkeypatch):
    def raise_request_error(url, timeout):
        raise requests.RequestException("network unavailable")

    monkeypatch.setattr("src.word_api.requests.get", raise_request_error)
    assert fetch_random_word() is None


def test_fetch_word_pool_removes_duplicates(monkeypatch):
    responses = iter(["APPLE", "APPLE", "GRAPE"])
    monkeypatch.setattr(
        "src.word_api.fetch_random_word",
        lambda length=5: next(responses),
    )
    assert fetch_word_pool(count=2) == ["APPLE", "GRAPE"]