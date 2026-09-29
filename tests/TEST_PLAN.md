# Test Plan & Test Cases — Wordle CLI V.2

**Project:** Wordle CLI V.2  
**Scope:** Sprint 1-3  
**Test Tool:** `pytest`  
**Latest Result:** `72 tests — 71 passed, 1 failed` (รันซ้ำเมื่อ 2026-09-29)

**Known Issue:** `tests/test_sprint3.py::test_hint_message_is_passed_to_next_redraw` ไม่ผ่าน เทสต์คาดว่า hint จะถูกส่งเป็น `message=` ให้ `render_game_screen()` แต่ `play_game()` พิมพ์ hint ใต้กระดานโดยตรงแล้วบวก `_last_render_lines` เอง (ผู้เล่นเห็น hint ถูกต้อง) ต้องแก้เทสต์ให้ตรวจพฤติกรรมจริง หรือแก้โค้ดให้ส่ง `message=`

## 1. Test Objectives

- Verify the CLI accepts valid commands and rejects invalid input without crashing.
- Verify Wordle business logic calculates exact, misplaced, and absent letters correctly.
- Verify history data is loaded and saved safely with JSON, including wrong-type and corrupted files.
- Verify the local word bank loads, falls back to defaults, and never touches the network.
- Verify the in-place redraw helpers and that all integrated menus and in-game commands work together.

## 2. Test Environment

- Python 3.13, Windows (ทีม) — รันซ้ำบน Python 3.12, Linux ได้ผลเท่ากัน
- Virtual environment: `.venv`
- Dependencies: `pytest`, `rich`, `requests` (`colorama` ยังอยู่ใน `requirements.txt` แต่โค้ดไม่ใช้แล้ว)
- Test command:

```text
.venv\Scripts\python.exe -m pytest -q
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
| S3-T07 | Hint message reaches next redraw | `hint` then `grape` | Hint passed as `message=` to `render_game_screen` | **FAIL** |
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

## 6. Automated Test Mapping

| Test File | Tests | Coverage |
|---|---:|---|
| [tests/test_cli.py](test_cli.py) | 20 | Sprint 1 input, menu, statistics, history, hint, answer, erase/clear |
| [tests/test_logic.py](test_logic.py) | 10 | Feedback, `WordleGame`, search/filter, JSON round-trip |
| [tests/test_word_bank.py](test_word_bank.py) | 13 | Word bank loading, fallback, parsing, no network, any CWD |
| [tests/test_sprint3.py](test_sprint3.py) | 17 | Hint, error replacement, answer discard, history hardening, integration |
| [tests/test_boardrenderer.py](test_boardrenderer.py) | 2 | Tile colors, empty rows |
| [tests/test_word_api.py](test_word_api.py) | 5 | `scripts/word_api.py` (Datamuse helpers) |
| [tests/test_today_word.py](test_today_word.py) | 5 | `src/word_api.today_word()` |
| **Total** | **72** | 71 pass, 1 fail |

## 7. Execution Evidence

Command executed:

```text
python -m pytest -q
```

Result:

```text
1 failed, 71 passed
FAILED tests/test_sprint3.py::test_hint_message_is_passed_to_next_redraw
```

## 8. Sprint Final QA Preparation

Sprint Final is not started. The remaining QA work is:

- Decide how to fix the failing hint test (test or code).
- Manual terminal checks: Windows Terminal, a Unix terminal, redirected output.
- Add GitHub Actions CI workflow.
- Run linting automatically on push and pull request.
- Add coverage reporting and verify the important paths reach the required target.
- Test and document the final AI/Automation feature.