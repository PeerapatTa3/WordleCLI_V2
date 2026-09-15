# 🟩 Wordle CLI V.2

โปรแกรมเกมทายคำศัพท์ (Wordle) แบบ Command Line Interface พัฒนาด้วย Python
โปรเจกต์นี้จัดทำเป็น Final Project รายวิชา **CP352301 Script Programming**

- Repository: [PeerapatTa3/Miniproject_WordleCLI](https://github.com/PeerapatTa3/Miniproject_WordleCLI)
- Version: V.2 (current project state)
- Status: Sprint 1 and Sprint 2 core features completed and verified; Sprint 3 integration in progress

---

## 📋 คุณสมบัติ (Features)

- 🎮 เล่นเกม Wordle ทายคำศัพท์ 5 ตัวอักษร ภายใน 6 ครั้ง
- 📊 ดูและเรียงลำดับประวัติการทาย (Guess History)
- 🔍 ค้นหา/กรองคำที่เคยทาย
- 🗑️ จัดการ Word Pool (ลบคำออกจากรายการที่ใช้สุ่ม)
- 💾 บันทึกและโหลดข้อมูลอัตโนมัติ (JSON)
- 🛡️ ตรวจสอบและป้องกันข้อมูลนำเข้าที่ผิดพลาด (Input Validation + Exception Handling)
- 🎨 แสดงผล feedback ด้วยสี 

---

## 🧱 สถาปัตยกรรม (Architecture)

โปรเจกต์แบ่งออกเป็น 3 เลเยอร์ตามหลัก Separation of Concerns:

| เลเยอร์ | หน้าที่ | ไฟล์ |
|---|---|---|
| **Presentation Layer** | แสดงเมนู, รับอินพุตจากผู้ใช้ | `cli.py` |
| **Business Logic Layer** | กติกาเกม, คำนวณ feedback, search/filter/sort | `game_logic.py` |
| **Data Access Layer** | อ่าน/เขียนไฟล์ข้อมูล (JSON) | `data_manager.py` |

```
Miniproject_WordleCLI/
├── game.py              # Entry point หลัก
├── cli.py                # Presentation Layer
├── game_logic.py          # Business Logic Layer
├── data_manager.py        # Data Access Layer
├── data/
│   └── history.json       # ไฟล์เก็บ guess history
├── tests/
│   └── test_logic.py       # Unit tests
├── .github/
│   └── workflows/ci.yml    # CI/CD pipeline
├── requirements.txt
├── PLAN.md
└── README.md
```

> หมายเหตุ: โครงสร้างไฟล์ข้างต้นคือเป้าหมายหลังแยกโมดูลใน Sprint 2-3 หากยังอยู่ระหว่างพัฒนา โค้ดปัจจุบันอาจยังรวมอยู่ใน `game.py` ไฟล์เดียว

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

4. เลือกเมนูจากตัวเลข 1-4 ตามที่แสดงในหน้าจอ

---

## 🕹️ วิธีเล่น (How to Play)

1. เลือกเมนู `1. Play Wordle`
2. พิมพ์คำทาย 5 ตัวอักษร แล้วกด Enter
3. ระบบจะแสดง feedback:
   - `✓` (สีเขียว) = ตัวอักษรถูกและอยู่ตำแหน่งที่ถูกต้อง
   - `-` (สีเหลือง) = ตัวอักษรมีในคำตอบ แต่ผิดตำแหน่ง
   - `x` (สีแดง) = ตัวอักษรไม่มีในคำตอบ
4. ทายให้ถูกภายใน 6 ครั้ง

---

## 🧪 การทดสอบ (Testing)

```bash
pytest tests/
```

Current verification: `20 passed`.

Test coverage includes CLI validation, colorized feedback, Wordle duplicate-letter rules, JSON persistence failures, API response validation, network failure handling, and duplicate word removal.

CI Pipeline จะรัน Linting และ Unit Test อัตโนมัติทุกครั้งที่มีการ push หรือเปิด Pull Request ผ่าน GitHub Actions

---

## 🗺️ แผนการพัฒนา (Development Roadmap)

| Sprint | โฟกัส | สถานะ |
|---|---|---|
| Sprint 1 | Front-End App Dev (CLI, Input Validation) | ✅ / 🔄 |
| Sprint 2 | Back-End App Dev (Logic, File I/O, Search/Filter/Sort) | 🔄 |
| Sprint 3 | Full-Stack Integration | ⏳ |
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
- `get_guess_input(word_length)`
- `is_valid_guess(guess, word_length)`
- `main()` / `run_wordle_cli()`

### Definition of Done (DoD)
- [x] เลือกเมนูนอกช่วง 1-4 ต้องไม่ทำให้โปรแกรม crash
- [x] คำทายที่มีความยาวไม่ตรง 5 หรือมีตัวเลข/สัญลักษณ์ต้องถูกปฏิเสธ
- [x] พิมพ์เล็ก/ใหญ่ปนกันให้ทำงานเหมือนกัน
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