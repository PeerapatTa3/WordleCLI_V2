import pytest

from cli import (
    colorize_feedback,
    display_how_to_play,
    display_menu,
    display_statistics,
    display_answer,
    display_hint,
    get_secret_word,
    get_menu_choice,
    get_guess_input,
    is_valid_guess,
)


def test_colorize_feedback_uses_ansi_colors():
    rendered = colorize_feedback(["✓", "-", "x"])
    assert "✓" in rendered
    assert "-" in rendered
    assert "x" in rendered
    assert "\x1b[" in rendered


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


def test_get_secret_word_uses_test_environment_variable(monkeypatch):
    monkeypatch.setenv("WORDLE_TEST_WORD", "grape")
    secret_word, is_test_mode = get_secret_word(["APPLE"])
    assert secret_word == "GRAPE"
    assert is_test_mode is True


def test_get_menu_choice_normalizes_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "  PLAY  ")
    assert get_menu_choice() == "play"


def test_get_guess_input_retries_until_valid(monkeypatch):
    responses = iter(["abc", "HELLO", "WORLD"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))
    assert get_guess_input(5) == "HELLO"


def test_get_guess_input_accepts_hint_command(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: " hint ")
    assert get_guess_input(5, {"APPLE"}) == "hint"


def test_display_menu_prints_options(capsys):
    display_menu()
    output = capsys.readouterr().out
    assert "1. Play Wordle" in output
    assert "3. View Statistics" in output
    assert "4. How to Play" in output
    assert "5. Exit" in output


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
