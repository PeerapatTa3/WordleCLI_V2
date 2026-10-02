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