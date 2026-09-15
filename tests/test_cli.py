import pytest

from cli import colorize_feedback, display_menu, get_menu_choice, is_valid_guess, get_guess_input


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


def test_get_menu_choice_normalizes_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "  PLAY  ")
    assert get_menu_choice() == "play"


def test_get_guess_input_retries_until_valid(monkeypatch):
    responses = iter(["abc", "HELLO", "WORLD"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))
    assert get_guess_input(5) == "HELLO"


def test_display_menu_prints_options(capsys):
    display_menu()
    output = capsys.readouterr().out
    assert "1. Play Wordle" in output
    assert "4. Exit" in output
