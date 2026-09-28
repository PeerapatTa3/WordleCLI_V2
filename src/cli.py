"""Presentation layer for the Wordle CLI game.

This module handles menu display, user input, input validation,
and integration with the game logic and JSON persistence modules.
"""

import os
import random
from pathlib import Path

from colorama import Fore, Style, init
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.data_manager import load_data, save_data, load_word_pool
from src.game_logic import WordleGame, calculate_feedback, search_history, filter_history
from src.word_api import fetch_random_word, fetch_valid_words, is_valid_dictionary_word

init(autoreset=True)
console = Console()

HISTORY_PATH = Path("data/history.json")
WORD_POOL_PATH = Path("data/word_pool.json")


def colorize_feedback(feedback):
    """Convert Wordle feedback markers into colored ANSI output."""
    color_map = {
        "✓": Fore.GREEN,
        "-": Fore.YELLOW,
        "x": Fore.RED,
    }

    return " ".join(f"{color_map.get(str(item), '')}{str(item)}{Style.RESET_ALL}" for item in feedback)


def _render_wordle_board(guesses, max_attempts=6, word_length=5):
    table = Table(show_header=False, show_lines=True, box=box.ROUNDED, padding=(0, 2))
    for _ in range(word_length):
        table.add_column(justify="center", min_width=5)

    for word, feedback in guesses:
        row_cells = []
        for char, fb in zip(word, feedback):
            if fb == "✓":
                row_cells.append(f"[bold white on green]  {char}  [/bold white on green]")
            elif fb == "-":
                row_cells.append(f"[bold white on yellow]  {char}  [/bold white on yellow]")
            else:
                row_cells.append(f"[bold white on bright_black]  {char}  [/bold white on bright_black]")
        table.add_row(*row_cells)

    for _ in range(max_attempts - len(guesses)):
        table.add_row(*[f"[dim white]  _  [/dim white]"] * word_length)

    console.print(Panel(table, title="[bold cyan]WORDLE BOARD[/bold cyan]", expand=False))


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
    """Validate guess format and optionally require a word from the word pool."""
    if guess is None:
        return False
    normalized = guess.strip()
    if len(normalized) != word_length:
        return False
    if not normalized.isalpha():
        return False
    if valid_words is not None and normalized.upper() not in {
        str(word).upper() for word in valid_words
    }:
        return False
    return True


def get_guess_input(word_length, valid_words=None, word_validator=None):
    """Prompt for a word or the supported ``hint``/``answer`` commands."""
    while True:
        guess = console.input(f"[bold white]Enter a {word_length}-letter word: [/bold white]").strip()
        if guess.lower() in {"hint", "answer"}:
            return guess.lower()

        with console.status("[bold cyan]Checking if the word is valid, this might take a while...[/bold cyan]", spinner="dots"):
            valid_format = is_valid_guess(guess, word_length, valid_words)
            dict_valid = (
                word_validator is not None
                and is_valid_guess(guess, word_length)
                and word_validator(guess, word_length)
            )

        if valid_format or dict_valid:
            return guess.upper()

        if valid_words is not None:
            console.print(Panel(f"[bold red]❌ Invalid guess![/bold red]\nPlease enter a {word_length}-letter valid word.", border_style="red", expand=False))
        else:
            console.print(Panel(f"[bold red]❌ Invalid guess![/bold red]\nPlease enter exactly {word_length} letters only.", border_style="red", expand=False))


def display_history():
    """Show saved history grouped by game like the legacy project."""
    history = load_data(HISTORY_PATH)
    if not history:
        console.print("[bold yellow]No guess history yet.[/bold yellow]")
        return

    grouped_games = {}
    has_game_numbers = any("game_number" in record for record in history)
    if has_game_numbers:
        for record in history:
            game_number = record.get("game_number", 1)
            grouped_games.setdefault(game_number, []).append(record)
    else:
        grouped_games[1] = history

    console.print(f"\n[bold cyan]Total Games Played: {len(grouped_games)}[/bold cyan]\n")
    for game_number, records in sorted(grouped_games.items()):
        is_won = any(record.get("correct", False) for record in records)
        status = "[bold green]WON[/bold green]" if is_won else "[bold red]LOST[/bold red]"
        secret_word = records[-1].get("secret_word", "UNKNOWN")

        table = Table(show_header=False, show_lines=True, box=box.ROUNDED, padding=(0, 1))
        word_len = len(secret_word) if secret_word != "UNKNOWN" else 5
        for _ in range(word_len):
            table.add_column(justify="center", min_width=3)

        for record in records:
            word = record.get("guess", "")
            fb_list = record.get("feedback", [])
            row_cells = []
            for char, fb in zip(word, fb_list):
                if fb == "✓":
                    row_cells.append(f"[bold white on green] {char} [/bold white on green]")
                elif fb == "-":
                    row_cells.append(f"[bold white on yellow] {char} [/bold white on yellow]")
                else:
                    row_cells.append(f"[bold white on bright_black] {char} [/bold white on bright_black]")
            table.add_row(*row_cells)

        border_color = "green" if is_won else "red"
        console.print(Panel(
            table,
            title=f"[bold white]Game {game_number}[/bold white] ({status} | Secret: [bold yellow]{secret_word}[/bold yellow])",
            expand=False,
            border_style=border_color
        ))


def display_statistics(history=None):
    """Display win rate, streak, and guess distribution from saved history."""
    if history is None:
        history = load_data(HISTORY_PATH)

    if not history:
        console.print("\n[bold yellow]No stats available yet. Play a game first![/bold yellow]")
        return

    grouped_games = {}
    has_game_numbers = any("game_number" in record for record in history)
    if has_game_numbers:
        for record in history:
            game_number = record.get("game_number", 1)
            grouped_games.setdefault(game_number, []).append(record)
    else:
        grouped_games[1] = history

    games = [grouped_games[key] for key in sorted(grouped_games)]
    wins = [any(record.get("correct", False) for record in game) for game in games]
    total_games = len(games)
    win_count = sum(wins)
    win_rate = win_count / total_games * 100

    current_streak = 0
    for won in reversed(wins):
        if not won:
            break
        current_streak += 1

    stats_table = Table(show_header=False, box=None)
    stats_table.add_column("Stat", style="bold cyan")
    stats_table.add_column("Value", style="bold white")

    stats_table.add_row("Games Played:", str(total_games))
    stats_table.add_row("Win Rate:", f"{win_rate:.1f}%")
    stats_table.add_row("Current Streak:", str(current_streak))

    console.print(Panel(stats_table, title="[bold yellow]PLAYER STATISTICS[/bold yellow]", expand=False, border_style="magenta"))

    console.print("\n[bold cyan]Guess Distribution:[/bold cyan]")
    for attempt in range(1, 7):
        count = sum(
            1
            for game in games
            if any(record.get("correct") and record.get("attempt") == attempt for record in game)
        )
        bar = "█" * count
        console.print(f"  [bold green]{attempt}[/bold green]: [bold green]{bar}[/bold green] ({count})")


def display_how_to_play():
    """Display the game rules and feedback marker explanations."""
    rules = (
        "1. Guess the secret 5-letter word in 6 tries.\n"
        "2. Each guess must contain letters only.\n"
        "3. Feedback markers show how close your guess is:\n"
        "   [bold white on green]  ✓  [/bold white on green] Correct letter in the correct position.\n"
        "   [bold white on yellow]  -  [/bold white on yellow] Correct letter in the wrong position.\n"
        "   [bold white on bright_black]  x  [/bold white on bright_black] Letter is not in the secret word.\n"
        "4. Type '[bold cyan]hint[/bold cyan]' to reveal one letter or '[bold cyan]answer[/bold cyan]' to reveal the word."
    )
    console.print(Panel(rules, title="[bold yellow]HOW TO PLAY[/bold yellow]", expand=False, border_style="blue"))


def display_hint(secret_word, revealed_positions=None):
    """Reveal one new secret-word position and return the updated positions."""
    revealed_positions = set(revealed_positions or set())
    hidden_positions = [
        position for position in range(len(secret_word)) if position not in revealed_positions
    ]
    if not hidden_positions:
        console.print(f"[bold cyan]Hint: All letters are revealed. The answer is {secret_word}.[/bold cyan]")
        return revealed_positions

    position = hidden_positions[0]
    revealed_positions.add(position)
    console.print(f"[bold cyan]Hint: Letter {position + 1} is '{secret_word[position]}'.[/bold cyan]")
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


def get_secret_word(pool):
    """Return a test word when configured, otherwise use API/local fallback."""
    test_word = os.getenv("WORDLE_TEST_WORD", "").strip().upper()
    if test_word:
        if is_valid_guess(test_word, 5):
            return test_word, True
        console.print("[bold yellow]Invalid WORDLE_TEST_WORD. Using the normal word source instead.[/bold yellow]")

    secret_word = fetch_random_word(5)
    if not secret_word:
        secret_word = random.choice(pool)
    return secret_word, False


def play_game():
    """Run a full Wordle game round using the current word pool."""
    pool = load_word_pool(WORD_POOL_PATH)
    if not pool:
        console.print("[bold red]No words available to play. Please add words to the pool.[/bold red]")
        return

    secret_word, is_test_mode = get_secret_word(pool)
    game = WordleGame(secret_word)
    history = load_data(HISTORY_PATH)
    game_number = _next_game_number(history)
    valid_words = set(fetch_valid_words(game.word_length))
    valid_words.update(pool)
    valid_words.add(secret_word)
    revealed_positions = set()
    board_history = []

    console.print(f"\n[bold green]New game started! Secret word is {game.word_length} letters long.[/bold green]")
    if is_test_mode:
        console.print(f"[bold yellow][TEST MODE] Secret word: {game.secret_word}[/bold yellow]")

    attempt = 1
    while attempt <= 6:
        guess = get_guess_input(game.word_length, valid_words, is_valid_dictionary_word)
        if guess == "hint":
            revealed_positions = display_hint(game.secret_word, revealed_positions)
            continue
        if guess == "answer":
            display_answer(game.secret_word)
            return
        feedback = calculate_feedback(guess, game.secret_word)
        is_correct = guess == game.secret_word

        history.append({
            "guess": guess,
            "correct": is_correct,
            "feedback": feedback,
            "attempt": attempt,
            "game_number": game_number,
            "secret_word": game.secret_word,
        })
        save_data(HISTORY_PATH, history)

        board_history.append((guess, feedback))
        _render_wordle_board(board_history, max_attempts=6, word_length=game.word_length)

        if is_correct:
            console.print(Panel(
                f"[bold white on green] 🎉 CONGRATULATIONS! [/bold white on green]\n\nYou solved it in [bold yellow]{attempt}[/bold yellow] attempts!",
                title="[bold green]VICTORY[/bold green]",
                border_style="green",
                expand=False
            ))
            return

        console.print(f"[bold cyan]Attempt {attempt}/6[/bold cyan]\n")
        attempt += 1

    console.print(Panel(
        f"[bold white on red] 💥 GAME OVER! [/bold white on red]\n\nThe secret word was: [bold yellow]{game.secret_word}[/bold yellow]",
        title="[bold red]OUT OF TRIES[/bold red]",
        border_style="red",
        expand=False
    ))


def main():
    """Run the CLI main loop."""
    display_welcome_message()
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            play_game()
        elif choice == "2":
            display_history()
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