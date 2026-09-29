# Sprint 3: Full-Stack App Development — Integration, Offline-First Words, In-Place Redraw

## 1. สถานะปัจจุบัน

Sprint 3 เสร็จในส่วนโค้ดและเอกสาร ผลการรัน `python -m pytest -q` ล่าสุด: **72 เคส — ผ่าน 71, ไม่ผ่าน 1**

เคสที่ไม่ผ่านคือ `test_hint_message_is_passed_to_next_redraw` ซึ่งคาดว่า hint จะถูกส่งเป็น `message=` ให้ `render_game_screen()` แต่โค้ดจริงพิมพ์ hint ใต้กระดานโดยตรงและนับบรรทัดเพิ่มเอง ตัวฟีเจอร์ทำงานถูกต้อง (hint แสดงและไม่หายทันที) ที่ยังไม่ตรงกันคือเทสต์กับโค้ด ต้องเลือกแก้ด้านใดด้านหนึ่ง

สิ่งที่ยังไม่ได้ยืนยัน: manual check บน terminal จริง (Windows Terminal + Unix terminal, redirect output ไปไฟล์)

## 2. Scope ที่ทำเสร็จ

### Phase 1: Planning

- ระบุปัญหาจากการใช้งานจริงของ Sprint 2: ทุกเกมเรียก Datamuse 2 ครั้ง, ทุกคำทายที่ไม่รู้จักเรียก Dictionary API (3-10 วินาที), `fetch_word_pool()` วนไม่รู้จบเมื่อ API ล่ม, path เป็น CWD-relative
- ตัดสินใจเปลี่ยนเป็น offline-first และวาดหน้าจอเกมทับที่เดิม (ดู [PLAN.md](../PLAN.md) และ [Sprint3_todo.md](../Sprint3_todo.md))

### Phase 2: Execution

**A. Offline-first word bank**
- `src/word_bank.py`: `load_word_bank()` คืน `(answers, valid_words)` จาก `data/answers.txt` (1,984 คำ) และ `data/valid_words.txt` (8,636 คำ), path จาก `Path(__file__)`, ไฟล์หาย/ว่างใช้ `DEFAULT_WORD_POOL`
- `scripts/build_wordlists.py`: สร้างไฟล์คำจาก source word list ครั้งเดียว
- โค้ด Datamuse ย้ายไป `scripts/word_api.py` (build-time); ลบ Dictionary API, retry, cache; `src/word_api.py` เหลือ `today_word()`
- `play_game()` เพิ่ม secret word เข้า `valid_words` เสมอ ทำให้ `WORDLE_TEST_WORD` ทายได้

**B. In-place redraw**
- `erase_lines()`, `clear_screen()`, `render_game_screen()` (ไม่ทำอะไรเมื่อ output ไม่ใช่ terminal)
- Invalid guess แสดงบรรทัดเดียวและถูกแทนที่เมื่อทายใหม่ (รองรับ input ยาวที่ขึ้นบรรทัดใหม่)
- Hint แสดงใต้กระดานและอยู่จนกว่าจะวาดใหม่

**C. Refactor และ hardening**
- แยก `BoardRenderer` (`src/board_renderer.py`) และ `history_manager` (`src/history_manager.py`) ออกจาก `cli.py`
- เพิ่ม `MAX_ATTEMPTS`, `WORD_LENGTH`; ลบ `colorize_feedback()` และการใช้ colorama
- `_persist()` โหลด history ใหม่จากดิสก์ก่อนเขียนทุกครั้ง; `HISTORY_PATH` อิงจาก `Path(__file__)`
- `load_data()` คืน `[]` ถ้าไม่ใช่ list และทิ้ง record ที่ไม่ใช่ dict; เตือนเมื่อบันทึกไม่สำเร็จ
- `answer` ทิ้งเกมที่ไม่จบ ไม่ให้ประวัติ/สถิติมีเกมค้าง

**D. Rich UI (ทำต่อเนื่องนอกแผน Sprint)**
- เมนู กระดาน ประวัติ สถิติ และวิธีเล่นใช้ `rich` (Panel/Table)

### Phase 3: Review & Testing

- เพิ่ม `tests/test_word_bank.py` (13), `tests/test_sprint3.py` (17), `tests/test_boardrenderer.py` (2), `tests/test_today_word.py` (5)
- ปรับ `tests/test_cli.py` (20) และ `tests/test_word_api.py` (5) ให้ตรงกับโครงสร้างใหม่
- ทดสอบ: ไม่เรียก network ตอนโหลด word bank, ทำงานได้จากทุก CWD, history ถูกลบระหว่างเล่นไม่ถูกฟื้น, บันทึกไม่สำเร็จเตือนครั้งเดียว, game จบทั้งเกมแล้วถูกบันทึก

---

## 3. ผลการทดสอบจริง (Verified)

| รายการทดสอบ | ผลลัพธ์ |
| :--- | :--- |
| Word bank: โหลดไฟล์จริง, `answers ⊆ valid_words` | สำเร็จ |
| Word bank: ไฟล์หาย/ว่าง/ความยาวผิด → default pool | สำเร็จ |
| Word bank: ไม่เรียก network, ทำงานจากทุก CWD | สำเร็จ |
| Invalid guess: บรรทัดเดียว, erase `[1, 2, 2]` บรรทัดเมื่อผิดซ้ำ | สำเร็จ |
| `erase_lines` / `clear_screen` เป็น no-op เมื่อไม่ใช่ terminal | สำเร็จ |
| `answer` ทิ้งเกมที่ไม่จบ / ไม่เขียนไฟล์ถ้ายังไม่ทาย | สำเร็จ |
| History: ไม่ใช่ list, record ไม่ใช่ dict, ลบไฟล์กลางเกม | สำเร็จ |
| เกมเต็มรอบ: บันทึก, game_number เพิ่มถูกต้อง, เตือนเมื่อ save ล้มเหลว | สำเร็จ |
| `hint_text()` เปิดตำแหน่งตามลำดับ | สำเร็จ |
| Hint ส่งเป็น `message=` ให้ redraw ถัดไป | **ไม่ผ่าน** (เทสต์ไม่ตรงกับโค้ด) |
| Test suite ของโปรเจกต์ | 71 passed, 1 failed |

---

## 4. สรุปบทเรียน

### Wow!
- เปลี่ยนจากตรวจคำผ่าน API (3-10 วินาที/คำ) เป็น `set` lookup ในเครื่อง เล่นได้ offline และตรวจคำทันที
- กระดานและข้อความ error ไม่ซ้อนกันอีก (stacked boards and error panels → in-place redraw)
- `cli.py` เบาลงหลังแยก `BoardRenderer` และ `history_manager`

### Whoops!
- การเปลี่ยนวิธีแสดง hint ทำให้เทสต์ที่เขียนไว้ก่อนหน้าไม่ตรงกับโค้ดอีกต่อไป (เหลือ 1 เคสที่ยังไม่ผ่าน)
- `colorama` ถูกเลิกใช้ในโค้ดแต่ยังค้างใน `requirements.txt`
- `search_history` / `filter_history` มีซ้ำทั้งใน `game_logic.py` และ `history_manager.py` ควรรวมเป็นที่เดียวตอน refactor

---

## 5. Deliverable Status

- [x] Integration ของ Presentation → Business Logic → Data Access ผ่าน `main()`
- [x] Offline-first word bank และเครื่องมือ build word list
- [x] In-place redraw (โค้ด + unit test)
- [x] State/Data hardening และเทสต์
- [x] เอกสารปรับให้ตรงกับสถานะจริง
- [ ] `pytest` ผ่านครบ (71/72)
- [ ] Manual check บน terminal จริง

---

# การประเมินตนเองแยกตามบทบาท (Role-Based Grading Rubrics)

## Sprint 3 — Full-Stack App Dev

**บทบาท:** Planner = พี | Coder = เทน | Debugger = ซอก

### การประเมินบทบาท Planner (นักวางแผนและสถาปนิก)
### พี — Planner

| เกณฑ์การประเมิน                   | เทน | ซอก |  พี (Self) | สรุปคะแนน (0–10) |
| --------------------------------- | :--------: | :-: | :-: | :--------------: |
| การวางแผนและกำหนดขอบเขตงาน        |            |     |     |                  |
| การนิยาม Definition of Done (DoD) |            |     |     |                  |
| การจัดทำเอกสารโครงการ             |            |     |     |                  |
| **รวมคะแนนบุคคล**                 |            |     |     |      **/10**     |

### การประเมินบทบาท Coder (นักเขียนโค้ด)
### เทน — Coder

| เกณฑ์การประเมิน                | เทน (Self) | ซอก |  พี | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :--------: | :-: | :--------------: |
| การจัดโครงสร้างโค้ดและโมดูล    |     |            |     |                  |
| การจัดการอินพุตและสถานะโปรแกรม |     |            |     |                  |
| มาตรฐานและอ่านง่ายของโค้ด      |     |            |     |                  |
| **รวมคะแนนบุคคล**              |     |            |     |      **/10**     |

### การประเมินบทบาท Debugger (นักทดสอบและประกันคุณภาพ)
### ซอก — Debugger

| เกณฑ์การประเมิน                | เทน | ซอก(Self) | พี  | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-: | :-------: | :--------------: |
| การทดสอบเคสขอบเขต (Edge Cases) |     |     |           |                  |
| การจัดการ Exception Handling   |     |     |           |                  |
| การรายงานผลและการส่งมอบงาน     |     |     |           |                  |
| **รวมคะแนนบุคคล**              |     |     |           |      **/10**     |

