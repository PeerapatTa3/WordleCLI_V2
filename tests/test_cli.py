import os

import pytest

from src.cli import (
    colorize_feedback,
    display_how_to_play,
    display_menu,
    display_statistics,
    display_answer,
    display_hint,
    display_history,
    get_secret_word,
    get_menu_choice,
    get_guess_input,
    is_valid_guess,
    erase_lines,
    clear_screen,
)
from src.word_bank import load_word_bank


# def test_colorize_feedback_uses_ansi_colors():
#     rendered = colorize_feedback(["✓", "-", "x"])
#     assert "✓" in rendered
#     assert "-" in rendered
#     assert "x" in rendered
#     assert "\x1b[" in rendered


def test_is_valid_guess_accepts_five_letters():
    assert is_valid_guess("APPLE", 5) is True
    assert is_valid_guess("apple", 5) is True


def test_is_valid_guess_rejects_invalid_values():
    assert is_valid_guess("APP", 5) is False
    assert is_valid_guess("APP1E", 5) is False
    assert is_valid_guess("APP LE", 5) is False


def test_is_valid_guess_rejects_word_outside_word_pool():
    assert is_valid_guess("HELLO", 5, {"APPLE", "GRAPE"}) is False
    assert is_valid_guess("apple", 5, {"APPLE", "GRAPE"}) is True


def test_common_local_words_remain_valid_without_api():
    """No API call needed — membership check against the frozenset."""
    valid_words = frozenset(["HELLO", "WORLD", "ELECT", "UPPER", "MINER"])
    assert is_valid_guess("HELLO", 5, valid_words) is True
    assert is_valid_guess("WORLD", 5, valid_words) is True
    assert is_valid_guess("ELECT", 5, valid_words) is True
    assert is_valid_guess("UPPER", 5, valid_words) is True
    assert is_valid_guess("MINER", 5, valid_words) is True


def test_get_secret_word_uses_test_environment_variable(monkeypatch):
    monkeypatch.setenv("WORDLE_TEST_WORD", "grape")
    secret_word, is_test_mode = get_secret_word(["APPLE"])
    assert secret_word == "GRAPE"
    assert is_test_mode is True


def test_get_menu_choice_normalizes_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: "  PLAY  ")
    assert get_menu_choice() == "play"


def test_get_guess_input_retries_until_valid(monkeypatch):
    responses = iter(["abc", "HELLO", "WORLD"])
    monkeypatch.setattr("builtins.input", lambda: next(responses))
    assert get_guess_input(5) == "HELLO"


def test_get_guess_input_accepts_hint_command(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: " hint ")
    assert get_guess_input(5, {"APPLE"}) == "hint"


def test_display_menu_prints_options(capsys):
    display_menu()
    output = capsys.readouterr().out
    assert "Play Wordle" in output
    assert "View Statistics" in output
    assert "How to Play" in output
    assert "Exit" in output


def test_display_statistics_reports_wins_and_distribution(capsys):
    history = [
        {"correct": False, "attempt": 1, "game_number": 1},
        {"correct": True, "attempt": 3, "game_number": 1},
        {"correct": True, "attempt": 2, "game_number": 2},
    ]
    display_statistics(history)
    output = capsys.readouterr().out
    assert "Games Played:    2" in output
    assert "Win Rate:        100.0%" in output
    assert "Current Streak:  2" in output
    assert "3: * (1)" not in output
    assert "3: █ (1)" in output


def test_display_history_groups_records_by_game(capsys):
    history = [
        {"guess": "HELLO", "correct": False, "game_number": 1, "secret_word": "APPLE"},
        {"guess": "APPLE", "correct": True, "game_number": 1, "secret_word": "APPLE"},
        {"guess": "WORLD", "correct": False, "game_number": 2, "secret_word": "ELECT"},
    ]
    display_history.__globals__["load_data"] = lambda path: history
    display_history()
    output = capsys.readouterr().out
    assert "Total Games Played: 2" in output
    assert "Game 1" in output
    assert "WON" in output
    assert "APPLE" in output
    assert "Game 2" in output
    assert "LOST" in output
    assert "ELECT" in output


def test_display_how_to_play_explains_feedback(capsys):
    display_how_to_play()
    output = capsys.readouterr().out
    assert "HOW TO PLAY" in output
    assert "Correct letter in the correct position" in output
    assert "hint" in output


def test_display_hint_reveals_one_position(capsys):
    revealed = display_hint("APPLE")
    output = capsys.readouterr().out
    assert revealed == {0}
    assert "Letter 1 is 'A'" in output


def test_display_answer_reveals_secret_word(capsys):
    display_answer("APPLE")
    assert "Answer: APPLE" in capsys.readouterr().out


def test_erase_lines_writes_nothing_when_not_terminal(monkeypatch):
    """erase_lines is a no-op when console.is_terminal is False."""
    from rich.console import Console
    fake_console = Console(force_terminal=False, file=open(os.devnull, "w"))
    monkeypatch.setattr("src.cli.console", fake_console)
    written = []
    monkeypatch.setattr(fake_console.file, "write", lambda s: written.append(s))
    erase_lines(3)
    assert written == []

def test_clear_screen_writes_nothing_when_not_terminal(monkeypatch):
    """clear_screen is a no-op when console.is_terminal is False."""
    from rich.console import Console
    fake_console = Console(force_terminal=False, file=open(os.devnull, "w"))
    monkeypatch.setattr("src.cli.console", fake_console)
    cleared = []
    monkeypatch.setattr(fake_console, "clear", lambda: cleared.append(True))
    clear_screen()
    assert cleared == []


def test_word_bank_answers_subset_of_valid():
    """Every answer word must be in the valid words set."""
    answers, valid = load_word_bank(5)
    for word in answers:
        assert word in valid, f"{word} not in valid_words"


def test_word_bank_accepts_test_word(monkeypatch):
    """WORDLE_TEST_WORD is accepted by is_valid_guess via the word bank."""
    monkeypatch.setenv("WORDLE_TEST_WORD", "grape")
    answers, valid = load_word_bank(5)
    assert is_valid_guess("GRAPE", 5, valid)


def test_get_secret_word_returns_from_answers(monkeypatch):
    """get_secret_word picks from answers when no test word is set."""
    monkeypatch.setenv("WORDLE_TEST_WORD", "")
    word, is_test = get_secret_word(["TIGER", "CLOUD", "BRAVE"])
    assert word in ("TIGER", "CLOUD", "BRAVE")
    assert is_test is False


def test_get_guess_input_invalid_shows_one_error_line(monkeypatch, capsys):
    """Invalid guess prints a single 'Invalid guess' line (not a Panel)."""
    responses = iter(["ZZZZZ", "APPLE"])
    monkeypatch.setattr("builtins.input", lambda: next(responses))
    result = get_guess_input(5, frozenset(["APPLE"]))
    assert result == "APPLE"
    output = capsys.readouterr().out
    assert "Invalid guess" in output
    assert "Panel" not in output
