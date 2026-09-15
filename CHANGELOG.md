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
- Created `src/game_logic.py` containing `WordleGame`, `calculate_feedback()`, `search_history()`, and `filter_history()`.
- Added JSON persistence logic in `src/data_manager.py`.
- Added default word pool and fallback behavior for missing or empty data files.
- Implemented save/load flow for guess history and word-pool data.
- Created tests for logic and data handling in `tests/test_logic.py`.

### Changed
- Integrated the game loop in `cli.py` so it now plays a real Wordle round using the word pool and saves history.
- Added `remove_word_from_pool()` and `display_history()` actions to the menu flow.
- Added colorized feedback output for Wordle results via `colorama`.

### Notes
- `data/history.json` and `data/word_pool.json` are now used as persistent game state.
- A live API fallback is also available through `src/word_api.py` for fetching 5-letter words when external connectivity is available.
- Expanded automated tests to cover duplicate-letter feedback, corrupted JSON, API validation, network failure, and duplicate word removal.
- Latest verification result: `20 passed`.

---

## [v0.3.0] - Sprint 3: Full Integration (In Progress)
### Planned
- Connect all layers more tightly under one consistent state manager.
- Improve synchronization across game rounds and menu navigation.
- Handle empty pool, corrupted files, and mid-session data changes gracefully.

---

## [v1.0.0] - Sprint Final: CI/CD & AI Integration (Planned)
### Planned
- Add automated CI workflow through GitHub Actions.
- Extend AI or automation features such as gameplay statistics, smart word hints, or suggestion logic.
- Finalize presentation slides and project documentation.
