import json

from src.game_logic import WordleGame, calculate_feedback, search_history, filter_history
from src.data_manager import save_data, load_data


def test_calculate_feedback_exact_match():
    assert calculate_feedback("APPLE", "APPLE") == ["✓", "✓", "✓", "✓", "✓"]


def test_calculate_feedback_mixed_result():
    assert calculate_feedback("AERIE", "APPLE") == ["✓", "x", "x", "x", "✓"]


def test_calculate_feedback_handles_duplicate_letters():
    assert calculate_feedback("ALLEY", "APPLE") == ["✓", "-", "x", "-", "x"]


def test_wordle_game_tracks_state():
    game = WordleGame("APPLE")
    assert game.secret_word == "APPLE"
    assert game.word_length == 5
    assert game.attempts == 0


def test_wordle_game_evaluates_guess_case_insensitively():
    game = WordleGame("APPLE")
    assert game.evaluate_guess("apple") == ["✓", "✓", "✓", "✓", "✓"]


def test_search_history_matches_keyword_case_insensitive():
    history = [{"guess": "APPLE"}, {"guess": "PEARL"}, {"guess": "GRAPE"}]
    assert search_history(history, "pear") == [{"guess": "PEARL"}]


def test_filter_history_by_correct_flag():
    history = [{"guess": "APPLE", "correct": True}, {"guess": "CRANE", "correct": False}]
    assert filter_history(history, "correct") == [{"guess": "APPLE", "correct": True}]


def test_save_and_load_data_round_trip(tmp_path):
    path = tmp_path / "history.json"
    payload = [{"guess": "APPLE", "correct": True}]
    assert save_data(path, payload) is True
    assert load_data(path) == payload


def test_load_data_returns_empty_list_for_missing_file(tmp_path):
    path = tmp_path / "missing.json"
    assert load_data(path) == []


def test_load_data_returns_empty_list_for_corrupted_json(tmp_path):
    path = tmp_path / "corrupted.json"
    path.write_text("{not valid json", encoding="utf-8")
    assert load_data(path) == []
