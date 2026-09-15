import requests

from src.word_api import (
    fetch_random_word,
    fetch_valid_words,
    fetch_word_pool,
    is_valid_dictionary_word,
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


def test_is_valid_dictionary_word_accepts_defined_word(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse(
            [{"word": "hello", "meanings": [{"definitions": [{"definition": "a greeting"}]}]}]
        ),
    )
    assert is_valid_dictionary_word("HELLO") is True


def test_is_valid_dictionary_word_rejects_unknown_word(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse([]),
    )
    assert is_valid_dictionary_word("QZXJK") is False


def test_is_valid_dictionary_word_retries_then_accepts(monkeypatch):
    attempts = {"count": 0}

    def flaky_request(url, timeout):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise requests.Timeout("temporary timeout")
        return FakeResponse(
            [{"word": "world", "meanings": [{"definitions": [{"definition": "earth"}]}]}]
        )

    monkeypatch.setattr("src.word_api.requests.get", flaky_request)
    assert is_valid_dictionary_word("WORLD") is True
    assert attempts["count"] == 3


def test_is_valid_dictionary_word_uses_cache(monkeypatch):
    monkeypatch.setattr(
        "src.word_api.requests.get",
        lambda url, timeout: FakeResponse(
            [{"word": "upper", "meanings": [{"definitions": [{"definition": "higher"}]}]}]
        ),
    )
    assert is_valid_dictionary_word("UPPER") is True

    def unexpected_request(url, timeout):
        raise AssertionError("cached word should not call API")

    monkeypatch.setattr("src.word_api.requests.get", unexpected_request)
    assert is_valid_dictionary_word("UPPER") is True


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