# Presentation Slide Prompts — Wordle CLI V.2

## ส่วนที่ 1: ปัญหา สถาปัตยกรรม และการออกแบบ (20%)
- อธิบายปัญหาที่โปรเจกต์นี้แก้ไข: การทายคำศัพท์แบบ CLI ที่ต้องมีการตรวจสอบอินพุตและโครงสร้างชัดเจน
- อธิบายประโยชน์ต่อผู้ใช้: รันง่าย, ใช้งานเร็ว, ปลอดภัยกับข้อมูลที่ป้อนผิด
- นำเสนอแผนผังชั้นของโปรเจกต์: Presentation Layer / Business Logic Layer / Data Access Layer
- วาด UML class diagram แบบง่ายสำหรับ `WordleGame`, `CLI`, และ `DataManager` ในอนาคต

## ส่วนที่ 2: Stack เทคโนโลยีและมาตรฐานการพัฒนา (10%)
- ระบุ Python 3.8+ (ทดสอบและรองรับบน Python 3.12 และ 3.13) เป็นภาษาหลัก
- ระบุไลบรารี: `rich`, `requests`, `pytest`, `pytest-cov`, `flake8`
- ระบบ Packaging: `pyproject.toml` (Hatchling) พร้อม entry points `wordle` และ `run-app`
- อธิบายการใช้ `rich` (Panel, Table, Console) เพื่อสร้าง UI แบบกรอบ/สีที่สวยงาม และการทำ ANSI in-place redraw
- อธิบายการเปลี่ยนสถาปัตยกรรมเป็น Offline-First Word Bank (`src/data/answers.txt` และ `valid_words.txt`) ตรวจสอบคำในเครื่องแบบ `O(1)` ทันที ไม่ต้องรอ API 3-10 วินาที
- อธิบายแนวคิดการออกแบบ: Separation of Concerns (3-Tier Layered Architecture), Single Responsibility, Defensive Programming, Zero Lint Findings (PEP 8)

## ส่วนที่ 3: การสาธิตฟังก์ชันและการทดสอบจริง (40%)
- สาธิตการติดตั้งแพ็กเกจด้วย `pip install .` และรันคำสั่ง `wordle` จากไดเรกทอรีใดก็ได้
- สาธิตคำสั่ง `wordle start` ที่เริ่มเกมทันทีโดยข้ามหน้าจอ Banner และเมนู
- สาธิตโหมด `wordle today` ที่ดึงคำเฉลยประจำวันจาก NYT API มาใช้เป็นคำเฉลยของเกม
- แสดงเมนูหลักและการเลือกเมนูที่ผิด เช่น `0`, `abc`, ค่าว่าง (Defensive Input Validation)
- สาธิตกระดานทาย (Wordle Board) แบบ Rich Table/Panel ที่ redraw ทับตำแหน่งเดิม พร้อม Panel สรุปตอนชนะ/แพ้
- สาธิตเมนู Statistics (Games, Win Rate, Streak, Distribution) และ How to Play
- แสดงคำทายที่ผิดพลาด เช่น สั้น, ยาว, มีตัวเลข, มีช่องว่าง, คำที่ไม่มีใน word list และการแทนที่บรรทัด error เดิม
- สาธิตการใช้ `hint` (เปิดตัวอักษรไม่เสียรอบ) และ `answer` (ยอมแพ้โดยตัดเกมที่ยอมแพ้ออกจากสถิติ)
- อธิบาย `WORDLE_TEST_WORD` สำหรับการทดสอบด้วยคำเฉลยที่กำหนดเอง
- อ้างอิง [TEST_PLAN.md](./tests/TEST_PLAN.md) และ [TEST_CASES.md](./tests/TEST_CASES.md) นำเสนอชุดการทดสอบทั้งหมด **93 เคส (ผ่าน 100%)** พร้อม Code Coverage **93.46%**

## ส่วนที่ 4: ปัญหาทางเทคนิค การแก้ไข และการเปรียบเทียบ (15%)
- สรุปความท้าทายหลัก: การแยก Presentation, Business Logic และ Data Access ออกจากกัน
- เปรียบเทียบ Runtime API validation (ช้า 3-10s, เสี่ยง timeout) กับ Offline-first word bank (รวดเร็ว <1ms, 100% reliable)
- อธิบายการแก้ปัญหา Terminal Cursor และกระดานซ้อนด้วย `erase_lines()` และ in-place redraw
- อธิบายการจัดการ State และประวัติการเล่น: ย้ายไปเก็บที่ `~/.wordle/history.json` แยกตาม User Profile เพื่อให้ใช้งานได้ทั่วเครื่องและไม่กระทบ CI
- สรุปการประเมิน Class Extraction (`HistoryRepository`, `GameSession`, `ConsoleUI`) จาก [REFACTOR_NOTES.md](./REFACTOR_NOTES.md)

## ส่วนที่ 5: ระบบ DevOps, CI/CD Pipeline และแนวโน้ม AI Integration (15%)
- นำเสนอระบบ CI/CD Automation บน GitHub Actions (`.github/workflows/ci.yml`):
  - Matrix Build ทดสอบบน Ubuntu และ Windows กับ Python 3.12 และ 3.13
  - Pip cache เพื่อลดเวลาการติดตั้ง
  - Flake8 Linting ตรวจสอบคุณภาพโค้ด (0 findings)
  - Enforce Coverage Gate อย่างน้อย 80% (`--cov-fail-under=80`, ทำได้จริง 93.46%)
- สาธิตการทำงานของ Global CLI และ Direct Subcommands (`start`, `history`, `stats`, `howto`, `today`, `help`)
- นำเสนอ Daily Word Automation Feature จาก `src/word_api.py:today_word()`
- แนวทางการต่อยอดในอนาคต: ระบบ AI Assistant แนะนำคำทายที่มีประสิทธิภาพสูงสุดตาม Letter Frequency และ Rule-based Candidate Filtering

---

## Suggested Demo Script
1. เปิด terminal นอกโฟลเดอร์โปรเจกต์ รัน `pip install .` เพื่อแสดงการติดตั้ง
2. รัน `wordle` แสดงเมนูหลักและทดสอบ invalid choice (`abc`, `0`)
3. รัน `wordle start` แสดงการเข้าเกมทันที และทดสอบคำทาย, error line replacement, `hint` และ `answer`
4. รัน `wordle today` แสดงโหมด Daily Word ที่เชื่อมต่อกับ API
5. รัน `wordle stats` และ `wordle history` แสดงสถิติและประวัติการเล่น
6. รัน `pytest --cov=src --cov-fail-under=80` แสดงผล 93 เคสผ่านครบและ Coverage 93.46%
7. แสดงหน้า GitHub Actions Workflow ที่รันผ่านทุก OS และ Python Matrix

---

## Sample Q&A Prompts
- ทำไมจึงเปลี่ยนจาก Dictionary API มาเป็น Offline-First Word Bank?
- ทำไมต้องแยกเก็บประวัติการเล่นไว้ที่ `~/.wordle/history.json` แทนในโฟลเดอร์โปรเจกต์?
- GitHub Actions ช่วยควบคุมคุณภาพของซอฟต์แวร์อย่างไรบ้าง?
- การคำนวณ feedback ของตัวอักษรซ้ำ (Duplicate Letters) มีอัลกอริทึมอย่างไร?
- การทำ in-place redraw มีการจัดการอย่างไรเมื่อ output ถูก redirect ไปยังไฟล์ที่ไม่ใช่ terminal?