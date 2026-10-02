"""Tests for src.word_bank: local loading, filtering, and fallback behaviour."""

import pytest

import src.word_bank as wb


@pytest.fixture
def fake_data(tmp_path, monkeypatch):
    """Point load_word_bank at tmp_path/src/data via a fake module location."""
    data_dir = tmp_path / "src" / "data"
    data_dir.mkdir(parents=True)
    monkeypatch.setattr(wb, "__file__", str(tmp_path / "src" / "word_bank.py"))

    def write(answers=None, valid=None):
        if answers is not None:
            (data_dir / "answers.txt").write_text(answers, encoding="utf-8")
        if valid is not None:
            (data_dir / "valid_words.txt").write_text(valid, encoding="utf-8")

    return write


def _assert_playable(answers, valid):
    assert len(answers) > 0
    assert len(valid) > 0
    assert set(answers) <= set(valid)


# --- real data files -------------------------------------------------------

def test_real_word_bank_loads_and_is_consistent():
    answers, valid = wb.load_word_bank(5)
    _assert_playable(answers, valid)
    assert isinstance(answers, tuple)
    assert isinstance(valid, frozenset)
    assert all(len(w) == 5 and w.isalpha() and w.isupper() for w in valid)
    assert len(answers) != len(wb.DEFAULT_WORD_POOL)  # real files, not fallback


# --- missing / empty files -> default pool ---------------------------------

def test_missing_files_fall_back_to_default_pool(fake_data):
    answers, valid = wb.load_word_bank(5)  # no files written at all
    assert answers == tuple(wb.DEFAULT_WORD_POOL)
    assert valid == frozenset(wb.DEFAULT_WORD_POOL)


def test_empty_files_fall_back_to_default_pool(fake_data):
    fake_data(answers="", valid="")
    answers, valid = wb.load_word_bank(5)
    assert answers == tuple(wb.DEFAULT_WORD_POOL)
    assert valid == frozenset(wb.DEFAULT_WORD_POOL)


def test_files_with_no_valid_length_words_fall_back(fake_data):
    fake_data(answers="TOOLONG\nab\n12345\n", valid="TOOLONG\nab\n12345\n")
    answers, valid = wb.load_word_bank(5)
    _assert_playable(answers, valid)
    assert answers == tuple(wb.DEFAULT_WORD_POOL)


def test_only_answers_missing_still_returns_playable_bank(fake_data):
    fake_data(valid="ABCDE\nFGHIJ\n")
    _assert_playable(*wb.load_word_bank(5))


def test_only_valid_words_missing_still_returns_playable_bank(fake_data):
    fake_data(answers="ABCDE\nFGHIJ\n")
    _assert_playable(*wb.load_word_bank(5))


def test_default_pool_is_well_formed():
    assert wb.DEFAULT_WORD_POOL
    assert all(len(w) == 5 and w.isalpha() and w.isupper() for w in wb.DEFAULT_WORD_POOL)


# --- parsing / filtering ---------------------------------------------------

def test_loader_filters_uppercases_and_strips(fake_data):
    fake_data(
        answers="apple\n  BRAVE  \n\ncat\ntoolong\nab3de\nhe llo\n",
        valid="cloud\nGRAPE\n",
    )
    answers, valid = wb.load_word_bank(5)
    assert answers == ("APPLE", "BRAVE")
    assert valid == frozenset({"APPLE", "BRAVE", "CLOUD", "GRAPE"})


def test_valid_set_is_union_of_answers_and_valid_words(fake_data):
    fake_data(answers="APPLE\n", valid="BRAVE\n")  # APPLE only in answers
    answers, valid = wb.load_word_bank(5)
    assert answers == ("APPLE",)
    assert "APPLE" in valid and "BRAVE" in valid


def test_load_lines_returns_empty_list_for_missing_file(tmp_path):
    assert wb._load_lines(tmp_path / "nope.txt", 5) == []


def test_load_lines_respects_length(tmp_path):
    f = tmp_path / "w.txt"
    f.write_text("CAT\nAPPLE\nPLANET\n", encoding="utf-8")
    assert wb._load_lines(f, 3) == ["CAT"]
    assert wb._load_lines(f, 6) == ["PLANET"]


# --- no network / CWD independence -----------------------------------------

def test_load_word_bank_makes_no_network_calls(monkeypatch):
    import socket

    def boom(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket.socket, "connect", boom)
    _assert_playable(*wb.load_word_bank(5))


def test_load_word_bank_works_from_any_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    answers, valid = wb.load_word_bank(5)
    _assert_playable(answers, valid)
    assert len(answers) != len(wb.DEFAULT_WORD_POOL)