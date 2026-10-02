# Sprint 4: Sprint Final — Packaging and Global CLI Command

## 1. สถานะปัจจุบัน

Sprint 4 ยังดำเนินอยู่ โดยรายงานฉบับนี้บันทึกเฉพาะ Workstream D: คำสั่งติดตั้ง `wordle` และ `wordle start` ซึ่งทำเสร็จและตรวจสอบแล้ว งาน CI/CD, AI/automation, coverage, manual terminal checks และเอกสารส่งมอบส่วนที่เหลือยังไม่ถือว่าเสร็จ (ดู [Sprint4_todo.md](../Sprint4_todo.md))

การทดสอบเฉพาะส่วนที่แก้: **34 passed** (`test_entrypoint.py`, `test_word_bank.py`, `test_sprint3.py`)

การรัน test suite ทั้งหมดติด collection error ที่มีอยู่เดิม: `tests/test_cli.py` import `display_history` จาก `src.cli` แต่ไม่มี symbol นี้ในโมดูล เมื่อข้ามไฟล์ดังกล่าว การทดสอบส่วนที่เหลือผ่าน **56 tests**

## 2. Scope ที่ทำเสร็จ

### Phase 1: Packaging decisions

- ใช้ `src/data/` เป็นตำแหน่ง word lists ที่ติดตั้งไปกับแพ็กเกจ และคงสำเนาเดิมใน root `data/` ไว้ใน checkout
- คงชื่อแพ็กเกจ `src` เพื่อจำกัดขอบเขตการเปลี่ยนแปลง โดยบันทึกความเสี่ยงเรื่องชื่อทั่วไปที่อาจชนกับแพ็กเกจอื่น
- ย้ายตำแหน่งเริ่มต้นของประวัติออกจากแพ็กเกจไปที่ `~/.wordle/history.json` และเพิ่ม `WORDLE_HISTORY_PATH` สำหรับกำหนด path เอง

### Phase 2: Execution

**A. Installable command and game-start mode**
- `pyproject.toml` ใช้ Hatchling, กำหนด console script `wordle = "src.cli:main"` และคง alias `run-app`
- `main(argv=None)` ใช้ `argparse`; เรียก `wordle` โดยไม่มี subcommand เพื่อแสดง banner/menu ตามเดิม และเรียก `wordle start` เพื่อเริ่มเกมทันทีโดยไม่แสดง banner/menu
- `start` จบโปรแกรมหลังจบเกมหนึ่งรอบ
- `--help` แสดง usage; subcommand ที่ไม่รู้จักออกด้วย usage และ exit code 2

**B. Packaged data and persistence**
- `src/word_bank.py` โหลด word lists จาก `src/data/`; `scripts/build_wordlists.py` เขียนลงตำแหน่งนี้เป็นค่าเริ่มต้น
- Wheel มี `answers.txt` และ `valid_words.txt`; ไม่รวม `history.json` หรือ tests
- `HISTORY_PATH` เป็น absolute path; ค่า environment override ถูก resolve เป็น absolute path เช่นกัน
- `.gitignore` มี build artifacts และ `history.json` อยู่แล้ว จึงไม่ต้องเพิ่มรายการสำหรับตำแหน่ง history ใหม่ซึ่งอยู่นอก repository

### Phase 3: Tests and documentation

- เพิ่ม `tests/test_entrypoint.py` ครอบคลุม `start`, เมนูปกติ, unknown subcommand และ `--help`
- ปรับ fixture ของ word-bank tests ให้ใช้โครงสร้าง `src/data/`
- อัปเดต README เรื่อง `pip install .`, การเรียกคำสั่ง, ตำแหน่ง history และโครงสร้างไฟล์
- อัปเดตส่วน D ใน `Sprint4_todo.md` ตามผลที่ตรวจสอบแล้ว

## 3. ผลการทดสอบจริง (Verified)

| รายการทดสอบ | ผลลัพธ์ |
| :--- | :--- |
| Entry-point tests: `start`, no arguments, unknown command, `--help` | ผ่าน |
| Word-bank และ history regression tests (`test_word_bank.py`, `test_sprint3.py`) | ผ่าน |
| Focused test command สำหรับ Sprint 4 D | 34 passed |
| Tests ทั้งหมดเมื่อข้าม `tests/test_cli.py` | 56 passed |
| Full `pytest -q` | ยังไม่ผ่าน collection: `tests/test_cli.py` import `display_history` ที่ไม่มีใน `src.cli` |
| สร้าง wheel และตรวจรายการไฟล์ | มี word lists ทั้งสอง; ไม่มี `src/data/history.json` หรือ `tests/` |
| ติดตั้งแบบ non-editable ใน clean virtualenv และรันจาก `%TEMP%` | สำเร็จ |
| Word lists จาก installed package | 1,984 answers และ 8,636 valid words; ไม่ใช่ fallback pool |
| `wordle` จาก directory อื่น | แสดง banner/menu และออกได้ด้วยตัวเลือก 5 |
| `wordle start` จาก directory อื่น | เริ่มเกมโดยตรง; scripted win สำเร็จ |
| History หลังเล่นจาก installed command | เขียนไฟล์ได้ที่ `WORDLE_HISTORY_PATH`; default path ตรวจพบเป็น `~/.wordle/history.json` |

## 4. สรุปบทเรียน

### Wow!
- ทดสอบการติดตั้งแบบ wheel จริงจาก working directory อื่น ทำให้ยืนยันได้ว่า package data ไม่ได้พึ่ง checkout หรือ CWD
- การเก็บ history ไว้นอก `site-packages` ทำให้ไม่ต้องเขียนข้อมูลผู้ใช้ลงในตำแหน่งติดตั้ง และยังเปลี่ยน path สำหรับทดสอบได้
- `wordle` และ `wordle start` ใช้ entry point เดียวกัน โดยโหมด start ยังคงเรียก `play_game()` เดิม

### Whoops!
- Full test suite ยังถูกรบกวนจาก import ใน `tests/test_cli.py` ที่อ้างถึง `display_history` ซึ่งไม่มีใน `src.cli`; ประเด็นนี้ไม่ได้แก้ใน Workstream D
- ชื่อแพ็กเกจ `src` ยังเป็นชื่อ generic และควรพิจารณาเปลี่ยนเมื่อมีเวลาสำหรับ migration ที่กว้างขึ้น
- การตรวจสอบนี้ทำบน Windows/Python 3.13; การตรวจบน Unix terminal และการ redirect output ยังเป็น manual checks ที่ต้องทำต่อ

## 5. Deliverable Status

- [x] ติดตั้งแบบ non-editable ด้วย `pip install .`
- [x] คำสั่ง `wordle` เริ่มเมนูเดิมจาก directory อื่น
- [x] `wordle start` เริ่มเกมโดยตรงและจบหลังเกมนั้นสิ้นสุด
- [x] Word lists ถูกรวมใน wheel และโหลดจาก installed package
- [x] History ถูกบันทึกนอก package; environment override ทำงาน
- [x] Tests สำหรับ CLI arguments และ package data
- [ ] Sprint 4 CI/CD, AI/automation, coverage/lint และ manual terminal checks
- [ ] เอกสารและ demo deliverables ที่เหลือตาม Sprint 4 checklist

---

# การประเมินตนเองแยกตามบทบาท (Role-Based Grading Rubrics)

## Sprint 4 — Sprint Final

**บทบาท:** ไม่หมุนเวียนบทบาทใน Sprint นี้; ให้ทีมกรอกผลประเมินเมื่อ Sprint เสร็จ

### การประเมินบทบาท Planner (นักวางแผนและสถาปนิก)

| เกณฑ์การประเมิน | สมาชิก 1 | สมาชิก 2 | สมาชิก 3 | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การวางแผนและจัดลำดับ workstreams | | | | |
| การกำหนดขอบเขตและ Definition of Done | | | | |
| การตัดสินใจเรื่อง packaging และ data layout | | | | |
| **รวมคะแนนบุคคล** | | | | **/10** |

### การประเมินบทบาท Coder (นักเขียนโค้ด)

| เกณฑ์การประเมิน | สมาชิก 1 (Self) | สมาชิก 2 | สมาชิก 3 | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การทำงานตาม architecture และ package boundaries | | | | |
| ความถูกต้องของ CLI และ persistence | | | | |
| มาตรฐานและอ่านง่ายของโค้ด | | | | |
| **รวมคะแนนบุคคล** | | | | **/10** |

### การประเมินบทบาท Debugger / QA (นักทดสอบและประกันคุณภาพ)

| เกณฑ์การประเมิน | สมาชิก 1 | สมาชิก 2 (Self) | สมาชิก 3 | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การทดสอบ behavior และ edge cases | | | | |
| การตรวจสอบ installation และ runtime | | | | |
| การรายงานผลและการส่งมอบหลักฐาน | | | | |
| **รวมคะแนนบุคคล** | | | | **/10** |
