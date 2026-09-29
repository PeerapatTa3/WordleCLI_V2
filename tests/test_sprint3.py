"""Sprint 3 tests: hint message, error redraw, answer discard, history hardening."""

import json

import pytest

import src.cli as cli
import src.data_manager as dm


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


# --- history hardening -----------------------------------------------------

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


# --- F1: hint ---------------------------------------------------------------

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


def test_hint_message_is_passed_to_next_redraw(history_file, monkeypatch):
    monkeypatch.setenv("WORDLE_TEST_WORD", "GRAPE")
    messages = record_screens(monkeypatch)
    script_input(monkeypatch, "hint", "grape")
    cli.play_game()
    assert messages[0] is None
    assert "Letter 1 is 'G'" in messages[1]


# --- F2: error line replacement ---------------------------------------------

def test_invalid_guesses_erase_previous_error(monkeypatch):
    erased = []
    monkeypatch.setattr(cli, "erase_lines", erased.append)
    script_input(monkeypatch, "abc", "abc", "APPLE")
    assert cli.get_guess_input(5, frozenset({"APPLE"})) == "APPLE"
    assert erased == [1, 2, 2]


# --- F3: answer discards the unfinished game --------------------------------

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


# --- integration: full game with a known secret -----------------------------

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
        if reply == "grape":  # user wipes the file between the two guesses
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