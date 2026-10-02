# Developer Handbook

## Set up

Use Python 3.8 or newer. From the repository root, create and activate a virtual environment, then install the project with its development dependency:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

On macOS/Linux, activate with `source .venv/bin/activate` instead. For a regular, non-editable install, use `python -m pip install .`.

The package uses Hatchling. Its console scripts are declared in `pyproject.toml`:

- `wordle` and `wordle start` call `src.cli:main`.
- `run-app` is a compatibility alias for the same entry point.

The CLI also supports `history`, `stats`, `howto`, and `help` subcommands. With no subcommand, `main()` opens the interactive menu. `handle_command_line_args()` owns parsing and dispatch; it returns whether a command was handled so the menu does not run afterward.

## Project layout

- `src/cli.py`: menu, prompts, game loop, and command-line entry point.
- `src/board_renderer.py`: board and feedback rendering.
- `src/game_logic.py`: game model and feedback calculation.
- `src/history_manager.py`: history grouping, search/filter, and statistics calculations.
- `src/data_manager.py`: JSON history persistence.
- `src/word_bank.py`: local answer and guess-word loading.
- `src/data/`: packaged `answers.txt` and `valid_words.txt`.
- `scripts/`: build-time utilities; these are not required to play.
- `tests/`: pytest tests.

Keep user history outside the installed package. By default it is `~/.wordle/history.json`; `WORDLE_HISTORY_PATH` overrides it. The path is resolved when `src.data_manager` is imported, so set the environment variable before starting Python.

## Common tasks

Run the tests:

```bash
python -m pytest -q
```

Build replacement word lists from a source text file containing one word per line. The default output is `src/data/`:

```bash
python scripts/build_wordlists.py path/to/source-words.txt
```

Choose another output directory with `-o`:

```bash
python scripts/build_wordlists.py path/to/source-words.txt -o src/data
```

Create a non-editable wheel install with `python -m pip install .`. The wheel includes the package word lists and excludes the history snapshot.

## Design notes

- Runtime word validation is local and does not call a network service.
- Keep presentation in `cli.py` / `board_renderer.py`, game rules in `game_logic.py`, and persistence/statistics in their data and history modules.
- `WORDLE_TEST_WORD` is a test aid that prints the chosen answer. Avoid relying on it in normal play.

## Test status

Run `python -m pytest -q` from the repository root. The full suite passed **80 tests** after the CLI subcommands and history display were wired up.
