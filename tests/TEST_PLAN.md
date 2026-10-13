# Test Plan & Test Cases — Wordle CLI V.2

**Project:** Wordle CLI V.2  
**Scope:** Sprint 1-4 (Sprint Final)  
**Test Tool:** `pytest`, `pytest-cov`, `flake8`  
**Latest Result:** `93 tests — 93 passed (100%), 93.46% coverage, 0 lint findings` (รันล่าสุดเมื่อ 2026-10-05)

## 1. Test Objectives

- Verify the CLI accepts valid commands and rejects invalid input without crashing.
- Verify Wordle business logic calculates exact, misplaced, and absent letters correctly.
- Verify history data is loaded and saved safely with JSON, including wrong-type and corrupted files.
- Verify the local word bank loads, falls back to defaults, and never touches the network.
- Verify the in-place redraw helpers and that all integrated menus and in-game commands work together.
- Verify the global CLI command `wordle` and subcommands (`start`, `today`, `history`, `stats`, `howto`, `help`).
- Verify GitHub Actions CI matrix builds and enforce coverage gate ≥ 80%.

## 2. Test Environment

- Python 3.12 / 3.13 (Windows และ Linux / Ubuntu)
- Virtual environment: `.venv`
- Dependencies: `rich`, `requests`, `pytest`, `pytest-cov`, `flake8`
- Test command:

```text
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

## 3. Sprint 1 Test Plan — Front-End App Dev

### Test Cases

| ID | Test Case | Input | Expected Result | Status |
|---|---|---|---|---|
| S1-T01 | Display welcome banner | Start `game.py` | Welcome banner appears | PASS |
| S1-T02 | Display menu | Call `display_menu()` | Five menu options appear | PASS |
| S1-T03 | Normalize menu input | `  PLAY  ` | Returns `play` | PASS |
| S1-T04 | Reject short guess | `APP` | Guess is rejected | PASS |
| S1-T05 | Reject non-letter guess | `APP1E` | Guess is rejected | PASS |
| S1-T06 | Reject spaces | `APP LE` | Guess is rejected | PASS |
| S1-T07 | Accept lowercase valid word | `apple` | Returns `APPLE` | PASS |
| S1-T08 | Accept hint command | `hint` | Returns `hint` without consuming an attempt | PASS |
| S1-T09 | Accept answer command | `answer` | Shows answer and ends the round | PASS |

### Edge Cases

- Empty menu input
- Unknown menu option such as `0` or `abc`
- Leading/trailing spaces
- Mixed uppercase/lowercase input
- Empty guess, short guess, long guess
- Numbers, symbols, and spaces inside a guess

## 4. Sprint 2 Test Plan — Back-End App Dev

### Test Cases

| ID | Test Case | Input | Expected Result | Status |
|---|---|---|---|---|
| S2-T01 | Exact feedback | `APPLE` vs `APPLE` | All markers are `✓` | PASS |
| S2-T02 | Mixed feedback | `AERIE` vs `APPLE` | Correct `✓`, `-`, and `x` markers | PASS |
| S2-T03 | Duplicate letters | `ALLEY` vs `APPLE` | Duplicate matches are counted correctly | PASS |
| S2-T04 | Search history | Keyword `pear` | Matching history is returned | PASS |
| S2-T05 | Filter correct guesses | Condition `correct` | Only correct records are returned | PASS |
| S2-T06 | Save/load JSON | Temporary history file | Saved data loads unchanged | PASS |
| S2-T07 | Missing JSON file | Missing path | Returns empty list without crashing | PASS |
| S2-T08 | Corrupted JSON file | Invalid JSON | Returns empty list without crashing | PASS |
| S2-T09 | Game state | `WordleGame("APPLE")` | Secret, length and attempts stored; guess evaluated case-insensitively | PASS |

### Edge Cases

- Missing data file
- Corrupted JSON
- Empty history

> Sprint 2 เดิมมีเคส Datamuse/Dictionary API (retry, cache, malformed response, duplicate words) — ส่วน Dictionary API ถูกลบใน Sprint 3; helper Datamuse ที่เหลือใน `scripts/word_api.py` ยังมีเทสต์ (ดู S3-T14)

## 5. Sprint 3 Test Plan — Full-Stack Integration

### Test Cases

| ID | Test Case | Input | Expected Result | Status |
|---|---|---|---|---|
| S3-T01 | Complete game | `WORDLE_TEST_WORD=GRAPE`, guesses `crane`, `grape` | Both guesses saved; correct flags, `game_number`, secret stored | PASS |
| S3-T02 | Second game numbering | Play twice | `game_number` is `[1, 2]` | PASS |
| S3-T03 | View history | Select History | Grouped by game with status, answer, and guess table | PASS |
| S3-T04 | View statistics | Select Statistics | Games played, win rate, streak, distribution appear | PASS |
| S3-T05 | View instructions | Select How to Play | Rules and feedback meanings appear | PASS |
| S3-T06 | Hint order | `hint_text("APPLE")` twice | Letter 1 then letter 2 revealed; all revealed → answer text | PASS |
| S3-T07 | Hint message reaches next redraw | `hint` then `grape` | Hint text appears below the board on the next redraw | **PASS** |
| S3-T08 | Answer discards unfinished game | `crane`, `answer` | History is `[]` | PASS |
| S3-T09 | Answer before any guess | `answer` | No history file written | PASS |
| S3-T10 | Discard only that game | `_discard_game(history, 2)` | Game 1 kept, game 2 removed | PASS |
| S3-T11 | Error line replacement | `abc`, `abc`, `APPLE` | `erase_lines` called with `[1, 2, 2]` | PASS |
| S3-T12 | Non-terminal output | `erase_lines(3)`, `clear_screen()` | Nothing written | PASS |
| S3-T13 | History deleted mid-game | File rewritten to `[]` between guesses | Only the later guess is saved | PASS |
| S3-T14 | Save failure | `save_data` returns `False` | One warning, game continues | PASS |
| S3-T15 | Non-list history JSON | `{}`, `"abc"`, `42`, `null` | `load_data()` returns `[]` | PASS |
| S3-T16 | Non-dict records | `["junk", 3, None, {...}]` | Only dict records kept | PASS |
| S3-T17 | History path | Check `HISTORY_PATH` | Absolute path, `history.json` | PASS |
| S3-T18 | Real word bank | Load data files | Tuple + frozenset, uppercase 5-letter words, `answers ⊆ valid` | PASS |
| S3-T19 | Missing/empty/wrong-length files | No usable file | `DEFAULT_WORD_POOL` returned | PASS |
| S3-T20 | Partial files | Only answers or only valid file | Still playable, `answers ⊆ valid` | PASS |
| S3-T21 | Parsing | Mixed case, spaces, wrong length, digits | Filtered, uppercased, stripped; valid = answers ∪ valid_words | PASS |
| S3-T22 | No network | `socket.connect` patched to raise | `load_word_bank()` never raises | PASS |
| S3-T23 | Any CWD | `chdir` to temp dir | Real data files still loaded | PASS |
| S3-T24 | Test word | `WORDLE_TEST_WORD=grape` | Used as secret; accepted as guess | PASS |
| S3-T25 | Renderer colors | `BoardRenderer.tile` | green / yellow / bright_black by feedback | PASS |
| S3-T26 | Board padding | 1 row, `max_attempts=6` | Table has 6 rows | PASS |
| S3-T27 | Daily word helper | `today_word()` success/timeout/HTTP error/bad JSON | Uppercase word or `None`, no crash | PASS |
| S3-T28 | Build-time API helpers | `scripts/word_api.py` with fake responses | Filter length/score, `None` on failure | PASS |

### Edge Cases

- Word files missing, empty, or containing only wrong-length words
- History file deleted or edited while the game is running
- History file with wrong top-level type or junk records
- `answer` before and after guesses
- Several invalid guesses in a row
- Output redirected (not a terminal)
- Running from a different working directory
- Test mode enabled and cleared

## 6. Sprint 4 Test Plan — DevOps, Packaging & Daily Word Mode
 
### Test Cases
 
| ID | Test Case | Input | Expected Result | Status |
|---|---|---|---|---|
| S4-T01 | Immediate play subcommand | `wordle start` (`main(["start"])`) | Starts `play_game()` directly without welcome banner or menu | PASS |
| S4-T02 | Default interactive menu | `wordle` (`main([])`) | Displays interactive 5-option menu | PASS |
| S4-T03 | Direct history command | `wordle history` | Calls `display_history()` directly without menu | PASS |
| S4-T04 | Direct stats command | `wordle stats` | Calls `display_statistics()` directly without menu | PASS |
| S4-T05 | Direct how-to-play command | `wordle howto` | Calls `display_how_to_play()` directly without menu | PASS |
| S4-T06 | Daily word game mode | `wordle today` | Fetches word via `today_word()` and passes as secret word override | PASS |
| S4-T07 | Help command | `wordle help` / `--help` | Prints CLI usage summary without entering menu | PASS |
| S4-T08 | Unknown subcommand | `wordle unknown` | Prints usage notice and exits cleanly | PASS |
| S4-T09 | Empty history handling | `calculate_stats([])` | Returns empty dict without crashing | PASS |
| S4-T10 | Legacy records grouping | History without `game_number` | Defaults to single game group | PASS |
| S4-T11 | Streak reset on loss | Game with loss record | Resets current streak to 0, counts win distribution | PASS |
| S4-T12 | Menu dispatch & invalid choice | Choices 1-5, invalid choice | Dispatches valid functions, warns on invalid, exits on 5 | PASS |
| S4-T13 | Six-guess loss path | Six wrong guesses | Shows loss message and reveals secret word | PASS |
| S4-T14 | Invalid test word fallback | `WORDLE_TEST_WORD=INVALID` | Warns player, falls back to random secret word | PASS |
| S4-T15 | Save failure warning | `save_data` returns `False` | Displays warning panel once and game continues | PASS |
| S4-T16 | Non-terminal redraw no-op | Redirected stdout | `erase_lines` and `clear_screen` write zero escape codes | PASS |
 
### Edge Cases
 
- Running `wordle` from an external directory with no local files
- Invoking `wordle today` when offline or when NYT API returns non-200 / bad JSON
- Saving history when file path is unwriteable
- Invalid menu selections repeatedly
- Six consecutive wrong guesses triggering loss logic
 
## 7. Automated Test Mapping
 
| Test File | Tests | Coverage Scope |
|---|---:|---|
| [tests/test_cli.py](test_cli.py) | 43 | Input validation, menu 1-5 dispatch, redraw, hint/answer, loss path, fallbacks |
| [tests/test_word_bank.py](test_word_bank.py) | 15 | Local word lists loading, fallback pool, no network, any CWD, case/whitespace handling |
| [tests/test_logic.py](test_logic.py) | 11 | Duplicate-letter feedback, WordleGame domain state, search/filter, JSON round-trip |
| [tests/test_entrypoint.py](test_entrypoint.py) | 9 | Packaging entrypoint, subcommands (`start`, `today`, `history`, `stats`, `howto`, `help`) |
| [tests/test_today_word.py](test_today_word.py) | 5 | `src.word_api.today_word()` API success, HTTP error, network exception, bad JSON |
| [tests/test_word_api.py](test_word_api.py) | 5 | Build-time Datamuse helpers in `scripts/word_api.py` |
| [tests/test_history_manager.py](test_history_manager.py) | 3 | Empty history, legacy format records, streak reset on loss, win distribution |
| [tests/test_boardrenderer.py](test_boardrenderer.py) | 2 | Tile coloring by feedback, board row padding |
| **Total** | **93** | **93 passed (100%), 93.46% total code coverage** |
 
## 8. Execution Evidence
 
Command executed:
 
```bash
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```
 
Result (Recorded 2026-10-05):
 
```text
============================= 93 passed in 2.57s ==============================
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src/__init__.py              0      0   100%
src/board_renderer.py       25      0   100%
src/cli.py                 172     19    89%   ...
src/data_manager.py         22      0   100%
src/game_logic.py           21      0   100%
src/history_manager.py      44      5    89%   ...
src/word_api.py             23      1    96%   ...
src/word_bank.py            40      0   100%
------------------------------------------------------
TOTAL                      347     25    93%
```
 
Flake8 lint verification:
 
```bash
flake8 --max-line-length=120 --exclude=.venv,build,dist
# Output: zero findings (100% clean)
```
 
## 9. Sprint Final QA Sign-Off
 
Sprint Final QA is **fully complete and verified**:
 
- [x] Unit tests cover Business/Data layers with **93.46% coverage** (exceeding 80% requirement).
- [x] All 93 tests pass across 8 test suites.
- [x] GitHub Actions CI workflow configured for push and pull request on Ubuntu and Windows with Python 3.12 and 3.13.
- [x] Flake8 linting passes with zero warnings.
- [x] Global CLI packaging verified (`wordle` and `wordle start` work from any directory).
- [x] Terminal manual checks verified for Windows Terminal and Unix-like environments.