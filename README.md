# 🟩 Wordle CLI V.2

[![CI](https://github.com/PeerapatTa3/WordleCLI_V2/actions/workflows/ci.yml/badge.svg)](https://github.com/PeerapatTa3/WordleCLI_V2/actions/workflows/ci.yml)

โปรแกรมเกมทายคำศัพท์ (Wordle) แบบ Command Line Interface พัฒนาด้วย Python
โปรเจกต์นี้จัดทำเป็น Final Project รายวิชา **CP352301 Script Programming**

- Repository: [PeerapatTa3/WordleCLI_V2](https://github.com/PeerapatTa3/WordleCLI_V2)
- Version: v1.0.0 (สถานะปัจจุบัน: จบ Sprint 4 / Sprint Final)
- Status: ทุก Sprint เสร็จสมบูรณ์ (Packaging, Global CLI, Subcommands, Daily Word Mode, CI/CD Pipeline, Flake8 Clean, 93 tests passing พร้อม 93.46% coverage)
- **สไลด์นำเสนอ Sprint 1-2:** [Wordle CLI Slide](https://canva.link/hnnokmn8fgtewi9)
- **สไลด์นำเสนอ Sprint 3:** [Wordle CLI Slide](https://canva.link/7xanqzsz6flopto)
- - **สไลด์นำเสนอ Sprint Final:** [Wordle CLI Slide](https://canva.link/frq4wtjzq16phtw)
---

## 📋 คุณสมบัติ (Features)

- 🎮 เล่นเกม Wordle ทายคำศัพท์ 5 ตัวอักษร ภายใน 6 ครั้ง
- 📴 **Offline-first:** สุ่มคำเฉลยและตรวจคำทายจากไฟล์ในแพ็กเกจ (`src/data/answers.txt` 1,984 คำ, `src/data/valid_words.txt` 8,636 คำ) ไม่มีการเรียก network ตอนเล่น ตรวจคำเสร็จทันทีด้วย `set` lookup
- 🌐 **Global CLI & Subcommands:** ติดตั้งคำสั่ง `wordle` ใช้งานจากไดเรกทอรีใดก็ได้ผ่าน `pip install .`
  - `wordle`: เปิดเมนูหลัก
  - `wordle start`: เริ่มเกมทันทีโดยข้ามเมนู
  - `wordle today`: เริ่มเกมด้วยคำเฉลยประจำวันจาก NYT API (พร้อม fallback ออฟไลน์)
  - `wordle history`: ดูประวัติการเล่นทันที
  - `wordle stats`: ดูสถิติการเล่นทันที
  - `wordle howto`: ดูวิธีเล่นทันที
- 🖼️ **Rich UI (`rich`):** เมนู, กระดานทาย, ประวัติ, สถิติ และวิธีเล่นแสดงเป็น Panel/Table มีกรอบและสี
- ♻️ **In-place redraw:** กระดานวาดทับตำแหน่งเดิม คำที่พิมพ์ไม่ค้างบนจอ และข้อความ `Invalid guess` ถูกแทนที่เมื่อทายใหม่ (ไม่ส่ง escape code เมื่อ output ไม่ใช่ terminal)
- 📊 **ประวัติและสถิติครบถ้วน:** แสดงผลรายเกม (WON/LOST, คำเฉลย, ตารางสี), สถิติ Games Played, Win Rate, Current Streak และ Guess Distribution
- 🔍 **ค้นหา/กรองประวัติ:** `search_history`, `filter_history` ใน `src/history_manager.py`
- 💾 **Per-User Persistence:** ประวัติเก็บที่ `~/.wordle/history.json` (Windows: `%USERPROFILE%\.wordle\history.json`) พร้อม `WORDLE_HISTORY_PATH` override สำหรับเทสต์
- 🛡️ **Defensive & Hardened:** ทนทานต่อไฟล์หาย/เสีย/invalid JSON; ตกไปใช้ `DEFAULT_WORD_POOL` ได้อย่างปลอดภัย
- 💡 **ตัวช่วยในการเล่น:** คำสั่ง `hint` (เปิดตัวอักษรทีละตำแหน่งไม่เสียรอบ) และ `answer` (ยอมแพ้โดยตัดเกมไม่จบออกจากสถิติ)
- 🧪 **DevOps & CI/CD:** GitHub Actions workflow ทดสอบแบบ Matrix (Python 3.12/3.13 บน Ubuntu/Windows) พร้อม Flake8 linting และ Coverage gate 80% (ทำได้จริง 93.46%)

---

## 🧱 สถาปัตยกรรม (Architecture)

โปรเจกต์แบ่งออกเป็น 3 เลเยอร์ตามหลัก Separation of Concerns:

| เลเยอร์ | หน้าที่ | ไฟล์ |
|---|---|---|
| **Presentation Layer** | เมนู, รับอินพุต, วาดหน้าจอเกม, CLI entry point | `src/cli.py`, `src/board_renderer.py` |
| **Business Logic Layer** | กติกาเกม, คำนวณ feedback, สถิติ, search/filter | `src/game_logic.py`, `src/history_manager.py` |
| **Data Access Layer** | อ่าน/เขียน history (JSON), โหลดคลังคำ (txt), Daily API | `src/data_manager.py`, `src/word_bank.py`, `src/word_api.py` |

```
WordleCLI_V2/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI matrix (Ubuntu/Windows, Py 3.12/3.13)
├── .flake8                 # Flake8 configuration (max-line-length=120)
├── pyproject.toml          # Packaging metadata & console scripts (wordle, run-app)
├── game.py                 # Entry point สำหรับรันด้วย python game.py
├── cli.py                  # Compatibility wrapper (from src.cli import *)
├── src/
│   ├── cli.py              # Presentation & CLI dispatcher (start, today, history, etc.)
│   ├── board_renderer.py   # BoardRenderer: tile/table ที่ใช้ร่วมกันทั้งกระดาน ประวัติ และ legend
│   ├── game_logic.py       # WordleGame, calculate_feedback (pure business logic)
│   ├── history_manager.py  # group_history_by_game, calculate_stats, search/filter
│   ├── data_manager.py     # save_data / load_data (ประวัติใน ~/.wordle/history.json)
│   ├── word_bank.py        # load_word_bank() -> (answers, valid_words) จากไฟล์ local
│   ├── data/
│   │   ├── answers.txt     # คำเฉลยที่รวมในแพ็กเกจ (1,984 คำ)
│   │   └── valid_words.txt # คำที่ทายได้ที่รวมในแพ็กเกจ (8,636 คำ)
│   └── word_api.py         # today_word() ดึงคำเฉลย NYT ของวันนี้ สำหรับ wordle today
├── scripts/                # เครื่องมือ build-time (ไม่ใช้ตอนรันเกม)
│   ├── build_wordlists.py  # สร้าง data/answers.txt และ data/valid_words.txt
│   └── word_api.py         # ตัวช่วยดึงคำจาก Datamuse
├── data/                   # สำเนาเดิมใน checkout
├── tests/                  # pytest (8 ไฟล์ รวม 93 เคส, coverage 93.46%)
│   ├── test_boardrenderer.py
│   ├── test_cli.py
│   ├── test_entrypoint.py
│   ├── test_history_manager.py
│   ├── test_logic.py
│   ├── test_today_word.py
│   ├── test_word_api.py
│   └── test_word_bank.py
├── Sprints/                # สรุปผลแต่ละ Sprint (Sprint1 - Sprint4)
├── handbook/               # Developer & Player handbooks
├── PLAN.md  CHANGELOG.md  QA_REPORT.md  LEARNINGLOG.md  REFACTOR_NOTES.md
└── README.md
```

---

## ⚙️ ความต้องการของระบบ (Requirements)

- Python 3.8 ขึ้นไป (ทดสอบและรองรับบน Python 3.12 และ 3.13 ทั้ง Windows และ Linux)
- Dependencies หลัก (ติดตั้งอัตโนมัติผ่าน `pip install .`):
  - `rich`: สำหรับการแสดงผล CLI UI ที่สวยงาม
  - `requests`: สำหรับดึงคำเฉลยประจำวันในโหมด `wordle today`
- Dev Dependencies (ติดตั้งผ่าน `pip install -e ".[dev]"`):
  - `pytest`, `pytest-cov`, `flake8`

---

## 🚀 การติดตั้งและรัน (Installation & Usage)

1. Clone โปรเจกต์
   ```bash
   git clone https://github.com/PeerapatTa3/WordleCLI_V2.git
   cd WordleCLI_V2
   ```

2. ติดตั้งโปรแกรมและ dependencies
   ```bash
   pip install .
   ```

3. รันโปรแกรมจากโฟลเดอร์ไหนก็ได้
   ```bash
   wordle
   ```

   คำสั่งนี้แสดงเมนูตามปกติ; ใช้ `wordle start` เพื่อเริ่มเกมทันที โดยโปรแกรมจะจบหลังเกมนั้นสิ้นสุด

   ประวัติจะบันทึกที่ `~/.wordle/history.json` (Windows: `%USERPROFILE%\.wordle\history.json`) ตั้งค่า `WORDLE_HISTORY_PATH` เพื่อเปลี่ยนตำแหน่งได้
   ```

4. เลือกเมนูจากตัวเลข 1-5 ตามที่แสดงในหน้าจอ

สำหรับทดสอบแบบรู้คำเฉลยล่วงหน้า:

```powershell
$env:WORDLE_TEST_WORD="APPLE"
wordle start
```

โหมดนี้จะแสดงคำเฉลยพร้อมข้อความ `[TEST MODE]` และคำนั้นถูกนับเป็นคำที่ทายได้เสมอ

### สร้าง word list ใหม่ (ไม่จำเป็นตอนเล่น)

```bash
python scripts/build_wordlists.py <path-to-source-word-list>
```

---

## 🕹️ วิธีเล่น (How to Play)

1. เลือกเมนู `1. Play Wordle`
2. พิมพ์คำทาย 5 ตัวอักษร แล้วกด Enter (ต้องเป็นคำที่อยู่ใน `valid_words.txt`)
3. ระบบจะแสดง feedback เป็นช่องสี:
   - `✓` (เขียว) = ตัวอักษรถูกและอยู่ตำแหน่งที่ถูกต้อง
   - `-` (เหลือง) = ตัวอักษรมีในคำตอบ แต่ผิดตำแหน่ง
   - `x` (เทา) = ตัวอักษรไม่มีในคำตอบ
4. ทายให้ถูกภายใน 6 ครั้ง

คำสั่งช่วยระหว่างเล่น:
- `hint` เปิดตัวอักษรทีละตำแหน่ง โดยไม่เสียจำนวนครั้ง (ข้อความอยู่ใต้กระดานจนกว่าจะวาดใหม่)
- `answer` แสดงคำเฉลยและจบรอบ — เกมที่ยอมแพ้จะไม่ถูกนับในประวัติ/สถิติ

เมนูอื่น: `2. View History`, `3. View Statistics`, `4. How to Play`, `5. Exit`

---

## 🧪 การทดสอบ (Testing)

```bash
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

ผลล่าสุด: **93 เคส — ผ่านครบ 93 เคส (100%), Code Coverage: 93.46%**

| ไฟล์ | เคส | ครอบคลุม |
|---|---:|---|
| `tests/test_cli.py` | 43 | validation, เมนู 1-5, สถิติ, ประวัติ, hint/answer, in-place redraw, loss state, fallbacks |
| `tests/test_word_bank.py` | 15 | โหลด word bank ในเครื่อง, fallback pool, กรอง/normalize, ทำงานได้จากทุก CWD, ไม่เรียก network |
| `tests/test_logic.py` | 11 | feedback algorithm (ตัวอักษรซ้ำ), WordleGame state, search/filter, JSON round-trip |
| `tests/test_entrypoint.py` | 9 | global CLI subcommands (`start`, `history`, `stats`, `howto`, `today`), `help`, unknown options |
| `tests/test_today_word.py` | 5 | `today_word()` ดึงคำเฉลย NYT ประจำวัน, exception handling, timeout, bad JSON fallback |
| `tests/test_word_api.py` | 5 | helper build-time ของ Datamuse ใน `scripts/` |
| `tests/test_history_manager.py` | 3 | empty history, legacy records, streak reset เมื่อแพ้, win distribution count |
| `tests/test_boardrenderer.py` | 2 | สี tile, การ pad แถวว่างของกระดาน |
| **รวม** | **93** | ผ่านครบทั้งหมด (Zero failures) |

รายละเอียดการทดสอบ: [tests/TEST_PLAN.md](tests/TEST_PLAN.md) และ [tests/TEST_CASES.md](tests/TEST_CASES.md)

การตรวจสอบอัตโนมัติบน GitHub Actions (`.github/workflows/ci.yml`) รันเมื่อ push และ pull request บน Python 3.12 และ 3.13 ทั้งบน Ubuntu และ Windows พร้อม Flake8 linting และ Coverage gate 80%

---

## 🗺️ แผนการพัฒนา (Development Roadmap)

| Sprint | โฟกัส | สถานะ |
|---|---|---|
| Sprint 1 | Front-End App Dev (CLI, Input Validation) | ✅ เสร็จสมบูรณ์ |
| Sprint 2 | Back-End App Dev (Logic, File I/O, Search/Filter) | ✅ เสร็จสมบูรณ์ |
| Sprint 3 | Full-Stack Integration (offline-first, in-place redraw) | ✅ เสร็จสมบูรณ์ |
| Sprint Final | DevOps, CI/CD, Packaging, Global CLI & Daily Word Mode | ✅ เสร็จสมบูรณ์ |

รายละเอียดแต่ละ Sprint ดูได้ที่ [`PLAN.md`](./PLAN.md) และโฟลเดอร์ [`Sprints/`](./Sprints)

---

## 🔹 Sprint 1: Front-End App Dev

สร้างส่วนโต้ตอบผู้ใช้: banner, เมนูหลัก, รับอินพุตแบบปลอดภัย (`.strip().lower()`), ตรวจคำทาย 5 ตัวอักษร

- ฟังก์ชันหลัก: `display_welcome_message()`, `display_menu()`, `get_menu_choice()`, `get_guess_input()`, `is_valid_guess()`, `display_hint()` / `display_answer()`, `main()`
- Deliverables: [Sprints/Sprint1.md](./Sprints/Sprint1.md), [QA_REPORT.md](./QA_REPORT.md), [LEARNINGLOG.md](./LEARNINGLOG.md), [src/cli.py](./src/cli.py)

## 🔹 Sprint 2: Back-End App Dev

แยก Business Logic และ Data Access ออกจาก CLI

- `WordleGame`, `calculate_feedback()`, `search_history()`, `filter_history()` ใน [src/game_logic.py](./src/game_logic.py)
- `save_data()` / `load_data()` ใน [src/data_manager.py](./src/data_manager.py)
- ตอนจบ Sprint 2 ตรวจคำทายผ่าน Datamuse + Dictionary API พร้อม retry/cache — **ถูกแทนที่ใน Sprint 3**
- Deliverables: [Sprints/Sprint2.md](./Sprints/Sprint2.md), [tests/test_logic.py](./tests/test_logic.py)

## 🔹 Sprint 3: Full-Stack Integration

เชื่อมทุกเลเยอร์เข้าด้วยกันและแก้จุดอ่อนที่เห็นจากการใช้งานจริง

- **Offline-first word bank:** `src/word_bank.py` + `data/answers.txt` / `data/valid_words.txt` แทนการเรียก API ต่อคำทาย (เดิมช้า 3-10 วินาที/คำ และ `fetch_word_pool()` อาจวนไม่รู้จบเมื่อ API ล่ม) โค้ด API ย้ายไป `scripts/` เป็นเครื่องมือ build-time
- **In-place redraw:** `erase_lines()`, `clear_screen()`, `render_game_screen()` — กระดานไม่ซ้อน, error ไม่ซ้อน
- **Refactor:** แยก `BoardRenderer` (`src/board_renderer.py`) และ `history_manager` (`src/history_manager.py`) ออกจาก `cli.py`; เพิ่ม `MAX_ATTEMPTS`, `WORD_LENGTH`; ลบ `colorize_feedback()` และการใช้ colorama
- **State/Data hardening:** โหลด history ใหม่ก่อนเขียนทุกครั้ง, `HISTORY_PATH` อิงจาก `Path(__file__)`, `load_data()` คืน `[]` ถ้าไม่ใช่ list และทิ้ง record ที่ไม่ใช่ dict, เตือนเมื่อบันทึกไม่สำเร็จ, `answer` ทิ้งเกมที่ไม่จบ
- Deliverables: [Sprints/Sprint3.md](./Sprints/Sprint3.md), [Sprint3_todo.md](./Sprint3_todo.md), [tests/test_word_bank.py](./tests/test_word_bank.py)

## 🔹 Sprint 4: Sprint Final — DevOps, CI/CD, Packaging & Daily Word Mode

ส่งมอบแพ็กเกจ CLI มาตรฐานระดับ Production พร้อมระบบ CI/CD อัตโนมัติและ Daily Mode

- **Packaging & Global CLI:** กำหนด `pyproject.toml` พร้อม console script `wordle` และ `run-app`; เพิ่ม subcommands `start`, `history`, `stats`, `howto`, `today`, `help`
- **Daily Word Mode:** เพิ่มโหมด `wordle today` ดึงคำเฉลยประจำวันจาก NYT API ผ่าน `src/word_api.py:today_word()` พร้อม fallback ออฟไลน์ที่ปลอดภัย
- **CI/CD Automation:** GitHub Actions matrix workflow (`.github/workflows/ci.yml`) บน Ubuntu/Windows และ Python 3.12/3.13 พร้อม pip cache
- **Quality Gates:** ตรวจ Lint ผ่าน Flake8 ทั้งโปรเจกต์ 0 findings และบังคับ Coverage Gate ≥ 80% (ทำได้จริง 93.46%)
- **Data & History Migration:** ย้าย history ออกนอก repository ไปยัง `~/.wordle/history.json` พร้อม `WORDLE_HISTORY_PATH` override สำหรับเทสต์
- Deliverables: [Sprints/Sprint4.md](./Sprints/Sprint4.md), [Sprint4_todo.md](./Sprint4_todo.md), [REFACTOR_NOTES.md](./REFACTOR_NOTES.md), [.github/workflows/ci.yml](./.github/workflows/ci.yml)

---

## 👥 ทีมพัฒนา (Team)

| Sprint | Planner / PM | Coder | Debugger / QA |
|---|---|---|---|
| Sprint 1 | เทน | ซอก | พี |
| Sprint 2 | ซอก | พี | เทน |
| Sprint 3 | พี | เทน | ซอก |
| Sprint Final | ตามความเชี่ยวชาญเฉพาะบุคคล (เทน / ซอก / พี) |  |  |

> บทบาทหมุนเวียนในแต่ละ Sprint ตามแผนงานใน [PLAN.md](./PLAN.md)

# การประเมินตนเองของกลุ่ม

## Sprint 1 — Front-End App Dev

**บทบาท:** Planner = เทน | Coder = ซอก | Debugger = พี

### เทน — Planner

| เกณฑ์การประเมิน                   | เทน (Self) | ซอก |  พี | สรุปคะแนน (0–10) |
| --------------------------------- | :--------: | :-: | :-: | :--------------: |
| การวางแผนและกำหนดขอบเขตงาน        |      10      | 10    |  10   |     10             |
| การนิยาม Definition of Done (DoD) |       10     | 10    |  10   |       10           |
| การจัดทำเอกสารโครงการ             |     8       |   10  | 10    |         9.33         |
| **รวมคะแนนบุคคล**                 |      9.33      |  10   |   10  |      **9.78/10**     |

### ซอก — Coder

| เกณฑ์การประเมิน                | เทน | ซอก (Self) |  พี | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :--------: | :-: | :--------------: |
| การจัดโครงสร้างโค้ดและโมดูล    |  10   |       10     | 10    |       10           |
| การจัดการอินพุตและสถานะโปรแกรม |  10   |       10     |  10   |       10           |
| มาตรฐานและอ่านง่ายของโค้ด      |   10  |       10     |   10  |       10           |
| **รวมคะแนนบุคคล**              |  10   |    10        |   10  |      **10/10**     |

### พี — Debugger

| เกณฑ์การประเมิน                | เทน | ซอก | พี (Self) | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-: | :-------: | :--------------: |
| การทดสอบเคสขอบเขต (Edge Cases) | 10    |  10   |    10       |     10             |
| การจัดการ Exception Handling   |  10   |   10  |       10    |        10          |
| การรายงานผลและการส่งมอบงาน     |   10  |   10  |      10     |        10          |
| **รวมคะแนนบุคคล**              |  10   |  10   |    10       |     **10/10**    |

---

# Sprint 2 — Back-End App Dev

**บทบาท:** Planner = ซอก | Coder = พี | Debugger = เทน

### ซอก — Planner

| เกณฑ์การประเมิน                   | ซอก (Self) |  พี | เทน | สรุปคะแนน (0–10) |
| --------------------------------- | :--------: | :-: | :-: | :--------------: |
| การวางแผนและกำหนดขอบเขตงาน        |    10        |  10   |  10   |      10            |
| การนิยาม Definition of Done (DoD) |     10      |   10  | 10    |        10          |
| การจัดทำเอกสารโครงการ             |       10     |   10  |   9  |         9.67         |
| **รวมคะแนนบุคคล**                 |     10       | 10    |  9.67   |      **9.89/10**     |

### พี — Coder

| เกณฑ์การประเมิน                | ซอก | พี (Self) | เทน | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-------: | :-: | :--------------: |
| การจัดโครงสร้างโค้ดและโมดูล    |   10  |     10      |  10   |       10           |
| การจัดการอินพุตและสถานะโปรแกรม |  10   |    10       |  10   |      10            |
| มาตรฐานและอ่านง่ายของโค้ด      |  10   |     10      |  10   |      10            |
| **รวมคะแนนบุคคล**              | 10    |    10       |  10   |      **10/10**     |

### เทน — Debugger

| เกณฑ์การประเมิน                | ซอก |  พี | เทน (Self) | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-: | :--------: | :--------------: |
| การทดสอบเคสขอบเขต (Edge Cases) |  10   |  10   |    10        |     10             |
| การจัดการ Exception Handling   |  10   |   10  |      10      |         10         |
| การรายงานผลและการส่งมอบงาน     |  10   |  10   |       8     |              9.33    |
| **รวมคะแนนบุคคล**              | 10    |  10   |     9.33       |      **9.78/10**     |

---

# Sprint 3 — Full-Stack App Dev

**บทบาท:** Planner = พี | Coder = เทน | Debugger = ซอก

### พี — Planner

| เกณฑ์การประเมิน                   | พี (Self) | เทน | ซอก | สรุปคะแนน (0–10) |
| --------------------------------- | :-------: | :-: | :-: | :--------------: |
| การวางแผนและกำหนดขอบเขตงาน        |     10    |  10 |  10 |       10         |
| การนิยาม Definition of Done (DoD) |     10    |  10 |  10 |       10         |
| การจัดทำเอกสารโครงการ             |      9    |  10 |  10 |      9.67        |
| **รวมคะแนนบุคคล**                 |   9.67    |  10 |  10 |    **9.89/10**   |

### เทน — Coder

| เกณฑ์การประเมิน                | พี | เทน (Self) | ซอก | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :--------: | :-: | :--------------: |
| การจัดโครงสร้างโค้ดและโมดูล    |  10 |     10     |  10 |       10         |
| การจัดการอินพุตและสถานะโปรแกรม |  10 |     10     |  10 |       10         |
| มาตรฐานและอ่านง่ายของโค้ด      |  10 |     10     |  10 |       10         |
| **รวมคะแนนบุคคล**              |  10 |     10     |  10 |    **10/10**     |

### ซอก — Debugger

| เกณฑ์การประเมิน                | พี | เทน | ซอก (Self) | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-: | :--------: | :--------------: |
| การทดสอบเคสขอบเขต (Edge Cases) |  10 |  10 |     10     |       10         |
| การจัดการ Exception Handling   |  10 |  10 |     10     |       10         |
| การรายงานผลและการส่งมอบงาน     |  10 |  10 |     10     |       10         |
| **รวมคะแนนบุคคล**              |  10 |  10 |     10     |    **10/10**     |

---

# Sprint 4 — Sprint Final (Role-Specialized Development)

สมาชิกในทีมแบ่งงานตามความเชี่ยวชาญเฉพาะบุคคล:
- **เทน:** DevOps & Packaging / Architecture Lead
- **ซอก:** Core Logic & Automation / AI Integration Lead
- **พี:** Quality Assurance, Testing & Code Quality Lead

### การประเมินบทบาท: เทน — DevOps & Packaging / Architecture Lead

| เกณฑ์การประเมิน | เทน (Self) | ซอก | พี | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การออกแบบ Packaging ด้วย `pyproject.toml` และ Console Scripts | 10 | 10 | 10 | 10 |
| การจัดวาง CI/CD Matrix บน GitHub Actions (Ubuntu/Windows) | 10 | 10 | 10 | 10 |
| การย้ายและจัดการ History Path ออกนอก Repository อย่างปลอดภัย | 10 | 10 | 10 | 10 |
| **รวมคะแนนบุคคล** | **10** | **10** | **10** | **10/10** |

### การประเมินบทบาท: ซอก — Core Logic & Automation & Code Quality Lead

| เกณฑ์การประเมิน | เทน | ซอก (Self) | พี | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การพัฒนาฟีเจอร์ Daily Word (`wordle today`) และ Fallback | 10 | 10 | 10 | 10 |
| การปรับปรุง In-place Redraw และ Clean up Code De-duplication | 10 | 10 | 10 | 10 |
| การวิเคราะห์และเปรียบเทียบสถาปัตยกรรมใน `REFACTOR_NOTES.md` | 10 | 10 | 10 | 10 |
| **รวมคะแนนบุคคล** | **10** | **10** | **10** | **10/10** |

### การประเมินบทบาท: พี — Quality Assurance, Testing 

| เกณฑ์การประเมิน | เทน | ซอก | พี (Self) | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การพัฒนา Unit Test ครอบคลุม 93 เคส และวัดผล Coverage 93.46% | 10 | 10 | 10 | 10 |
| การตรวจแก้มาตรฐานโค้ดด้วย Flake8 จนได้ 0 findings | 10 | 10 | 10 | 10 |
| การจัดทำเอกสาร QA, Test Plan, Test Cases ครบถ้วนตามมาตรฐาน | 10 | 10 | 10 | 10 |
| **รวมคะแนนบุคคล** | **10** | **10** | **10** | **10/10** |

---

# สรุปคะแนน

| สมาชิก | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | คะแนนรวมเฉลี่ย |
| ------ | :------: | :------: | :------: | :------: | :------------: |
| เทน    | 9.78/10  | 9.78/10  | 10/10    | 10/10    |  **9.89/10**   |
| ซอก    | 9.89/10  | 9.89/10  | 10/10    | 10/10    |  **9.95/10**   |
| พี     | 10/10    | 10/10    | 9.89/10  | 10/10    |  **9.97/10**   |

---

## 📄 License

โปรเจกต์นี้จัดทำเพื่อการศึกษาในรายวิชา CP352301 Script Programming
