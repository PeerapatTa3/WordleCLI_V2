# Refactoring and Technical Notes — Wordle CLI V.2

**Project:** Wordle CLI V.2  
**Sprint:** Sprint 4 (Sprint Final)  
**Deliverable:** Architecture, Refactoring Alternatives & Technical Problem Analysis

---

## 1. Overview

In Sprint 4 (Sprint Final), Wordle CLI V.2 transitioned from a local script into a production-grade installable CLI package (`pip install .`) with automated CI/CD pipelines, strict code quality gates (Flake8), and comprehensive unit testing (93 tests, 93.46% coverage).

This document analyzes the architectural decisions made during development, compares the alternatives considered against what was built, evaluates future class extraction candidates, and summarizes technical challenges solved across Sprints 1–4.

---

## 2. Comparison of Technical Alternatives

### 2.1 Word Validation: Runtime API vs. Offline-First Set Lookup

| Dimension | Alternative A: Runtime API Validation (Sprint 2) | Alternative B: Offline-First Set Lookup (Sprint 3–4, Chosen) |
|---|---|---|
| **Mechanism** | Query Datamuse / Dictionary API per guess over HTTP | Pre-built local text files loaded into in-memory `frozenset` |
| **Response Latency** | 3,000 ms – 10,000 ms per guess (network dependent) | **< 1 ms** instant lookup (`O(1)` hash set) |
| **Network Requirement** | Requires constant, active internet connection | **Zero network usage** during gameplay |
| **Failure Modes** | DNS failure, API rate limits, timeouts, service outages | Handled by graceful fallback to built-in `DEFAULT_WORD_POOL` |
| **Determinism** | External API dictionary changes could break reproducibility | 100% deterministic; covered by offline automated tests |
| **Verdict** | **Discarded:** Latency destroyed gameplay UX and CI tests hanged | **Adopted:** Instant, offline, and rock-solid reliability |

#### Verification Evidence:
- `tests/test_word_bank.py::test_load_word_bank_makes_no_network_calls` patches `socket.connect` to raise an exception, proving that loading and playing never trigger network I/O.
- Test suites run in ~2.5 seconds for all 93 tests without network flakiness.

---

### 2.2 Project Structure: Monolithic CLI vs. 3-Tier Layered Architecture

| Dimension | Monolithic CLI (`game.py` only) | 3-Tier Layered Architecture (Chosen) |
|---|---|---|
| **Separation** | UI, game rules, and JSON I/O mixed together | Presentation (`cli`, `board_renderer`), Business (`game_logic`, `history_manager`), Data (`data_manager`, `word_bank`) |
| **Maintainability** | High coupling; small changes cause side-effects | High cohesion; changes to rendering do not affect game scoring |
| **Testability** | Requires mocking terminal `print` / `input` for everything | Business logic functions are pure and tested without UI mocks |
| **Extensibility** | Difficult to add new subcommands or entry points | Easily supported `wordle start`, `wordle today`, `wordle stats` |

---

### 2.3 Packaging & Data Layout: Root Files vs. Package Data

When creating the installable package (`pyproject.toml`):
- **Option 1 (Chosen):** Move runtime word lists into `src/data/` (`answers.txt` and `valid_words.txt`) and configure Hatchling to package `src`.
  - *Rationale:* When a user installs the package via `pip install .` in any environment, package data files are bundled inside the wheel and accessible via `importlib.resources` or relative module paths (`Path(__file__).parent / "data"`).
  - *Root directory copies:* Retained in `data/` for backward compatibility with checkout-based scripts.
- **Option 2 (Rejected):** Keep word lists strictly in root `data/` and require editable installs (`pip install -e .`).
  - *Rationale for Rejection:* Fails when installed as a global CLI tool across arbitrary directories.

---

### 2.4 History Persistence Location: CWD vs. User Home Directory

- **Sprint 1–2 Issue:** History was written to `./history.json` relative to the current working directory. Launching the game from `C:\` or `D:\` created scattered `history.json` files.
- **Sprint 3 Fix:** Resolved relative to `Path(__file__)`. While better, this risked writing into protected site-packages when installed globally.
- **Sprint 4 Final Decision:** History is saved to a dedicated per-user directory:
  - Windows: `%USERPROFILE%\.wordle\history.json`
  - Linux/macOS: `~/.wordle/history.json`
  - Environment override: `WORDLE_HISTORY_PATH` allows test fixtures to use isolated temporary files without touching real player history.

---

## 3. Analysis of Class Extraction Candidates

During Sprint 3 and 4 retrospectives, three candidates for further Object-Oriented extraction were evaluated:

### 3.1 `HistoryRepository`
- **What it would own:** Encapsulating `HISTORY_PATH`, `load_data()`, `save_data()`, `_next_game_number()`, `_discard_game()`, and `_persist()`.
- **Potential benefit:** Eliminates global functions in `data_manager.py` and decouples file handling from `cli.py`.
- **Why it was deferred:** The functional approach (`history_manager.py` for calculations + `data_manager.py` for persistence) is already clean, thoroughly tested (89% coverage on history manager), and simple. Adding an extra repository abstraction layer would introduce unnecessary boilerplate without improving testability.

### 3.2 `GameSession`
- **What it would own:** Managing the loop state of an active match: secret word, attempt counter, guesses, feedback history, hint state, and status (IN_PROGRESS, WON, LOST).
- **Potential benefit:** Encapsulates the local variables inside `play_game()` in `cli.py` (`board_history`, `game_number`, `hint_count`).
- **Why it was deferred:** `WordleGame` in `src/game_logic.py` already encapsulates the domain model (`secret_word`, `attempts`, `evaluate_guess`). Expanding it into a full session object can be implemented in a future release if GUI or multiplayer modes are added.

### 3.3 `ConsoleUI`
- **What it would own:** All Rich console interactions, panels, tables, and terminal cursor control (`erase_lines`, `clear_screen`).
- **Potential benefit:** Further separates Rich presentation logic from CLI flow control.
- **Current status:** Partially realized via `BoardRenderer` in `src/board_renderer.py`. Retaining straightforward helper functions in `cli.py` keeps the CLI entry point simple and easy for script programming students to follow.

---

## 4. Summary of Technical Problems Solved (Sprints 1–4)

| Problem Encountered | Sprint | Root Cause | Solution Implemented |
|---|---|---|---|
| **Stacked terminal boards & errors** | Sprint 1–3 | Standard `print()` scrolled down on each guess or invalid input | Implemented `erase_lines()` ANSI cursor repositioning and `render_game_screen()` in-place redraw (with non-terminal no-op fallback). |
| **Duplicate letters feedback bug** | Sprint 2 | Naive matching marked identical letters green and yellow improperly | Implemented two-pass feedback calculation in `calculate_feedback()`: first pass assigns exact `✓`, second pass accounts for remaining unmatched counts `-`. |
| **API latency & network hang** | Sprint 2–3 | Calling Dictionary API on every guess took 3–10s and hung on outages | Replaced with local offline-first word lists (`1,984` answers, `8,636` valid words) in `src/word_bank.py` with `O(1)` set lookup. |
| **Stale in-memory history overwrite** | Sprint 3 | Keeping history in memory overwrote changes if the user edited or deleted `history.json` | `_persist()` re-reads disk history immediately before writing, preventing stale state overwrites. |
| **CWD-dependent file paths** | Sprint 3–4 | Relative paths broke when running from another working directory | Used `Path(__file__)` for package assets and `~/.wordle/history.json` for persistent user history. |
| **Hint redraw testing mismatch** | Sprint 3 | Test checked internal `message=` argument while CLI printed directly under board | Updated test assertion to verify player-visible output captured by `capsys`. |
| **Flake8 lint failures across modules** | Sprint 4 | Unused imports, lines > 120 chars, trailing whitespaces, and missing newlines | Cleaned all 31 findings across `scripts/`, `src/`, and `tests/` without using suppressions. |
| **CI test isolation** | Sprint 4 | Tests could accidentally read/write real player history | Patched `data_manager.HISTORY_PATH` to `tmp_path` in all tests and removed tracked `data/history.json`. |
