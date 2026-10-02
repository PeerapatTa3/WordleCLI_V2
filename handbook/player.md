# Player Handbook

## Install and launch

Install Python 3.8 or newer, then install the game from the project folder:

```bash
python -m pip install .
```

Start the menu from any folder:

```bash
wordle
```

Start a game immediately, without the welcome screen or menu:

```bash
wordle start
```

The game ends after you solve the word, use `answer`, or run out of guesses. `wordle start` exits after that game.

Other direct commands:

```text
wordle history   Show saved games
wordle stats     Show player statistics
wordle howto     Show game instructions
wordle today     Override secret word with today's word from wordle.com
```

Use `wordle --help` for the command summary. Running `wordle` with no command opens the interactive menu.

## Play

Guess the hidden five-letter word in six attempts. Enter a valid five-letter word and press Enter. After each guess, the board marks each letter:

- `✓`: the letter is correct and in the right position.
- `-`: the letter is in the answer, but in another position.
- `x`: the letter is not in the answer, or there are no remaining copies of it.

The game uses local word lists, so guessing does not require an internet connection.

## In-game commands

- `hint`: reveal the next hidden letter without using a guess.
- `answer`: show the answer and end the game. An unfinished game is not kept in history.

The menu also offers history, statistics, and a How to Play screen.

## Saved history

Game history is saved at:

- Windows: `%USERPROFILE%\.wordle\history.json`
- macOS/Linux: `~/.wordle/history.json`

Set `WORDLE_HISTORY_PATH` to an absolute path to use another file. Set this before launching the game.

For testing only, `WORDLE_TEST_WORD` selects and displays a fixed answer when it contains a valid five-letter word. Do not set this during normal play.
