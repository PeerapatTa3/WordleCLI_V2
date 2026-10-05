# QA Report — Sprint 1-3 Integration

**Project:** Wordle CLI V.2  
**Sprint:** 1-3 (สถานะปัจจุบัน: จบ Sprint 3)  
**Week:** 12  
**Members:** เทน (Planner), ซอก (Coder), พี (Debugger)

---

## 1. Sprint Progress Summary

### Sprint 1-2
- [x] Defined CLI scope and Definition of Done in PLAN.md
- [x] Implemented welcome banner and main menu
- [x] Completed input validation for menu and guess handling
- [x] Added core game logic for Wordle feedback calculation (duplicate-letter aware)
- [x] Added JSON-based history persistence
- [x] Restored and tested Statistics and How to Play menu features from the legacy project
- [x] Added and tested in-game `hint` and `answer` commands
- [x] Upgraded the CLI presentation layer to a `rich`-based UI (Panel/Table for menu, board, history, and stats)
- [x] Added edge-case tests for duplicate letters and corrupted JSON

### Sprint 3
- [x] Replaced API-based word validation with an offline-first word bank (`src/word_bank.py`, `data/answers.txt` 1,984 words, `data/valid_words.txt` 8,636 words); guesses are checked by set lookup, no network at runtime
- [x] Moved Datamuse helpers to `scripts/` (build-time only); removed the Dictionary API, retry and cache
- [x] Added `scripts/build_wordlists.py` to generate the word lists
- [x] In-place redraw: `erase_lines()`, `clear_screen()`, `render_game_screen()`; invalid-guess line is replaced instead of stacked
- [x] Extracted `BoardRenderer` and `history_manager` from `cli.py`; added `MAX_ATTEMPTS` / `WORD_LENGTH`; removed `colorize_feedback()` and colorama usage
- [x] History is reloaded from disk before every write; `HISTORY_PATH` resolved from `Path(__file__)`
- [x] `load_data()` returns `[]` for non-list JSON and drops non-dict records; save failure shows one warning
- [x] `answer` discards the unfinished game so history/statistics never show it
- [x] Added tests: `test_word_bank.py`, `test_sprint3.py`, `test_boardrenderer.py`, `test_today_word.py`
- [x] `pytest` fully green (72 of 72 pass)
- [ ] Manual terminal checks (Windows Terminal, Unix terminal, redirected output)

---

## 2. Bug/Validation Report

### 2.1 Input, logic and persistence (Sprint 1-2, still valid)

| Test Case | Observation | Expected | Actual | Status |
|---|---|---|---|---|
| Select menu `0` | User enters invalid menu option | Program shows warning and loops again | Program shows invalid option message and continues | PASS |
| Select menu `abc` | User enters non-numeric text | Program rejects input and asks again | Program rejects input and continues | PASS |
| Guess with short word | User enters `APP` | System rejects as invalid length | Invalid guess message shown | PASS |
| Guess with numbers | User enters `APP1E` | System rejects because not alphabetic | Invalid guess message shown | PASS |
| Guess with spaces | User enters `APP LE` | System rejects because not alphabetic | Invalid guess message shown | PASS |
| Mixed case input | User enters `play` or `PLAY` | All variants should behave the same | Menu input is normalized with `.lower()` | PASS |
| Valid 5-letter word | User enters `APPLE` | Accept and continue | Input accepted and returned uppercase | PASS |
| Duplicate letters | Guess `ALLEY` against `APPLE` | Only available matching letters receive yellow feedback | Feedback is `['✓', '-', 'x', '-', 'x']` | PASS |
| Corrupted history file | JSON cannot be decoded | Loader returns an empty list without crashing | `load_data()` returns `[]` | PASS |
| Statistics | Saved history contains multiple games | Show win rate, streak, and guess distribution | Statistics summary is displayed correctly | PASS |
| How to Play | User selects the help menu | Explain rules and feedback markers | Help text is displayed | PASS |
| Hint command | User enters `hint` during a round | Reveal one letter without consuming an attempt | One letter is shown | PASS |
| Answer command | User enters `answer` during a round | Reveal the secret and end the round | Secret word is displayed | PASS |

### 2.2 Word validation (changed in Sprint 3)

| Test Case | Observation | Expected | Actual | Status |
|---|---|---|---|---|
| Common words offline | `HELLO`, `WORLD`, `ELECT`, `UPPER`, `MINER` | Accepted without any network call | Accepted from local `valid_words` | PASS |
| Unknown word | User enters `QZXJK` or `POFIT` | Reject the guess and ask again | Rejected (not in word list) | PASS |
| Wrong length | User enters `PROFIT` | Reject non-five-letter input | Rejected | PASS |
| Word lists consistent | Real data files | Every answer is also a valid guess | `answers ⊆ valid_words` | PASS |
| Files missing/empty/wrong length | No usable word file | Fall back to default pool, stay playable | `DEFAULT_WORD_POOL` used | PASS |
| No network at load | `socket.connect` patched to raise | Loading the bank never touches the network | No error raised | PASS |
| Any working directory | Run from another CWD | Same data files are found | Bank loads from `tmp_path` CWD | PASS |
| Test word | `WORDLE_TEST_WORD=grape` | Used as secret and accepted as a guess | Accepted | PASS |

> Sprint 1-2 cases about the Dictionary API (`HELLO` via API, retry/cache, unknown dictionary word) were removed with the API in Sprint 3.

### 2.3 Integration and UX (Sprint 3)

| Test Case | Observation | Expected | Actual | Status |
|---|---|---|---|---|
| Consecutive invalid guesses | `abc`, `abc`, then `APPLE` | Each error replaces the previous one | `erase_lines` called with `[1, 2, 2]` | PASS |
| Output not a terminal | `erase_lines(3)` / `clear_screen()` with `force_terminal=False` | Nothing written | Nothing written | PASS |
| Answer mid-game | `crane` then `answer` | Partial game not left in history | History is `[]` | PASS |
| Answer before any guess | `answer` immediately | No history file written | File not created | PASS |
| Full game win | `crane` then `grape` | Both guesses saved, correct flags and secret stored | Records match | PASS |
| Second game | Play twice | `game_number` increments | `[1, 2]` | PASS |
| History deleted mid-game | File rewritten to `[]` between guesses | Stale in-memory copy must not overwrite it | Only the later guess remains | PASS |
| Save fails | `save_data` returns `False` | One warning, game continues | One warning shown | PASS |
| History JSON is `{}`, `"abc"`, `42`, `null` | Wrong top-level type | Loader returns `[]` | Returns `[]` | PASS |
| History has junk records | `["x", 3, None, {...}]` | Only dict records kept | Only the dict kept | PASS |
| History path | Check `HISTORY_PATH` | Absolute, independent of CWD | Absolute, `history.json` | PASS |
| Hint message reaches next redraw | `hint` then `grape`, player-visible output checked | Hint text appears under the board on the next redraw | Hint text appears under the board on the next redraw | PASS |

**Note on the original failing case:** the hint was already shown correctly to the player, and the older test was coupled to the implementation detail of passing it as `message=` to `render_game_screen()`. The test was changed instead of the code because the behavior was correct and user-visible.

### 2.4 Known leftovers

| Item | Detail |
|---|---|
| `requirements.txt` | Still lists `colorama`, which the code no longer imports |
| Duplicate helpers | `search_history` / `filter_history` exist in both `src/game_logic.py` and `src/history_manager.py` |
| Manual checks | Not yet run: Windows Terminal, Unix terminal, output redirected to a file |

---

## 3. Retrospective

### Wow!
- ระบบ CLI แยกฟังก์ชันได้ชัดเจนตาม Single Responsibility และแยกเป็นโมดูลย่อย (`BoardRenderer`, `history_manager`, `word_bank`)
- การ normalize input ด้วย `.strip()` และ `.lower()` ทำให้ผู้ใช้พิมพ์ผิดแบบเล็ก/ใหญ่หรือมีช่องว่างนำหน้า/ตามหลังยังทำงานได้
- เปลี่ยนเป็น offline-first ทำให้ตรวจคำเร็วขึ้นมาก (จาก 3-10 วินาทีเป็นทันที) และเล่นได้โดยไม่ต้องมีอินเทอร์เน็ต
- ทดสอบครอบคลุมทั้ง logic, persistence, word bank และ edge case ของการทำงานร่วมกัน (72 เคส)

### Whoops!
- ในช่วงแรกยังมีความสับสนเรื่องการจัดโครงสร้างไฟล์และ README ซึ่งแก้ด้วยการใช้ [PLAN.md](./PLAN.md) เป็นแผนงานหลัก
- ออกแบบให้ตรวจคำผ่าน Dictionary API ต่อคำทาย ซึ่งช้าและพึ่งพา network จึงต้องรื้อใน Sprint 3
- การเปลี่ยนวิธีแสดง hint ทำให้เทสต์เดิมไม่ตรงกับโค้ด (ค้าง 1 เคส)
- เอกสารตามโค้ดไม่ทัน ทำให้ README, TEST_PLAN และสไลด์ยังอ้างถึงสิ่งที่ถูกลบไปแล้ว (แก้แล้วในรอบนี้)

---

## 4. Delivery Status

**Status:** Sprint 1-3 core features completed; Sprint Final (CI/CD, AI integration, global `wordle` command) ยังไม่เริ่ม

**Pull Request Summary:**
- Feature: CLI menu, validation, game loop, feedback scoring, JSON persistence, statistics, hint/answer, offline-first word bank, in-place redraw, Rich UI
- Testing: `python -m pytest -q` → **72 passed in 0.82s**

**PR Link:** To be filled when repository PR is created.

## 5. Test Plan and Sprint Test Cases

รายละเอียด Test Plan, Test Cases และ Edge Cases แยกตาม Sprint อยู่ที่ [TEST_PLAN.md](./tests/TEST_PLAN.md)
ตาราง Test Cases แบบ Quality Assurance Matrix อยู่ที่ [TEST_CASES.md](./tests/TEST_CASES.md)

## 6. Coverage and lint baseline (before Sprint Final B)

Recorded 2026-10-04 before adding focused coverage tests or fixing lint findings:

| Check | Baseline |
|---|---|
| `python -m pytest --cov=src --cov-report=term-missing` | 82 passed; 89.13% total coverage; `src/history_manager.py` at 79% |
| `flake8 --max-line-length=120 --exclude=.venv,build,dist` | Failed with 31 findings across `scripts/`, `src/`, and `tests/` (unused imports, line length, spacing, whitespace, and missing final newlines) |

After the Sprint Final B coverage and lint work:

| Check | Final result |
|---|---|
| `python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80` | 93 passed; 93.46% total coverage; `src/history_manager.py` at 89% |
| `flake8` | Passed with zero findings |