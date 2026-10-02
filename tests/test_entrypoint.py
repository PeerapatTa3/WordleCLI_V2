import pytest

import src.cli as cli


def test_main_start_runs_game_without_menu_or_banner(monkeypatch):
    calls = []
    monkeypatch.setattr(cli, "display_welcome_message", lambda: calls.append("welcome"))
    monkeypatch.setattr(cli, "display_menu", lambda: calls.append("menu"))
    monkeypatch.setattr(cli, "play_game", lambda: calls.append("game"))

    cli.main(["start"])

    assert calls == ["game"]


def test_main_without_arguments_shows_menu(monkeypatch):
    calls = []
    monkeypatch.setattr(cli, "display_welcome_message", lambda: calls.append("welcome"))
    monkeypatch.setattr(cli, "display_menu", lambda: calls.append("menu"))
    monkeypatch.setattr(cli, "get_menu_choice", lambda: "5")

    cli.main([])

    assert calls == ["welcome", "menu"]


@pytest.mark.parametrize(
    ("command", "target"),
    [
        ("history", "display_history"),
        ("stats", "display_statistics"),
        ("howto", "display_how_to_play"),
    ],
)
def test_main_command_runs_without_entering_menu(monkeypatch, command, target):
    calls = []
    monkeypatch.setattr(cli, target, lambda: calls.append(target))
    monkeypatch.setattr(cli, "display_welcome_message", lambda: calls.append("welcome"))
    monkeypatch.setattr(cli, "display_menu", lambda: calls.append("menu"))

    cli.main([command])

    assert calls == [target]


def test_main_today_uses_api_word_for_game(monkeypatch):
    calls = []
    monkeypatch.setattr(cli, "today_word", lambda: "GRAPE")
    monkeypatch.setattr(cli, "play_game", lambda secret_word_override=None: calls.append(secret_word_override))
    monkeypatch.setattr(cli, "display_welcome_message", lambda: calls.append("welcome"))
    monkeypatch.setattr(cli, "display_menu", lambda: calls.append("menu"))

    cli.main(["today"])

    assert calls == ["GRAPE"]


def test_main_help_command_prints_usage_without_entering_menu(monkeypatch, capsys):
    monkeypatch.setattr(cli, "display_menu", lambda: pytest.fail("menu should not run"))

    cli.main(["help"])

    assert "usage:" in capsys.readouterr().out


def test_main_unknown_command_shows_usage(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(["unknown"])

    assert error.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_main_help_shows_usage(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(["--help"])

    assert error.value.code == 0
    assert "usage:" in capsys.readouterr().out