# 🟩 Wordle CLI V.2

โปรแกรมเกมทายคำศัพท์ (Wordle) แบบ Command Line Interface พัฒนาด้วย Python
โปรเจกต์นี้จัดทำเป็น Final Project รายวิชา **CP352301 Script Programming**

- Repository: [PeerapatTa3/Miniproject_WordleCLI](https://github.com/PeerapatTa3/Miniproject_WordleCLI)
- Version: V.2 (current project state)
- Status: Sprint 1-3 core features completed and verified; Sprint Final remains for CI/CD and AI integration

---

## 📋 คุณสมบัติ (Features)

- 🎮 เล่นเกม Wordle ทายคำศัพท์ 5 ตัวอักษร ภายใน 6 ครั้ง
- 📊 ดูและเรียงลำดับประวัติการทาย (Guess History)
- 📈 ดูสถิติการเล่น เช่น Win Rate, Current Streak และ Guess Distribution
- 📖 ดูวิธีเล่นและความหมายของ feedback แต่ละแบบ
- 🔍 ค้นหา/กรองคำที่เคยทาย
- 💾 บันทึกและโหลดข้อมูลอัตโนมัติ (JSON)
- 🛡️ ตรวจสอบและป้องกันข้อมูลนำเข้าที่ผิดพลาด (Input Validation + Exception Handling)
- 📚 ตรวจคำทายจาก Datamuse, Dictionary API และ local fallback พร้อม retry/cache เพื่อไม่ให้คำจริง เช่น `UPPER` และ `MINER` ถูกปฏิเสธเมื่อ API timeout
- คำที่ใช้ต้องเป็นคำอังกฤษ 5 ตัวอักษร เช่น `ELECT`; `PROFIT` ใช้ไม่ได้เพราะมี 6 ตัวอักษร และ `POFIT` ไม่ใช่คำมาตรฐาน
- 📖 ใช้ Datamuse API ดึงรายการคำ 5 ตัวอักษร และ Dictionary API ตรวจ definition ของคำ
- 💡 ใช้ `hint` และ `answer` เพื่อช่วยเล่นหรือทดสอบเกม
- 🎨 แสดงผล feedback ด้วยสี 

---

## 🧱 สถาปัตยกรรม (Architecture)

โปรเจกต์แบ่งออกเป็น 3 เลเยอร์ตามหลัก Separation of Concerns:

| เลเยอร์ | หน้าที่ | ไฟล์ |
|---|---|---|
| **Presentation Layer** | แสดงเมนู, รับอินพุตจากผู้ใช้ | `cli.py` |
| **Business Logic Layer** | กติกาเกม, คำนวณ feedback, search/filter | `src/game_logic.py` |
| **Data Access Layer** | อ่าน/เขียนไฟล์ข้อมูล (JSON) | `src/data_manager.py` |

```
Miniproject_WordleCLI/
├── game.py              # Entry point หลัก
├── cli.py                # Presentation Layer
├── src/
│   ├── game_logic.py      # Business Logic Layer
│   ├── data_manager.py    # Data Access Layer
│   └── word_api.py        # Meaningful word API integration
├── data/
│   ├── history.json       # ไฟล์เก็บ guess history
│   └── word_pool.json     # คลังคำ fallback แบบอ่านอย่างเดียว
├── tests/
│   ├── test_cli.py         # CLI tests
│   ├── test_logic.py       # Business/data tests
│   └── test_word_api.py    # API tests
├── requirements.txt
├── PLAN.md
└── README.md
```

> โค้ดปัจจุบันแยกเป็น Presentation, Business Logic, Data Access และ API Integration แล้ว

---

## ⚙️ ความต้องการของระบบ (Requirements)

- Python 3.x ขึ้นไป
- ไลบรารีเพิ่มเติม (ดู `requirements.txt`):
  ```
   colorama
   pytest
   requests
  ```

---

## 🚀 การติดตั้งและรัน (Installation & Usage)

1. Clone โปรเจกต์
   ```bash
   git clone https://github.com/PeerapatTa3/Miniproject_WordleCLI.git
   cd Miniproject_WordleCLI
   ```

   > โครงการปัจจุบันคือเวอร์ชัน V.2 ของ [PeerapatTa3/Miniproject_WordleCLI](https://github.com/PeerapatTa3/Miniproject_WordleCLI)

2. ติดตั้ง dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. รันโปรแกรม
   ```bash
   python game.py
   ```

4. เลือกเมนูจากตัวเลข 1-5 ตามที่แสดงในหน้าจอ

สำหรับทดสอบแบบรู้คำเฉลยล่วงหน้า สามารถกำหนดคำก่อนรันโปรแกรมได้:

```powershell
$env:WORDLE_TEST_WORD="APPLE"
python game.py
```

โหมดนี้จะแสดงคำเฉลยพร้อมข้อความ `[TEST MODE]` เฉพาะรอบที่กำหนดตัวแปรเท่านั้น

---

## 🕹️ วิธีเล่น (How to Play)

1. เลือกเมนู `1. Play Wordle`
2. พิมพ์คำทาย 5 ตัวอักษร แล้วกด Enter
   - คำทายต้องอยู่ใน word pool หรือเป็นคำตอบที่ระบบสุ่มจาก API
3. ระบบจะแสดง feedback:
   - `✓` (สีเขียว) = ตัวอักษรถูกและอยู่ตำแหน่งที่ถูกต้อง
   - `-` (สีเหลือง) = ตัวอักษรมีในคำตอบ แต่ผิดตำแหน่ง
   - `x` (สีแดง) = ตัวอักษรไม่มีในคำตอบ
4. ทายให้ถูกภายใน 6 ครั้ง

ระหว่างเล่นสามารถใช้คำสั่งช่วยได้:
- พิมพ์ `hint` เพื่อเปิดตัวอักษรทีละตำแหน่ง โดยไม่เสียจำนวนครั้ง
- พิมพ์ `answer` เพื่อแสดงคำเฉลยและจบรอบปัจจุบัน

เมนูเพิ่มเติม:
- `3. View Statistics` แสดงสถิติการเล่นจากประวัติที่บันทึกไว้
- `4. How to Play` แสดงกติกาและความหมายของ feedback
- `5. Exit` ออกจากโปรแกรม

---

## 🧪 การทดสอบ (Testing)

```bash
pytest tests/
```

Current verification: `35 passed`.

รายละเอียด Test Plan, Test Cases และ Edge Cases แยกตาม Sprint อยู่ที่ [TEST_PLAN.md](TEST_PLAN.md)
ตาราง Test Cases แบบสรุปและรายละเอียดเชิงลึกอยู่ที่ [TEST_CASES.md](TEST_CASES.md)


หน้าประวัติจะแสดงผลแบบสรุปรายเกมเหมือนเวอร์ชันเก่า โดยมีหมายเลขเกม, สถานะ WON/LOST, คำเฉลย และลำดับคำที่ทาย

Test coverage includes CLI validation, full API word-list validation, exact-word fallback such as `HELLO`, colorized feedback, Wordle duplicate-letter rules, JSON persistence failures, Datamuse API response validation, network failure handling, statistics, hints, and answer reveal.

การตั้งค่า CI/CD ผ่าน GitHub Actions ยังเป็นงานของ Sprint Final และยังไม่ได้เพิ่ม workflow ใน repository นี้

---

## 🗺️ แผนการพัฒนา (Development Roadmap)

| Sprint | โฟกัส | สถานะ |
|---|---|---|
| Sprint 1 | Front-End App Dev (CLI, Input Validation) | ✅ |
| Sprint 2 | Back-End App Dev (Logic, File I/O, Search/Filter/Sort) | ✅ |
| Sprint 3 | Full-Stack Integration | ✅ |
| Sprint Final | CI/CD & AI Integration | ⏳ |

รายละเอียดแต่ละ Sprint ดูได้ที่ [`PLAN.md`](./PLAN.md)

---

## 🔹 Sprint 1: Front-End App Dev

Sprint 1 มุ่งเน้นการสร้างรากฐานส่วนโต้ตอบผู้ใช้ให้ทำงานได้อย่างถูกต้องก่อนเชื่อมต่อกับ Logic และ Data Layer

### เป้าหมายหลัก
- แสดง banner ต้อนรับและเมนูหลัก
- รับคำสั่งจากผู้ใช้แบบปลอดภัยและยอมรับการพิมพ์เล็ก/ใหญ่ต่างกันได้
- ตรวจสอบความถูกต้องของคำทาย 5 ตัวอักษร
- ป้องกันการพังของโปรแกรมจากอินพุตผิดพลาด

### ฟังก์ชันสำคัญที่ต้องมี
- `display_welcome_message()`
- `display_menu()`
- `get_menu_choice()`
- `get_guess_input(word_length, valid_words)`
- `is_valid_guess(guess, word_length, valid_words)`
- `display_hint()` / `display_answer()`
- `main()`

### Definition of Done (DoD)
- [x] เลือกเมนูนอกช่วง 1-5 ต้องไม่ทำให้โปรแกรม crash
- [x] คำทายที่มีความยาวไม่ตรง 5 หรือมีตัวเลข/สัญลักษณ์ต้องถูกปฏิเสธ
- [x] คำทายที่ไม่อยู่ใน word pool ต้องถูกปฏิเสธ
- [x] พิมพ์เล็ก/ใหญ่ปนกันให้ทำงานเหมือนกัน
- [x] ใช้ `hint` และ `answer` ระหว่างเล่นได้
- [x] ทุกฟังก์ชันมี Docstring และโค้ดแยกหน้าที่ชัดเจน

### Sprint 1 Deliverables
- QA Report: [QA_REPORT.md](./QA_REPORT.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Learning Log: [LEARNINGLOG.md](./LEARNINGLOG.md)
- CLI implementation: [cli.py](./cli.py)
- Tests: [tests/test_cli.py](./tests/test_cli.py)

---

## 👥 ทีมพัฒนา (Team)

| Sprint | Planner / PM | Coder | Debugger / QA |
|---|---|---|---|
| Sprint 1 | เทน | ซอก | พี |
| Sprint 2 | ซอก | พี | เทน |
| Sprint 3 | พี | เทน | ซอก |
| Sprint Final | ตามความเชี่ยวชาญเฉพาะบุคคล (เทน / ซอก / พี) |  |  |

> บทบาทหมุนเวียนในแต่ละ Sprint ตามแผนงานใน [PLAN.md](./PLAN.md)

---

## 📄 License

โปรเจกต์นี้จัดทำเพื่อการศึกษาในรายวิชา CP352301 Script Programming