# Test Plan & Test Cases — Wordle CLI V.2

**Project:** Wordle CLI V.2  
**Scope:** Sprint 1-3  
**Test Tool:** `pytest`  
**Latest Result:** `35 passed` (ก่อนอัปเกรด UI เป็น `rich`; ดู Known Issue ด้านล่าง)

**Known Issue:** หลังเปลี่ยน `cli.py` ให้ใช้ `rich` (`console.input`/`console.print` แทน `input()`/`print()` และแสดงผลเป็น Panel/Table) เทสต์ที่ `monkeypatch("builtins.input", ...)` หรือตรวจ plain-text ผ่าน `capsys` (เช่น `test_get_menu_choice_normalizes_input`, `test_get_guess_input_retries_until_valid`, `test_display_menu_prints_options`, `test_display_history_groups_records_by_game`) ต้องปรับให้ mock `console.input`/`Console` หรือตรวจสอบข้อความภายใน Rich markup แทน ก่อนผลลัพธ์จะกลับมา `35 passed` ทั้งหมด

## 1. Test Objectives

- Verify the CLI accepts valid commands and rejects invalid input without crashing.
- Verify Wordle business logic calculates exact, misplaced, and absent letters correctly.
- Verify history and word-pool data are loaded and saved safely with JSON.
- Verify API responses, network failures, fallback words, and dictionary validation.
- Verify all integrated menus and in-game commands work together.

## 2. Test Environment

- Python 3.13
- Windows
- Virtual environment: `.venv`
- Dependencies: `pytest`, `requests`, `colorama`, `rich`
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
| S2-T09 | Load default word pool | Missing word-pool file | Default words are created/returned | PASS |

### Edge Cases

- Missing data file
- Corrupted JSON
- Empty history
- Empty word pool
- API request exception
- Invalid API response type
- Duplicate words from an API response
- Unknown five-letter word

## 5. Sprint 3 Test Plan — Full-Stack Integration

### Test Cases

| ID | Test Case | Input | Expected Result | Status |
|---|---|---|---|---|
| S3-T01 | Start a complete game | Select Play | Secret word is selected and game starts | PASS |
| S3-T02 | Persist every guess | Submit a guess | History JSON is updated immediately | PASS |
| S3-T03 | View history | Select History | History is grouped by game with status, answer, and guess sequence | PASS |
| S3-T04 | View statistics | Select Statistics | Games played, win rate, streak, and distribution appear | PASS |
| S3-T05 | View instructions | Select How to Play | Rules and feedback meanings appear | PASS |
| S3-T06 | Use hint | Enter `hint` | One secret-letter position is revealed | PASS |
| S3-T07 | Reveal answer | Enter `answer` | Secret word appears and round ends | PASS |
| S3-T08 | API fallback | API unavailable | Local words remain playable | PASS |
| S3-T09 | Dictionary validation | `HELLO` / `WORLD` | Meaningful common words are accepted | PASS |
| S3-T10 | Unknown-word protection | `QZXJK` | Unknown word is rejected | PASS |
| S3-T11 | Manual test mode | `WORDLE_TEST_WORD=APPLE` | Known answer is used only in test mode | PASS |
| S3-T12 | Exit safely | Select Exit | Program ends without exception | PASS |

### Edge Cases

- Datamuse API unavailable
- Dictionary API timeout
- Local fallback words `HELLO` and `WORLD`
- API returns an empty list
- API returns duplicate or malformed records
- Corrupted history during menu navigation
- Switching Play -> History -> Statistics -> How to Play -> Exit
- Test mode enabled and cleared

## 6. Automated Test Mapping

| Test File | Coverage |
|---|---|
| [tests/test_cli.py](tests/test_cli.py) | Sprint 1 input, menu, statistics, hints, answer, and fallback validation |
| [tests/test_logic.py](tests/test_logic.py) | Sprint 2 game logic, search/filter, and JSON persistence |
| [tests/test_word_api.py](tests/test_word_api.py) | Datamuse, Dictionary API, malformed response, network failure, and duplicate handling |

## 7. Execution Evidence

Command executed:

```text
.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
35 passed in 0.13s
```

## 8. Sprint Final QA Preparation

Sprint Final is not complete yet. The remaining QA work is:

- Add GitHub Actions CI workflow.
- Run linting automatically on push and pull request.
- Add coverage reporting and verify the important paths reach the required target.
- Test and document the final AI/Automation feature.