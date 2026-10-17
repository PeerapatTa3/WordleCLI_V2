# QA Report — Sprint 1-4 (Sprint Final)

**Project:** Wordle CLI V.2  
**Sprint:** Sprint 4 (Sprint Final — DevOps, CI/CD, Packaging & Daily Word Mode)  
**Week:** 14  
**Members:** นายพิสิษฐ์ ทรัพย์อุดมโชติ 673380285-2 (เทน), นายพีรพล แก้วเจริญสันติสุข 673380287-8 (ซอก), นายพีรพัฒน์ แท่นประยุทร 673380288-6 (พี) (ร่วมกันพัฒนาตามความเชี่ยวชาญ)

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
- [x] Added tests: `test_word_bank.py`, `test_sprint3.py`, `test_boardrenderer.py`, `test_today_word.py` (72 tests passed)

### Sprint 4 (Sprint Final)
- [x] Packaging with `pyproject.toml` and console scripts (`wordle`, `run-app`)
- [x] Global CLI subcommands: `wordle start` (ข้ามเมนูเริ่มเกมทันที), `wordle history`, `wordle stats`, `wordle howto`, `wordle today`, `wordle help`
- [x] Daily Word mode (`wordle today`): ดึงคำเฉลยประจำวันจาก NYT API ผ่าน `src/word_api.py:today_word()` พร้อม fallback เมื่อ offline
- [x] CI/CD on GitHub Actions (`.github/workflows/ci.yml`): matrix testing บน Python 3.12 และ 3.13 ทั้ง Ubuntu และ Windows
- [x] Code Quality Gates: Flake8 ผ่าน 100% 0 findings; Coverage gate บังคับ ≥ 80% (ทำได้จริง 93.46%)
- [x] ขยายชุดการทดสอบเป็น 93 เคส (เพิ่ม `test_entrypoint.py`, `test_history_manager.py`, loss path, fallback handling) ผ่านครบ 100%
- [x] ย้าย history ออกนอก repository ไปที่ `~/.wordle/history.json` พร้อม `WORDLE_HISTORY_PATH` override
- [x] แก้ไขปัญหา code leftovers: ลบ duplicate helpers ใน `game_logic.py`, ลบ `data/history.json` ที่เคย track ใน repo, และให้ `display_history` ใช้ shared grouping function

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

### 2.4 Resolution of Known Leftovers

| Item | Status in Sprint 4 | Resolution Detail |
|---|---|---|
| `requirements.txt` | RESOLVED | โค้ดเลิกใช้ `colorama` โดยสมบูรณ์; dependencies หลักถูกควบคุมผ่าน `pyproject.toml` |
| Duplicate helpers | RESOLVED | ลบ `search_history` / `filter_history` ออกจาก `src/game_logic.py` รวมไว้ที่ `src/history_manager.py` ที่เดียว |
| History grouping | RESOLVED | `display_history()` ใน `src/cli.py` เรียกใช้ `history_manager.group_history_by_game()` โดยตรง |
| Local history file | RESOLVED | ลบไฟล์ `data/history.json` ที่เคย track ใน git; ประวัติเก็บที่ `~/.wordle/history.json` แยกตามผู้ใช้ |
| Manual terminal checks | VERIFIED | ตรวจสอบบน Windows Terminal (PowerShell/CMD) และ Linux CI runner แสดงผลสีและ ANSI in-place redraw ได้ถูกต้อง |

### 2.5 Sprint 4 Verification Matrix (Packaging, CLI & DevOps)

| Test Case | Observation | Expected | Actual | Status |
|---|---|---|---|---|
| `wordle start` | เริ่มเกมทันที | ข้าม banner และเมนู เริ่มทายคำทันที | เริ่มเกมทันทีและ exit เมื่อจบ | PASS |
| `wordle today` | โหมด Daily Word | ใช้คำเฉลยประจำวันจาก NYT API เป็น secret | เริ่มเกมด้วยคำประจำวัน | PASS |
| Daily API failure | ปิดเน็ต / API error | แจ้งเตือนข้อผิดพลาด ไม่ crash | พิมพ์ข้อความเตือนและออกจากเกมอย่างปลอดภัย | PASS |
| `wordle history/stats/howto` | เรียกดูข้อมูลผ่าน subcommand | แสดงผลทันทีโดยไม่ต้องเข้าเมนูหลัก | แสดงข้อมูลและ exit | PASS |
| `wordle --help` / `wordle help` | ขอความช่วยเหลือ | แสดงคำอธิบายคำสั่งย่อยทั้งหมด | แสดง Usage guide ครบถ้วน | PASS |
| Unknown subcommand | พิมพ์คำสั่งที่ไม่มีอยู่ เช่น `wordle xyz` | แจ้ง usage เตือนผู้ใช้ | แสดงข้อความช่วยเหลือและ exit | PASS |
| Six-guess loss | ทายผิดครบ 6 ครั้ง | แสดงคำเฉลยและบันทึกสถานะ LOST | บันทึกลง history ถูกต้อง | PASS |
| History manager edge cases | history ว่าง หรือ format เก่า | คืนค่าว่าง/จัดเป็น 1 เกม ไม่ crash | `group_history_by_game` คืน dict ปลอดภัย | PASS |
| Flake8 linting | ตรวจสอบ coding style | ไม่พบข้อผิดพลาดตาม PEP 8 | 0 findings | PASS |
| Test coverage gate | คำนวณ test coverage ทั้งหมด | ผ่านเกณฑ์อย่างน้อย 80% | ได้ 93.46% (ผ่าน gate) | PASS |

---

## 3. Retrospective

### Wow!
- ระบบ CLI แยกฟังก์ชันได้ชัดเจนตาม Single Responsibility และแยกเป็นโมดูลย่อย (`BoardRenderer`, `history_manager`, `word_bank`)
- การ normalize input ด้วย `.strip()` และ `.lower()` ทำให้ผู้ใช้พิมพ์ผิดแบบเล็ก/ใหญ่หรือมีช่องว่างนำหน้า/ตามหลังยังทำงานได้
- เปลี่ยนเป็น offline-first ทำให้ตรวจคำเร็วขึ้นมาก (จาก 3-10 วินาทีเป็นทันที) และเล่นได้โดยไม่ต้องมีอินเทอร์เน็ต
- ใน Sprint 4 สามารถทำ Packaging ผ่าน `pyproject.toml` ทำให้ติดตั้งและเรียกใช้คำสั่ง `wordle` ได้ทั่วระบบ
- เพิ่ม Daily Word Mode (`wordle today`) ดึงคำจริงจาก NYT API พร้อมระบบ graceful fallback
- CI/CD ผ่าน GitHub Actions matrix ครอบคลุมทั้ง Linux/Windows และ Python 3.12/3.13 บังคับ lint และ coverage gate 80% (ทำได้จริง 93.46%)

### Whoops!
- ในช่วงแรกยังมีความสับสนเรื่องการจัดโครงสร้างไฟล์และ README ซึ่งแก้ด้วยการใช้ [PLAN.md](./PLAN.md) เป็นแผนงานหลัก
- ออกแบบให้ตรวจคำผ่าน Dictionary API ต่อคำทาย ซึ่งช้าและพึ่งพา network จึงต้องรื้อใน Sprint 3
- NYT API เป็น dependency ภายนอกและอาจล่มได้ จึงต้องออกแบบ fallback ให้ครอบคลุมทุกกรณี
- การจัดการ local history ที่เคย track ไว้ใน git ส่งผลกระทบต่อ CI จึงต้องย้ายไปเก็บที่ User Home Directory (`~/.wordle/history.json`)

---

## 4. Delivery Status

**Status:** Sprint 1-4 (Sprint Final) เสร็จสมบูรณ์ตาม DoD ครบ 100%

**Pull Request / CI Summary:**
- Features: Global `wordle` CLI, `wordle start`, `wordle today` (Daily API mode), Packaging via `pyproject.toml`, Per-user history, In-place redraw, Offline-first word bank, Rich UI
- CI/CD: GitHub Actions Matrix (Python 3.12, 3.13 บน Ubuntu และ Windows)
- Quality Gates: Flake8 0 findings; pytest coverage 93.46% (ผ่าน gate ≥ 80%)
- Testing: `python -m pytest -q` → **93 passed in ~2.5s**

---

## 5. Test Plan and Sprint Test Cases

รายละเอียด Test Plan, Test Cases และ Edge Cases แยกตาม Sprint อยู่ที่ [TEST_PLAN.md](./tests/TEST_PLAN.md)
ตาราง Test Cases แบบ Quality Assurance Matrix อยู่ที่ [TEST_CASES.md](./tests/TEST_CASES.md)

---

## 6. Coverage and Lint Report

### 6.1 Baseline (ก่อนเริ่ม Sprint Final B)
Recorded 2026-10-04:
- `pytest --cov=src`: 82 passed; 89.13% coverage; `src/history_manager.py` อยู่ที่ 79%
- `flake8`: 31 findings across `scripts/`, `src/`, `tests/`

### 6.2 Final Results (จบ Sprint 4)
Recorded 2026-10-05:
| Check | Requirement | Result | Status |
|---|---|---|---|
| `python -m pytest --cov=src --cov-fail-under=80` | ≥ 80% Coverage | **93 passed; 93.46% total coverage** (`src/history_manager.py` 89%) | **PASSED** |
| `flake8 --max-line-length=120 --exclude=.venv,build,dist` | Zero findings | **0 findings** | **PASSED** |
| GitHub Actions Matrix | Push/PR triggers on Ubuntu & Windows | Workflow configured and validated | **PASSED** |
| Package Install | `pip install .` works from any folder | Tested global `wordle` and `wordle start` | **PASSED** |