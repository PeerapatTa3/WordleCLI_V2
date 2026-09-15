"""Presentation layer for the Wordle CLI game.

This module handles menu display, user input, input validation,
and integration with the game logic and JSON persistence modules.
"""

import random
from pathlib import Path

from colorama import Fore, Style, init

from src.data_manager import load_data, save_data, load_word_pool, save_word_pool
from src.game_logic import WordleGame, calculate_feedback, search_history, filter_history
from src.word_api import fetch_random_word


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
    print("            WORDLE CLI GAME")
    print("========================================\n")


def display_menu():
    """Display the main menu options for the user."""
    print("1. Play Wordle")
    print("2. View History")
    print("3. Remove Word")
    print("4. Exit")


def get_menu_choice():
    """Read and normalize the user's menu selection."""
    choice = input("Choose an option (1-4): ").strip().lower()
    return choice


def is_valid_guess(guess, word_length):
    """Validate a guess based on string length and alphabetic content."""
    if guess is None:
        return False
    normalized = guess.strip()
    if len(normalized) != word_length:
        return False
    if not normalized.isalpha():
        return False
    return True


def get_guess_input(word_length):
    """Prompt the user until a valid guess is entered."""
    while True:
        guess = input(f"Enter a {word_length}-letter word: ").strip()
        if is_valid_guess(guess, word_length):
            return guess.upper()
        print(f"Invalid guess. Please enter exactly {word_length} letters only.")


def display_history():
    """Show stored guess history from the JSON file."""
    history = load_data(HISTORY_PATH)
    if not history:
        print("No guess history yet.")
        return

    print("\nGuess History:")
    for index, record in enumerate(history, start=1):
        guess = record.get("guess", "")
        correct = record.get("correct", False)
        feedback = record.get("feedback", [])
        print(f"{index}. {guess} | correct={correct} | feedback={feedback}")


def remove_word_from_pool():
    """Remove a word from the pool and save the updated list."""
    pool = load_word_pool(WORD_POOL_PATH)
    if not pool:
        print("Word pool is empty.")
        return

    print("Current word pool:")
    for index, word in enumerate(pool, start=1):
        print(f"{index}. {word}")

    word_to_remove = input("Enter a word to remove (or 'cancel'): ").strip().upper()
    if word_to_remove.lower() == "cancel":
        return

    if word_to_remove in pool:
        pool.remove(word_to_remove)
        save_word_pool(WORD_POOL_PATH, pool)
        print(f"Removed '{word_to_remove}' from the word pool.")
    else:
        print("Word not found in the pool.")


def play_game():
    """Run a full Wordle game round using the current word pool."""
    pool = load_word_pool(WORD_POOL_PATH)
    if not pool:
        print("No words available to play. Please add words to the pool.")
        return

    secret_word = fetch_random_word(5)
    if not secret_word:
        secret_word = random.choice(pool)
    game = WordleGame(secret_word)
    history = load_data(HISTORY_PATH)

    print(f"\nNew game started! Secret word is {game.word_length} letters long.")
    for attempt in range(1, 7):
        guess = get_guess_input(game.word_length)
        feedback = calculate_feedback(guess, game.secret_word)
        is_correct = guess == game.secret_word

        history.append({
            "guess": guess,
            "correct": is_correct,
            "feedback": feedback,
            "attempt": attempt,
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
            remove_word_from_pool()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()
