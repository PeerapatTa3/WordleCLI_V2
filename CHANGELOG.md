# Changelog

All notable changes to the Wordle CLI V.2 project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v0.1.0] - Sprint 1: Front-End App Dev & CLI Validation
### Added
- Initialized the CLI project structure for Wordle V.2.
- Created the presentation layer in `cli.py` for welcome banner, menu display, and input handling.
- Added the main entry point in `game.py`.
- Implemented defensive input normalization with `.strip().lower()` for menu choices.
- Added guess validation for 5-letter alphabetic input only.
- Created automated tests in `tests/test_cli.py` for valid and invalid input cases.
- Added dependency configuration in `requirements.txt`.

### Changed
- Updated the project README to reflect the V.2 repository and Sprint 1 scope.
- Clarified the project roadmap based on [PLAN.md](./PLAN.md).

### Planner / Coder / Debugger Roles
- **Planner / PM (เทน):** Defined Sprint 1 scope, CLI requirements, and validation rules.
- **Coder (ซอก):** Implemented the menu flow and the core CLI functions.
- **Debugger / QA (พี):** Created unit tests for input validation and verified edge-case behavior.

---

## [v0.2.0] - Sprint 2: Business Logic & Data Access
### Added
- `WordleGame` domain model and `calculate_feedback()` in `src/game_logic.py` (duplicate-letter aware).
- `search_history()` and `filter_history()` for guess history.
- JSON persistence in `src/data_manager.py` (`save_data` / `load_data`) that never crashes on missing or corrupted files.
- Statistics (win rate, streak, guess distribution) with per-game numbering in history records.
- Legacy-compatible grouped history view (game status, secret word, guess sequence) and `How to Play` menu.
- In-game `hint` and `answer` commands.
- Optional `WORDLE_TEST_WORD` mode for testing with a known secret word.
- Automated tests for duplicate-letter feedback, corrupted JSON, and persistence round-trips.

### Changed
- Word validation moved from "any 5 letters" to "must be a known word".

### Note
- Sprint 2 originally validated words through the Datamuse and Dictionary APIs. That design was
  replaced in Sprint 3 (see below).

---

## [v0.3.0] - Sprint 3: Full Integration, Offline-First Words, In-Place Redraw
### Added
- `src/word_bank.py`: `load_word_bank()` returns `(answers, valid_words)` from local files
  (`data/answers.txt`, `data/valid_words.txt`), resolved from `Path(__file__)`, with a built-in default pool.
- `src/board_renderer.py` (`BoardRenderer`): shared tile/table rendering for the live board, history, and legend.
- `src/history_manager.py`: history grouping and `calculate_stats()` extracted from the CLI.
- In-place redraw helpers `erase_lines()`, `clear_screen()`, `render_game_screen()` (no-ops when output is not a terminal).
- `hint_text()` pure function; hint messages now stay visible under the board.
- `MAX_ATTEMPTS` and `WORD_LENGTH` constants.
- `tests/test_word_bank.py`, `tests/test_boardrenderer.py`, `tests/test_sprint3.py`.

### Changed
- **Offline-first:** the secret word and guess validation use local files only. No network calls at runtime;
  guess checking is an instant `set` lookup instead of a 3-10 second Dictionary API call.
- `src/word_api.py` no longer serves the game; the Datamuse/Dictionary helpers live in `scripts/` as build-time tools.
- Invalid guesses print a single error line that is replaced on retry instead of stacking.
- `answer` now discards the unfinished game's records so history and statistics never show an incomplete game.
- History is reloaded from disk before every write, so manual edits or a deleted file are respected.
- `HISTORY_PATH` is resolved from `Path(__file__)` instead of the current working directory.
- `load_data()` returns `[]` unless the file contains a JSON list, and drops non-dict records.
- A failed history save shows a warning instead of failing silently.

### Removed
- Dead `colorize_feedback()` and the `colorama` dependency.
- Runtime use of `data/word_pool.json` (file retired).
- Per-guess Dictionary API validation, retry, and cache.

### Fixed
- Hint text was erased by the next screen redraw.
- Consecutive invalid guesses stacked error lines.
- `answer` left orphan games in `history.json`.
- Running the game from another directory created a second history file.

---

## [Unreleased] - UI Enhancement: Rich-based Presentation Layer
### Added
- `rich` dependency; bordered Panel/Table rendering for the welcome banner, menu, board, history, statistics, and rules.

### Changed
- Replaced plain `print()`/`input()` in `cli.py` with `rich.console.Console` (`console.print` / `console.input`).
- `View History` renders each past game as a colored letter grid; statistics use a Panel table with green bars.

---

## [v1.0.0] - Sprint Final: CI/CD & AI Integration (Planned)
### Planned
- Add automated CI workflow through GitHub Actions (lint + tests on push/PR).
- Coverage reporting.
- Extend AI or automation features such as gameplay statistics, smart word hints, or suggestion logic.
- Global `wordle` / `wordle start` command via `pyproject.toml`.
- Finalize presentation slides and project documentation.