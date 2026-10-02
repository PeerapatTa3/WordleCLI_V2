"""Presentation layer for the Wordle CLI game.

This module handles menu display, user input, input validation,
and integration with the game logic and JSON persistence modules.
"""

import argparse
import os
import random

from rich.cells import cell_len
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src import history_manager
from src.data_manager import load_data, save_data
from src.game_logic import WordleGame, calculate_feedback
from src.word_bank import load_word_bank
from src.history_manager import calculate_stats
from src.board_renderer import BoardRenderer

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

console = Console()
renderer = BoardRenderer(console)

# Number of terminal lines used by the last game-screen render.
_last_render_lines = 0


def display_welcome_message():
    """Display the welcome banner for the Wordle game."""
    banner_text = "[bold cyan]🎯 WORDLE CLI GAME 🎯[/bold cyan]\n[dim]Guess the secret 5-letter word![/dim]"
    console.print(Panel(banner_text, title="[bold yellow]WELCOME[/bold yellow]", expand=False, border_style="green"))


def display_menu():
    """Display the main menu options for the user."""
    menu_text = (
        "[bold green]1.[/bold green] 🎮 Play Wordle\n"
        "[bold green]2.[/bold green] 📜 View History\n"
        "[bold green]3.[/bold green] 📊 View Statistics\n"
        "[bold green]4.[/bold green] ❓ How to Play\n"
        "[bold red]5.[/bold red] 🚪 Exit"
    )
    console.print(Panel(menu_text, title="[bold white]MAIN MENU[/bold white]", expand=False, border_style="cyan"))


def get_menu_choice():
    """Read and normalize the user's menu selection."""
    choice = console.input("[bold yellow]Choose an option (1-5): [/bold yellow]").strip().lower()
    return choice


def is_valid_guess(guess, word_length, valid_words=None):
    """Validate guess format and optionally require a word from the valid set."""
    if guess is None:
        return False
    normalized = guess.strip()
    if len(normalized) != word_length:
        return False
    if not normalized.isalpha():
        return False
    if valid_words is not None and normalized.upper() not in valid_words:
        return False
    return True


def erase_lines(n):
    """Erase the last *n* terminal lines (no-op when not a terminal)."""
    if console.is_terminal and n > 0:
        console.file.write("\033[F\033[K" * n)
        console.file.flush()


def clear_screen():
    """Clear the terminal screen (no-op when not a terminal)."""
    if console.is_terminal:
        console.clear()


def render_game_screen(board_history, attempt, max_attempts, word_length, message=None):
    """Redraw the game screen over the previous one instead of clearing the terminal."""
    global _last_render_lines

    # Render to a string first so we know how many lines it takes.
    with console.capture() as capture:
        console.print(f"[bold cyan]Attempt {attempt}/{max_attempts}[/bold cyan]\n")
        renderer.render_board(board_history, max_attempts, word_length)
        if message:
            console.print(message)
    output = capture.get()

    erase_lines(_last_render_lines)  # move up and wipe the old board
    console.file.write(output)
    console.file.flush()
    _last_render_lines = output.count("\n")


def get_guess_input(word_length, valid_words=None):
    """Prompt for a word or the supported ``hint``/``answer`` commands.

    Uses fast local validation — no network calls, no spinner.
    An invalid guess prints a single red line; on retry that line and the
    previous prompt are erased together so errors never stack.
    """
    error_shown = False
    prompt = f"Enter a {word_length}-letter word: "
    while True:
        raw = console.input(f"[bold white]{prompt}[/bold white]")
        # Long input wraps onto extra terminal rows; erase all of them.
        typed_rows = max(1, -(-(cell_len(prompt) + cell_len(raw)) // console.width))
        erase_lines(typed_rows + (1 if error_shown else 0))
        error_shown = False
        guess = raw.strip()

        if guess.lower() in {"hint", "answer"}:
            return guess.lower()

        if is_valid_guess(guess, word_length, valid_words):
            return guess.upper()

        console.print("[bold red]Invalid guess[/bold red]")
        error_shown = True


# def display_history():
#     """Show saved history grouped by game like the legacy project."""
#     history = load_data()
#     if not history:
#         console.print("[bold yellow]No guess history yet.[/bold yellow]")
#         return

#     grouped_games = {}
#     has_game_numbers = any("game_number" in record for record in history)
#     if has_game_numbers:
#         for record in history:
#             game_number = record.get("game_number", 1)
#             grouped_games.setdefault(game_number, []).append(record)
#     else:
#         grouped_games[1] = history

#     console.print(f"\n[bold cyan]Total Games Played: {len(grouped_games)}[/bold cyan]\n")
#     for game_number, records in sorted(grouped_games.items()):
#         is_won = any(record.get("correct", False) for record in records)
#         status = "[bold green]WON[/bold green]" if is_won else "[bold red]LOST[/bold red]"
#         secret_word = records[-1].get("secret_word", "UNKNOWN")
#         word_len = len(secret_word) if secret_word != "UNKNOWN" else WORD_LENGTH

#         rows = [(r.get("guess", ""), r.get("feedback", [])) for r in records]
#         table = renderer.build_history_table(rows, word_len)

#         border_color = "green" if is_won else "red"
#         console.print(Panel(
#             table,
#             title=f"[bold white]Game {game_number}[/bold white] ({status} | Secret: [bold yellow]{secret_word}[/bold yellow])",
#             expand=False,
#             border_style=border_color
#         ))


def display_statistics(history=None):
    """Display win rate, streak, and guess distribution."""
    if history is None:
        history = load_data()

    stats = calculate_stats(history)
    if not stats:
        console.print("\n[bold yellow]No stats available yet. Play a game first![/bold yellow]")
        return

    stats_table = Table(show_header=False, box=None)
    stats_table.add_column("Stat", style="bold cyan")
    stats_table.add_column("Value", style="bold white")

    stats_table.add_row("Games Played:", str(stats["total_games"]))
    stats_table.add_row("Win Rate:", f"{stats['win_rate']:.1f}%")
    stats_table.add_row("Current Streak:", str(stats["current_streak"]))

    console.print(Panel(stats_table, title="[bold yellow]PLAYER STATISTICS[/bold yellow]", expand=False, border_style="magenta"))

    console.print("\n[bold cyan]Guess Distribution:[/bold cyan]")
    for attempt, count in stats["distribution"].items():
        bar = "█" * count
        console.print(f"  [bold green]{attempt}[/bold green]: [bold green]{bar}[/bold green] ({count})")


def display_how_to_play():
    """Display the game rules and feedback marker explanations."""
    tile = BoardRenderer.tile
    rules = (
        f"1. Guess the secret {WORD_LENGTH}-letter word in {MAX_ATTEMPTS} tries.\n"
        "2. Each guess must contain letters only.\n"
        "3. Feedback markers show how close your guess is:\n"
        f"   {tile('✓', '✓')} Correct letter in the correct position.\n"
        f"   {tile('-', '-')} Correct letter in the wrong position.\n"
        f"   {tile('x', 'x')} Letter is not in the secret word.\n"
        "4. Type '[bold cyan]hint[/bold cyan]' to reveal one letter or '[bold cyan]answer[/bold cyan]' to reveal the word."
    )
    console.print(Panel(rules, title="[bold yellow]HOW TO PLAY[/bold yellow]", expand=False, border_style="blue"))


def hint_text(secret_word, revealed_positions=None):
    """Return ``(message, updated_positions)`` for the next hint (no printing)."""
    revealed_positions = set(revealed_positions or set())
    hidden_positions = [
        position for position in range(len(secret_word)) if position not in revealed_positions
    ]
    if not hidden_positions:
        return (
            f"[bold cyan]Hint: All letters are revealed. The answer is {secret_word}.[/bold cyan]",
            revealed_positions,
        )

    position = hidden_positions[0]
    revealed_positions.add(position)
    return (
        f"[bold cyan]Hint: Letter {position + 1} is '{secret_word[position]}'.[/bold cyan]",
        revealed_positions,
    )


def display_hint(secret_word, revealed_positions=None):
    """Print one new hint and return the updated revealed positions."""
    message, revealed_positions = hint_text(secret_word, revealed_positions)
    console.print(message)
    return revealed_positions


def display_answer(secret_word):
    """Reveal the current secret word for the answer command."""
    console.print(f"[bold red]Answer: {secret_word}[/bold red]")


def _next_game_number(history):
    """Return the next game number while tolerating legacy history records."""
    numbered_games = [
        record.get("game_number", 0)
        for record in history
        if isinstance(record, dict) and isinstance(record.get("game_number", 0), int)
    ]
    return max(numbered_games, default=0) + 1


def _discard_game(history, game_number):
    """Return history without the records of ``game_number`` (abandoned game)."""
    return [
        record for record in history
        if not (isinstance(record, dict) and record.get("game_number") == game_number)
    ]


def _persist(update):
    """Reload history from disk, apply ``update(history) -> history``, save it.

    Reloading right before writing means manual edits or a deleted file made
    while the game is running are respected instead of being overwritten by a
    stale in-memory copy. Returns True when the save succeeded.
    """
    return save_data(update(load_data()))


def get_secret_word(answers):
    """Return a test word when configured, otherwise pick randomly from answers."""
    test_word = os.getenv("WORDLE_TEST_WORD", "").strip().upper()
    if test_word:
        if is_valid_guess(test_word, WORD_LENGTH):
            return test_word, True
        console.print("[bold yellow]Invalid WORDLE_TEST_WORD. Using the normal word source instead.[/bold yellow]")

    secret_word = random.choice(answers)
    return secret_word, False


def play_game():
    """Run a full Wordle game round using the local word bank."""
    global _last_render_lines
    _last_render_lines = 0  # first render must not erase the menu above

    answers, valid_words = load_word_bank(WORD_LENGTH)
    if not answers:
        console.print("[bold red]No words available to play.[/bold red]")
        return

    secret_word, is_test_mode = get_secret_word(answers)
    valid_words = valid_words | {secret_word}
    game = WordleGame(secret_word, WORD_LENGTH)
    history = load_data()
    game_number = _next_game_number(history)
    revealed_positions = set()
    board_history = []

    if is_test_mode:
        console.print(f"[bold yellow][TEST MODE] Secret word: {game.secret_word}[/bold yellow]")

    save_warned = False
    attempt = 1
    message = None
    needs_render = True
    while attempt <= MAX_ATTEMPTS:
        if needs_render:
            render_game_screen(board_history, attempt, MAX_ATTEMPTS, game.word_length, message)
            message = None
        needs_render = True
        guess = get_guess_input(game.word_length, valid_words)
        if guess == "hint":
            # Print the hint below the board without redrawing it. Count the
            # extra line so the next redraw erases it together with the board.
            hint_message, revealed_positions = hint_text(game.secret_word, revealed_positions)
            console.print(hint_message)
            _last_render_lines += 1
            needs_render = False
            continue
        if guess == "answer":
            # Giving up is a testing aid: drop this game's partial records so
            # history/statistics never show an unfinished game.
            if board_history:
                _persist(lambda records: _discard_game(records, game_number))
            display_answer(game.secret_word)
            return
        feedback = calculate_feedback(guess, game.secret_word)
        is_correct = guess == game.secret_word

        record = {
            "guess": guess,
            "correct": is_correct,
            "feedback": feedback,
            "attempt": attempt,
            "game_number": game_number,
            "secret_word": game.secret_word,
        }
        if not _persist(lambda records: records + [record]) and not save_warned:
            message = "[bold yellow]Warning: could not save game history.[/bold yellow]"
            save_warned = True

        board_history.append((guess, feedback))

        if is_correct:
            render_game_screen(board_history, attempt, MAX_ATTEMPTS, game.word_length)
            console.print(Panel(
                f"[bold white on green] 🎉 CONGRATULATIONS! [/bold white on green]\n\nYou solved it in [bold yellow]{attempt}[/bold yellow] attempts!",
                title="[bold green]VICTORY[/bold green]",
                border_style="green",
                expand=False
            ))
            return

        attempt += 1

    render_game_screen(board_history, attempt - 1, MAX_ATTEMPTS, game.word_length)
    console.print(Panel(
        f"[bold white on red] 💥 GAME OVER! [/bold white on red]\n\nThe secret word was: [bold yellow]{game.secret_word}[/bold yellow]",
        title="[bold red]OUT OF TRIES[/bold red]",
        border_style="red",
        expand=False
    ))


def main(argv=None):
    """Run the CLI main loop or start a game from the command line."""
    parser = argparse.ArgumentParser(description="Play Wordle in your terminal.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("start", help="start a game immediately")
    args = parser.parse_args(argv)

    if args.command == "start":
        play_game()
        return

    display_welcome_message()
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            play_game()
        elif choice == "2":
            history_manager.group_history_by_game()
        elif choice == "3":
            display_statistics()
        elif choice == "4":
            display_how_to_play()
        elif choice == "5":
            console.print("[bold cyan]Goodbye![/bold cyan]")
            break
        else:
            console.print("[bold red]Invalid option. Please choose 1-5.[/bold red]")


if __name__ == "__main__":
    main()