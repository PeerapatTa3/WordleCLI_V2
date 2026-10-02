import io
import json

import pytest

import src.cli as cli
import src.data_manager as dm
from src.cli import (
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


def test_display_history_groups_records_by_game(monkeypatch, capsys):
    history = [
        {"guess": "HELLO", "correct": False, "game_number": 1, "secret_word": "APPLE"},
        {"guess": "APPLE", "correct": True, "game_number": 1, "secret_word": "APPLE"},
        {"guess": "WORLD", "correct": False, "game_number": 2, "secret_word": "ELECT"},
    ]
    monkeypatch.setattr("src.cli.load_data", lambda *args, **kwargs: history)
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
    buffer = io.StringIO()
    fake_console = Console(force_terminal=False, file=buffer)
    monkeypatch.setattr("src.cli.console", fake_console)
    erase_lines(3)
    assert buffer.getvalue() == ""


def test_clear_screen_writes_nothing_when_not_terminal(monkeypatch):
    """clear_screen is a no-op when console.is_terminal is False."""
    from rich.console import Console
    buffer = io.StringIO()
    fake_console = Console(force_terminal=False, file=buffer)
    monkeypatch.setattr("src.cli.console", fake_console)
    cleared = []
    monkeypatch.setattr(fake_console, "clear", lambda: cleared.append(True))
    clear_screen()
    assert cleared == []
    assert buffer.getvalue() == ""


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


@pytest.fixture
def history_file(tmp_path, monkeypatch):
    """Point the app's history file at a temporary path."""
    path = tmp_path / "history.json"
    monkeypatch.setattr(dm, "HISTORY_PATH", path)
    return path


def script_input(monkeypatch, *responses):
    """Feed scripted answers to the Rich console prompt."""
    answers = iter(responses)
    monkeypatch.setattr(cli.console, "input", lambda *a, **k: next(answers))


def record_screens(monkeypatch):
    """Capture the ``message`` passed to each render_game_screen call."""
    messages = []

    def fake(*args, **kwargs):
        messages.append(args[4] if len(args) > 4 else kwargs.get("message"))

    monkeypatch.setattr(cli, "render_game_screen", fake)
    return messages


@pytest.mark.parametrize("content", ["{}", '"abc"', "42", "null"])
def test_load_data_returns_empty_list_for_non_list_json(tmp_path, content):
    path = tmp_path / "h.json"
    path.write_text(content, encoding="utf-8")
    assert dm.load_data(path) == []


def test_load_data_drops_non_dict_records(tmp_path):
    path = tmp_path / "h.json"
    path.write_text(json.dumps([{"guess": "APPLE"}, "junk", 3, None]), encoding="utf-8")
    assert dm.load_data(path) == [{"guess": "APPLE"}]


def test_history_path_is_not_cwd_relative():
    assert dm.HISTORY_PATH.is_absolute()
    assert dm.HISTORY_PATH.name == "history.json"


def test_hint_text_reveals_positions_in_order():
    message, positions = cli.hint_text("APPLE")
    assert "Letter 1 is 'A'" in message
    assert positions == {0}
    message, positions = cli.hint_text("APPLE", positions)
    assert "Letter 2 is 'P'" in message
    assert positions == {0, 1}


def test_hint_text_when_everything_revealed():
    message, positions = cli.hint_text("APPLE", {0, 1, 2, 3, 4})
    assert "APPLE" in message
    assert positions == {0, 1, 2, 3, 4}


def test_hint_message_is_passed_to_next_redraw(history_file, monkeypatch, capsys):
    monkeypatch.setenv("WORDLE_TEST_WORD", "GRAPE")
    messages = record_screens(monkeypatch)
    script_input(monkeypatch, "hint", "grape")
    cli.play_game()
    assert messages[0] is None
    assert "Letter 1 is 'G'" in capsys.readouterr().out


def test_invalid_guesses_erase_previous_error(monkeypatch):
    erased = []
    monkeypatch.setattr(cli, "erase_lines", erased.append)
    script_input(monkeypatch, "abc", "abc", "APPLE")
    assert cli.get_guess_input(5, frozenset({"APPLE"})) == "APPLE"
    assert erased == [1, 2, 2]


def test_hint_line_is_replaced_by_invalid_guess(monkeypatch):
    erased = []
    monkeypatch.setattr(cli, "erase_lines", erased.append)
    cli._last_status_lines = 1
    script_input(monkeypatch, "abc", "APPLE")
    assert cli.get_guess_input(5, frozenset({"APPLE"})) == "APPLE"
    assert erased[0] == 2


def test_discard_game_removes_only_that_game():
    history = [{"game_number": 1, "guess": "A"}, {"game_number": 2, "guess": "B"}]
    assert cli._discard_game(history, 2) == [{"game_number": 1, "guess": "A"}]


def test_answer_discards_partial_game(history_file, monkeypatch):
    monkeypatch.setenv("WORDLE_TEST_WORD", "GRAPE")
    script_input(monkeypatch, "crane", "answer")
    cli.play_game()
    assert dm.load_data(history_file) == []


def test_answer_before_any_guess_writes_nothing(history_file, monkeypatch):
    monkeypatch.setenv("WORDLE_TEST_WORD", "GRAPE")
    script_input(monkeypatch, "answer")
    cli.play_game()
    assert not history_file.exists()


def test_full_game_win_is_persisted(history_file, monkeypatch):
    monkeypatch.setenv("WORDLE_TEST_WORD", "GRAPE")
    script_input(monkeypatch, "crane", "grape")
    cli.play_game()
    records = dm.load_data(history_file)
    assert [r["guess"] for r in records] == ["CRANE", "GRAPE"]
    assert [r["correct"] for r in records] == [False, True]
    assert {r["game_number"] for r in records} == {1}
    assert records[-1]["secret_word"] == "GRAPE"


def test_second_game_gets_next_game_number(history_file, monkeypatch):
    monkeypatch.setenv("WORDLE_TEST_WORD", "GRAPE")
    script_input(monkeypatch, "grape", "grape")
    cli.play_game()
    cli.play_game()
    assert [r["game_number"] for r in dm.load_data(history_file)] == [1, 2]


def test_history_deleted_mid_game_is_not_resurrected(history_file, monkeypatch):
    """A stale in-memory history must not overwrite a manual edit."""
    monkeypatch.setenv("WORDLE_TEST_WORD", "GRAPE")
    answers = iter(["crane", "grape"])

    def prompt(*args, **kwargs):
        reply = next(answers)
        if reply == "grape":
            history_file.write_text("[]", encoding="utf-8")
        return reply

    monkeypatch.setattr(cli.console, "input", prompt)
    cli.play_game()
    assert [r["guess"] for r in dm.load_data(history_file)] == ["GRAPE"]


def test_save_failure_shows_warning_once(history_file, monkeypatch):
    monkeypatch.setenv("WORDLE_TEST_WORD", "GRAPE")
    messages = record_screens(monkeypatch)
    monkeypatch.setattr(cli, "save_data", lambda *a, **k: False)
    script_input(monkeypatch, "crane", "brave", "grape")
    cli.play_game()
    warnings = [m for m in messages if m and "could not save" in m]
    assert len(warnings) == 1