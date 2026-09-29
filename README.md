# 🟩 Wordle CLI V.2

โปรแกรมเกมทายคำศัพท์ (Wordle) แบบ Command Line Interface พัฒนาด้วย Python
โปรเจกต์นี้จัดทำเป็น Final Project รายวิชา **CP352301 Script Programming**

- Repository: [PeerapatTa3/WordleCLI_V2](https://github.com/PeerapatTa3/WordleCLI_V2)
- Version: V.2 (สถานะปัจจุบัน: จบ Sprint 3)
- Status: Sprint 1-3 เสร็จและใช้งานได้; Sprint Final (CI/CD, AI integration, global `wordle` command) ยังไม่เริ่ม
- **สไลด์นำเสนอ:** [Wordle CLI Slide](https://canva.link/hnnokmn8fgtewi9)

---

## 📋 คุณสมบัติ (Features)

- 🎮 เล่นเกม Wordle ทายคำศัพท์ 5 ตัวอักษร ภายใน 6 ครั้ง
- 📴 **Offline-first:** สุ่มคำเฉลยและตรวจคำทายจากไฟล์ในเครื่อง (`data/answers.txt` 1,984 คำ, `data/valid_words.txt` 8,636 คำ) ไม่มีการเรียก network ตอนเล่น ตรวจคำเสร็จทันทีด้วย `set` lookup
- 🖼️ Rich UI (`rich`) — เมนู, กระดานทาย, ประวัติ, สถิติ และวิธีเล่นแสดงเป็น Panel/Table มีกรอบและสี
- ♻️ **In-place redraw:** กระดานวาดทับตำแหน่งเดิม คำที่พิมพ์ไม่ค้างบนจอ และข้อความ `Invalid guess` ถูกแทนที่เมื่อทายใหม่ (ไม่ส่ง escape code เมื่อ output ไม่ใช่ terminal)
- 📊 ดูประวัติรายเกม (WON/LOST, คำเฉลย, ลำดับคำทายเป็นตารางสี)
- 📈 ดูสถิติ: Games Played, Win Rate, Current Streak และ Guess Distribution
- 📖 ดูวิธีเล่นและความหมายของ feedback แต่ละแบบ
- 🔍 ค้นหา/กรองประวัติ (`search_history`, `filter_history`)
- 💾 บันทึกประวัติเป็น JSON ทุกครั้งที่ทาย และโหลด history ใหม่จากดิสก์ก่อนเขียนทุกครั้ง (แก้/ลบไฟล์ระหว่างเล่นได้โดยไม่ถูกเขียนทับ)
- 🛡️ Input Validation + Exception Handling: ไฟล์ history หาย/เสีย/ไม่ใช่ list → คืน `[]` ไม่ crash; ไฟล์ word list หาย/ว่าง → ใช้ `DEFAULT_WORD_POOL`
- 💡 ใช้ `hint` (เปิดตัวอักษรทีละตำแหน่งโดยไม่เสียรอบ) และ `answer` (ยอมแพ้ — ตัดเกมที่ยังไม่จบออกจาก history/สถิติ)
- 🧪 `WORDLE_TEST_WORD` สำหรับกำหนดคำเฉลยตอนทดสอบ

---

## 🧱 สถาปัตยกรรม (Architecture)

โปรเจกต์แบ่งออกเป็น 3 เลเยอร์ตามหลัก Separation of Concerns:

| เลเยอร์ | หน้าที่ | ไฟล์ |
|---|---|---|
| **Presentation Layer** | เมนู, รับอินพุต, วาดหน้าจอเกม | `src/cli.py`, `src/board_renderer.py` |
| **Business Logic Layer** | กติกาเกม, คำนวณ feedback, สถิติ, search/filter | `src/game_logic.py`, `src/history_manager.py` |
| **Data Access Layer** | อ่าน/เขียน history (JSON), โหลดคลังคำ (txt) | `src/data_manager.py`, `src/word_bank.py` |

```
WordleCLI_V2/
├── game.py                 # Entry point หลัก
├── cli.py                  # wrapper: from src.cli import * (ให้ import แบบเดิมยังใช้ได้)
├── src/
│   ├── cli.py              # Presentation: เมนู, game loop, redraw, hint/answer
│   ├── board_renderer.py   # BoardRenderer: tile/table ที่ใช้ร่วมกันทั้งกระดาน ประวัติ และ legend
│   ├── game_logic.py       # WordleGame, calculate_feedback, search/filter
│   ├── history_manager.py  # group_history_by_game, calculate_stats
│   ├── data_manager.py     # save_data / load_data (HISTORY_PATH อิงจาก Path(__file__))
│   ├── word_bank.py        # load_word_bank() -> (answers, valid_words) จากไฟล์ local
│   └── word_api.py         # today_word() ดึงคำเฉลย NYT ของวันนี้ (ไม่ได้ใช้ตอนเล่น)
├── scripts/                # เครื่องมือ build-time (ไม่ใช้ตอนรันเกม)
│   ├── build_wordlists.py  # สร้าง data/answers.txt และ data/valid_words.txt
│   └── word_api.py         # ตัวช่วยดึงคำจาก Datamuse
├── data/
│   ├── answers.txt         # คำเฉลย (1,984 คำ)
│   ├── valid_words.txt     # คำที่ทายได้ (8,636 คำ; ⊇ answers)
│   └── history.json        # ประวัติการเล่น
├── tests/                  # pytest (7 ไฟล์ รวม 72 เคส)
├── Sprints/                # สรุปผลแต่ละ Sprint
├── PLAN.md  CHANGELOG.md  QA_REPORT.md  LEARNINGLOG.md  Sprint3_todo.md
└── README.md
```

---

## ⚙️ ความต้องการของระบบ (Requirements)

- Python 3.x ขึ้นไป (ทดสอบบน Python 3.13 / Windows และ 3.12 / Linux)
- ไลบรารีเพิ่มเติม (ดู `requirements.txt`): `rich`, `pytest`, `requests`
  - `requests` ใช้เฉพาะ `src/word_api.py` และ `scripts/`; ตัวเกมไม่เรียก network
  - `colorama` ยังเหลืออยู่ใน `requirements.txt` แต่โค้ดเลิกใช้แล้ว (ลบได้)

---

## 🚀 การติดตั้งและรัน (Installation & Usage)

1. Clone โปรเจกต์
   ```bash
   git clone https://github.com/PeerapatTa3/WordleCLI_V2.git
   cd WordleCLI_V2
   ```

2. ติดตั้ง dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. รันโปรแกรม (รันจากโฟลเดอร์ไหนก็ได้ — path ของ history และ word list อิงจากตำแหน่งไฟล์โค้ด)
   ```bash
   python game.py
   ```

4. เลือกเมนูจากตัวเลข 1-5 ตามที่แสดงในหน้าจอ

สำหรับทดสอบแบบรู้คำเฉลยล่วงหน้า:

```powershell
$env:WORDLE_TEST_WORD="APPLE"
python game.py
```

โหมดนี้จะแสดงคำเฉลยพร้อมข้อความ `[TEST MODE]` และคำนั้นถูกนับเป็นคำที่ทายได้เสมอ

### สร้าง word list ใหม่ (ไม่จำเป็นตอนเล่น)

```bash
python scripts/build_wordlists.py <path-to-source-word-list> -o data
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
python -m pytest -q
```

ผลล่าสุด: **72 เคส — ผ่าน 71, ไม่ผ่าน 1**

| ไฟล์ | เคส | ครอบคลุม |
|---|---:|---|
| `tests/test_cli.py` | 20 | validation, เมนู, สถิติ, ประวัติ, hint/answer, erase/clear |
| `tests/test_logic.py` | 10 | feedback (ตัวอักษรซ้ำ), search/filter, JSON round-trip |
| `tests/test_word_bank.py` | 13 | โหลดไฟล์จริง, fallback, กรอง/normalize, ไม่เรียก network, ทำงานได้จากทุก CWD |
| `tests/test_sprint3.py` | 17 | hint, แทนที่ error line, answer ทิ้งเกมที่ไม่จบ, history hardening, integration ทั้งเกม |
| `tests/test_boardrenderer.py` | 2 | สี tile, แถวว่างของกระดาน |
| `tests/test_word_api.py` | 5 | helper Datamuse ใน `scripts/` |
| `tests/test_today_word.py` | 5 | `today_word()` (NYT endpoint) |

**เคสที่ยังไม่ผ่าน:** `test_hint_message_is_passed_to_next_redraw` (ใน `tests/test_sprint3.py`) — เทสต์คาดว่า hint จะถูกส่งเป็น `message=` ให้ `render_game_screen()` แต่โค้ดปัจจุบันพิมพ์ hint ใต้กระดานโดยตรงแล้วบวก `_last_render_lines` เอง ฟังก์ชันทำงานถูกต้อง (hint มองเห็นได้) ความไม่ตรงอยู่ที่วิธีที่เทสต์ตรวจ ต้องเลือกแก้ที่เทสต์หรือแก้โค้ดให้ตรงกัน

รายละเอียด: [tests/TEST_PLAN.md](tests/TEST_PLAN.md) และ [tests/TEST_CASES.md](tests/TEST_CASES.md)

การตั้งค่า CI/CD ผ่าน GitHub Actions เป็นงานของ Sprint Final และยังไม่มี workflow ใน repository นี้

---

## 🗺️ แผนการพัฒนา (Development Roadmap)

| Sprint | โฟกัส | สถานะ |
|---|---|---|
| Sprint 1 | Front-End App Dev (CLI, Input Validation) | ✅ |
| Sprint 2 | Back-End App Dev (Logic, File I/O, Search/Filter) | ✅ |
| Sprint 3 | Full-Stack Integration (offline-first, in-place redraw) | ✅ (เหลือเทสต์ 1 เคสและ manual check) |
| Sprint Final | CI/CD, AI Integration, global `wordle` command | ⏳ ยังไม่เริ่ม |

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
- Deliverables: [Sprints/Sprint3.md](./Sprints/Sprint3.md), [Sprint3_todo.md](./Sprint3_todo.md), [tests/test_word_bank.py](./tests/test_word_bank.py), [tests/test_sprint3.py](./tests/test_sprint3.py)

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
| การวางแผนและกำหนดขอบเขตงาน        |            |     |     |                  |
| การนิยาม Definition of Done (DoD) |            |     |     |                  |
| การจัดทำเอกสารโครงการ             |     8       |     |     |                  |
| **รวมคะแนนบุคคล**                 |            |     |     |      **/10**     |

### ซอก — Coder

| เกณฑ์การประเมิน                | เทน | ซอก (Self) |  พี | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :--------: | :-: | :--------------: |
| การจัดโครงสร้างโค้ดและโมดูล    |     |            |     |                  |
| การจัดการอินพุตและสถานะโปรแกรม |     |            |     |                  |
| มาตรฐานและอ่านง่ายของโค้ด      |     |            |     |                  |
| **รวมคะแนนบุคคล**              |     |            |     |      **/10**     |

### พี — Debugger

| เกณฑ์การประเมิน                | เทน | ซอก | พี (Self) | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-: | :-------: | :--------------: |
| การทดสอบเคสขอบเขต (Edge Cases) |     |     |           |                  |
| การจัดการ Exception Handling   |     |     |           |                  |
| การรายงานผลและการส่งมอบงาน     |     |     |           |                  |
| **รวมคะแนนบุคคล**              |     |     |           |      **/10**     |

---

# Sprint 2 — Back-End App Dev

**บทบาท:** Planner = ซอก | Coder = พี | Debugger = เทน

### ซอก — Planner

| เกณฑ์การประเมิน                   | ซอก (Self) |  พี | เทน | สรุปคะแนน (0–10) |
| --------------------------------- | :--------: | :-: | :-: | :--------------: |
| การวางแผนและกำหนดขอบเขตงาน        |            |     |  10   |                  |
| การนิยาม Definition of Done (DoD) |            |     | 10    |                  |
| การจัดทำเอกสารโครงการ             |            |     |   10  |                  |
| **รวมคะแนนบุคคล**                 |            |     |  10   |      **/10**     |

### พี — Coder

| เกณฑ์การประเมิน                | ซอก | พี (Self) | เทน | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-------: | :-: | :--------------: |
| การจัดโครงสร้างโค้ดและโมดูล    |     |           |  10   |                  |
| การจัดการอินพุตและสถานะโปรแกรม |     |           |  10   |                  |
| มาตรฐานและอ่านง่ายของโค้ด      |     |           |  10   |                  |
| **รวมคะแนนบุคคล**              |     |           |  10   |      **/10**     |

### เทน — Debugger

| เกณฑ์การประเมิน                | ซอก |  พี | เทน (Self) | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-: | :--------: | :--------------: |
| การทดสอบเคสขอบเขต (Edge Cases) |     |     |    10        |                  |
| การจัดการ Exception Handling   |     |     |      10      |                  |
| การรายงานผลและการส่งมอบงาน     |     |     |       8     |                  |
| **รวมคะแนนบุคคล**              |     |     |            |      **/10**     |

---

# Sprint 3 — Full-Stack App Dev

**บทบาท:** Planner = พี | Coder = เทน | Debugger = ซอก

> ช่องคะแนน Sprint 3 เว้นว่างไว้ให้ทีมกรอกเอง

### พี — Planner

| เกณฑ์การประเมิน                   | พี (Self) | เทน | ซอก | สรุปคะแนน (0–10) |
| --------------------------------- | :-------: | :-: | :-: | :--------------: |
| การวางแผนและกำหนดขอบเขตงาน        |           |     |     |                  |
| การนิยาม Definition of Done (DoD) |           |     |     |                  |
| การจัดทำเอกสารโครงการ             |           |     |     |                  |
| **รวมคะแนนบุคคล**                 |           |     |     |      **/10**     |

### เทน — Coder

| เกณฑ์การประเมิน                | พี | เทน (Self) | ซอก | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :--------: | :-: | :--------------: |
| การจัดโครงสร้างโค้ดและโมดูล    |     |            |     |                  |
| การจัดการอินพุตและสถานะโปรแกรม |     |            |     |                  |
| มาตรฐานและอ่านง่ายของโค้ด      |     |            |     |                  |
| **รวมคะแนนบุคคล**              |     |            |     |      **/10**     |

### ซอก — Debugger

| เกณฑ์การประเมิน                | พี | เทน | ซอก (Self) | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-: | :--------: | :--------------: |
| การทดสอบเคสขอบเขต (Edge Cases) |     |     |            |                  |
| การจัดการ Exception Handling   |     |     |            |                  |
| การรายงานผลและการส่งมอบงาน     |     |     |            |                  |
| **รวมคะแนนบุคคล**              |     |     |            |      **/10**     |

---

# สรุปคะแนน

| สมาชิก | Sprint 1 | Sprint 2 | Sprint 3 | คะแนนรวมเฉลี่ย |
| ------ | :------: | :------: | :------: | :------------: |
| เทน    |    /10   |    /10   |    /10   |     **/10**    |
| ซอก    |    /10   |    /10   |    /10   |     **/10**    |
| พี     |    /10   |    /10   |    /10   |     **/10**    |


---

## 📄 License

โปรเจกต์นี้จัดทำเพื่อการศึกษาในรายวิชา CP352301 Script Programming