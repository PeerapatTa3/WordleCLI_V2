"""Presentation layer for the Wordle CLI game.

This module handles menu display, user input, input validation,
and integration with the game logic and JSON persistence modules.
"""

import os
import random
from pathlib import Path

from colorama import Fore, Style, init

from src.data_manager import load_data, save_data, load_word_pool
from src.game_logic import WordleGame, calculate_feedback, search_history, filter_history
from src.word_api import fetch_random_word, fetch_valid_words, is_valid_dictionary_word


init(autoreset=True)
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


def display_welcome_message():
    """Display the welcome banner for the Wordle game."""
    print("\n========================================")
    print("                WELCOME")
    print("                  TO")
    print("            WORDLE CLI GAME")
    print("========================================\n")


def display_menu():
    """Display the main menu options for the user."""
    print("1. Play Wordle")
    print("2. View History")
    print("3. View Statistics")
    print("4. How to Play")
    print("5. Exit")


def get_menu_choice():
    """Read and normalize the user's menu selection."""
    choice = input("Choose an option (1-5): ").strip().lower()
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
        guess = input(f"Enter a {word_length}-letter word: ").strip()
        if guess.lower() in {"hint", "answer"}:
            return guess.lower()
        if is_valid_guess(guess, word_length, valid_words) or (
            word_validator is not None
            and is_valid_guess(guess, word_length)
            and word_validator(guess, word_length)
        ):
            return guess.upper()
        if valid_words is not None:
            print(f"Invalid guess. Enter a {word_length}-letter valid word")
        else:
            print(f"Invalid guess. Please enter exactly {word_length} letters only.")


def display_history():
    """Show saved history grouped by game like the legacy project."""
    history = load_data(HISTORY_PATH)
    if not history:
        print("No guess history yet.")
        return

    grouped_games = {}
    has_game_numbers = any("game_number" in record for record in history)
    if has_game_numbers:
        for record in history:
            game_number = record.get("game_number", 1)
            grouped_games.setdefault(game_number, []).append(record)
    else:
        grouped_games[1] = history

    print(f"\nTotal Games Played: {len(grouped_games)}")
    for game_number, records in sorted(grouped_games.items()):
        is_won = any(record.get("correct", False) for record in records)
        status = "WON" if is_won else "LOST"
        secret_word = records[-1].get("secret_word", "UNKNOWN")
        guesses = [record.get("guess", "") for record in records]
        print(f"\nGame {game_number} ({status}, secret: {secret_word})")
        print(f"  Guesses: {' -> '.join(guesses)}")


def display_statistics(history=None):
    """Display win rate, streak, and guess distribution from saved history."""
    if history is None:
        history = load_data(HISTORY_PATH)

    if not history:
        print("\nNo stats available yet. Play a game first!")
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

    print("\n=======================================")
    print("           PLAYER STATISTICS")
    print("=======================================")
    print(f"Games Played:    {total_games}")
    print(f"Win Rate:        {win_rate:.1f}%")
    print(f"Current Streak:  {current_streak}")
    print("\nGuess Distribution:")

    for attempt in range(1, 7):
        count = sum(
            1
            for game in games
            if any(record.get("correct") and record.get("attempt") == attempt for record in game)
        )
        print(f"  {attempt}: {'█' * count} ({count})")


def display_how_to_play():
    """Display the game rules and feedback marker explanations."""
    print("\n=======================================")
    print("             HOW TO PLAY")
    print("=======================================")
    print("1. Guess the secret 5-letter word in 6 tries.")
    print("2. Each guess must contain letters only.")
    print("3. Feedback markers show how close your guess is:")
    print("   ✓ Correct letter in the correct position.")
    print("   - Correct letter in the wrong position.")
    print("   x Letter is not in the secret word.")
    print("4. Type 'hint' to reveal one letter or 'answer' to reveal the word.")


def display_hint(secret_word, revealed_positions=None):
    """Reveal one new secret-word position and return the updated positions."""
    revealed_positions = set(revealed_positions or set())
    hidden_positions = [
        position for position in range(len(secret_word)) if position not in revealed_positions
    ]
    if not hidden_positions:
        print(f"Hint: All letters are revealed. The answer is {secret_word}.")
        return revealed_positions

    position = hidden_positions[0]
    revealed_positions.add(position)
    print(f"Hint: Letter {position + 1} is '{secret_word[position]}'.")
    return revealed_positions


def display_answer(secret_word):
    """Reveal the current secret word for the answer command."""
    print(f"Answer: {secret_word}")


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
        print("Invalid WORDLE_TEST_WORD. Using the normal word source instead.")

    secret_word = fetch_random_word(5)
    if not secret_word:
        secret_word = random.choice(pool)
    return secret_word, False


def play_game():
    """Run a full Wordle game round using the current word pool."""
    pool = load_word_pool(WORD_POOL_PATH)
    if not pool:
        print("No words available to play. Please add words to the pool.")
        return

    secret_word, is_test_mode = get_secret_word(pool)
    game = WordleGame(secret_word)
    history = load_data(HISTORY_PATH)
    game_number = _next_game_number(history)
    valid_words = set(fetch_valid_words(game.word_length))
    valid_words.update(pool)
    valid_words.add(secret_word)
    revealed_positions = set()

    print(f"\nNew game started! Secret word is {game.word_length} letters long.")
    if is_test_mode:
        print(f"[TEST MODE] Secret word: {game.secret_word}")
    for attempt in range(1, 7):
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

        print(f"Feedback: {colorize_feedback(feedback)}")

        if is_correct:
            print(f"Congratulations! You solved it in {attempt} attempts.")
            return

        print(f"Attempt {attempt}/6")

    print(f"Game over! The word was: {game.secret_word}")


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
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
