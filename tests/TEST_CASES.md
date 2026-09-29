# 🧪 Test Cases Documentation — Wordle CLI V.2

เอกสารจัดเก็บ **Test Cases (เคสการทดสอบระบบ)** สำหรับโปรเจกต์ **Wordle CLI V.2**  
รายวิชา CP352301 Script Programming

---

## 📋 ตารางสรุปผลการทดสอบระบบ (Quality Assurance & Test Suite Matrix)

| Test ID | หมวดการทดสอบ | รายละเอียดการทดสอบ | อินพุต (Input) | ผลลัพธ์ที่คาดหวัง (Expected Output) | ผลการทดสอบจริง (Actual Output) | สถานะ |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | CLI Menu | แสดงเมนูหลัก | Start `game.py` | แสดงเมนู 1-5 | แสดง Play, History, Statistics, How to Play และ Exit | **PASSED** |
| **TC-02** | Input Validation | ตรวจเมนูผิด | `0`, `abc`, ค่าว่าง | แจ้งเตือนและวนกลับเมนู โดยไม่ crash | โปรแกรมแสดง Invalid option และทำงานต่อ | **PASSED** |
| **TC-03** | Guess Validation | ตรวจคำสั้น/ยาว/มีตัวเลข | `APP`, `APP1E`, `APP LE` | ปฏิเสธคำและให้กรอกใหม่ | คำผิดรูปแบบถูกปฏิเสธ | **PASSED** |
| **TC-04** | Word Validation (offline) | ตรวจคำอังกฤษจากไฟล์ในเครื่อง | `HELLO`, `WORLD`, `ELECT`, `UPPER`, `MINER` | ยอมรับคำที่อยู่ใน `valid_words` โดยไม่เรียก network | คำทั้งหมดถูกยอมรับ | **PASSED** |
| **TC-05** | Unknown Word Protection | ป้องกันคำมั่ว | `QZXJK`, `POFIT` | ปฏิเสธคำที่ไม่อยู่ใน word list | คำที่ไม่รู้จักถูกปฏิเสธ | **PASSED** |
| **TC-06** | Wordle Algorithm | คำนวณ feedback | Guess `ALLEY`, Secret `APPLE` | คืนค่า `✓`, `-`, `x` ตามกติกาตัวอักษรซ้ำ | ได้ `['✓', '-', 'x', '-', 'x']` | **PASSED** |
| **TC-07** | Build-time API helper | helper Datamuse ใน `scripts/word_api.py` | fake response (list, dict+score, wrong length) | กรองความยาว/score, คืน `None` เมื่อ network ล้มเหลว | ผ่านทุกเคส (ไม่ได้ใช้ตอนเล่น) | **PASSED** |
| **TC-08** | Daily word helper | `today_word()` | success, timeout, HTTP 404, JSON ผิด | คืนคำตัวพิมพ์ใหญ่หรือ `None` โดยไม่ crash | ผ่านทั้ง 5 เคส (ไม่ได้ใช้ตอนเล่น) | **PASSED** |
| **TC-09** | JSON Persistence | บันทึก/โหลดประวัติ | History payload | ข้อมูลที่โหลดกลับมาต้องเหมือนข้อมูลที่บันทึก | Round-trip และ corrupted-file handling ผ่าน | **PASSED** |
| **TC-10** | Word Bank Fallback | ไฟล์คำหาย/ว่าง/ความยาวผิด | ไม่มีไฟล์ หรือไฟล์ว่าง | ใช้ `DEFAULT_WORD_POOL` และเล่นต่อได้ | ได้ default pool, `answers ⊆ valid` | **PASSED** |
| **TC-11** | Statistics | คำนวณสถิติผู้เล่น | History หลายเกม | แสดง games, win rate, streak และ distribution | แสดงผลสถิติถูกต้อง | **PASSED** |
| **TC-12** | Hint / Answer | ใช้คำสั่งช่วยระหว่างเล่น | `hint`, `answer` | Hint เปิดตัวอักษรโดยไม่เสียรอบ; answer แสดงเฉลยและจบรอบ | ทั้งสองคำสั่งทำงานตามที่กำหนด | **PASSED** |
| **TC-13** | History View | ดูประวัติแบบรายเกม | History หลายเกม | แสดงสถานะ, secret word และตารางคำทายต่อเกม | แสดง `Game N` WON/LOST พร้อมคำเฉลย | **PASSED** |
| **TC-15** | Offline / No Network | โหลดคลังคำโดยไม่มี network | `socket.connect` ถูก patch ให้ error | โหลดสำเร็จ ไม่แตะ network | ไม่เกิด error | **PASSED** |
| **TC-16** | Any Working Directory | รันจาก CWD อื่น | `chdir` ไป temp dir | ใช้ไฟล์ข้อมูลชุดเดิม | โหลด word bank จริงได้ | **PASSED** |
| **TC-17** | Test Word | กำหนดคำเฉลยเอง | `WORDLE_TEST_WORD=grape` | ใช้เป็นคำเฉลยและทายได้ | ถูกยอมรับ | **PASSED** |
| **TC-18** | Error Line Replacement | ทายผิดติดกัน | `abc`, `abc`, `APPLE` | error ทับบรรทัดเดิม ไม่ซ้อน | `erase_lines` = `[1, 2, 2]` | **PASSED** |
| **TC-19** | Non-terminal Output | output ไม่ใช่ terminal | `erase_lines(3)`, `clear_screen()` | ไม่เขียน escape code | ไม่มี output | **PASSED** |
| **TC-20** | Answer Discards Game | ยอมแพ้กลางเกม | `crane` แล้ว `answer` | ไม่มีเกมค้างใน history | history = `[]` | **PASSED** |
| **TC-21** | History Deleted Mid-game | ลบ/แก้ไฟล์ระหว่างเล่น | เขียน `[]` ระหว่างสองคำทาย | ไม่ถูกเขียนทับด้วยข้อมูลเก่า | เหลือเฉพาะคำทายหลังลบ | **PASSED** |
| **TC-22** | Save Failure | บันทึกไม่สำเร็จ | `save_data` คืน `False` | เตือน 1 ครั้ง เกมเล่นต่อ | เตือนครั้งเดียว | **PASSED** |
| **TC-23** | History Hardening | JSON ผิดชนิด | `{}`, `"abc"`, `42`, `null`, list ที่มีขยะ | คืน `[]` หรือเก็บเฉพาะ dict | ผ่านทุกเคส | **PASSED** |
| **TC-24** | Full Game Integration | เล่นครบเกม | `crane` → `grape` | บันทึกทั้งสองคำ, `game_number`, secret | ตรงตามคาด | **PASSED** |
| **TC-25** | Hint Redraw | hint ถูกส่งไปยัง redraw ถัดไป | `hint` → `grape` | `render_game_screen` ได้ `message=` เป็น hint | `message` เป็น `None` (โค้ดพิมพ์ hint ตรงใต้กระดาน) | **FAILED** |

> TC-14 (retry/cache ของ Dictionary API) ถูกถอดออกใน Sprint 3 พร้อมกับตัว API TC-04, TC-05, TC-10 ถูกปรับให้ตรวจกับ word bank ในเครื่อง

---

## 🔬 รายละเอียดเคสการทดสอบเชิงลึก (Detailed Test Case Specs)

### 🔹 TC-01 & TC-02: CLI Menu and Defensive Input
- **การทดสอบ:** เปิดโปรแกรมและเลือกคำสั่งที่ถูกต้อง/ผิด
- **เงื่อนไข:** ใช้ `1` ถึง `5`, รวมถึง `0`, `abc` และค่าว่าง
- **การยืนยันความถูกต้อง:** โปรแกรมต้องไม่หยุดทำงานจาก invalid menu input และต้องแสดงข้อความแจ้งเตือน

### 🔹 TC-03, TC-04 & TC-05: Guess and Word Validation
- **การทดสอบ:** ป้อนคำที่รูปแบบผิด คำที่มีความหมาย และคำสุ่มตัวอักษร
- **เงื่อนไข:** คำต้องยาว 5 ตัวอักษรและอยู่ใน `data/valid_words.txt` (8,636 คำ)
- **การยืนยันความถูกต้อง:** ตรวจด้วย membership test ใน `frozenset` ไม่มีการเรียก network; คำเฉลยทุกคำอยู่ใน valid set เสมอ

### 🔹 TC-06: Wordle Feedback Algorithm
- **การทดสอบ:** ทดสอบ exact match, wrong-position match และ duplicate letters
- **ตัวอย่าง:** `ALLEY` เทียบกับ `APPLE`
- **การยืนยันความถูกต้อง:** ตัวอักษรที่ใช้ได้เท่านั้นจึงได้รับ `-` และตัวที่ตรงตำแหน่งได้รับ `✓`

### 🔹 TC-09 & TC-23: JSON Persistence and Hardening
- **การทดสอบ:** บันทึก guess history แล้วโหลดกลับมา และโหลดไฟล์ที่เสีย/ผิดชนิด
- **การยืนยันความถูกต้อง:** ข้อมูลต้องตรงกันหลัง round-trip; corrupted JSON, ไฟล์ที่ไม่ใช่ list และ record ที่ไม่ใช่ dict ต้องไม่ทำให้ crash

### 🔹 TC-10, TC-15, TC-16 & TC-17: Offline Word Bank
- **การทดสอบ:** โหลด `answers.txt` / `valid_words.txt` ในสภาพต่าง ๆ
- **การยืนยันความถูกต้อง:** ไฟล์หาย/ว่าง → default pool; ไม่แตะ network; ทำงานได้จากทุก CWD; `WORDLE_TEST_WORD` ทายได้

### 🔹 TC-18 & TC-19: In-Place Redraw
- **การทดสอบ:** ทายผิดหลายครั้งติดกัน และรันเมื่อ output ไม่ใช่ terminal
- **การยืนยันความถูกต้อง:** บรรทัด error ถูกแทนที่ ไม่ซ้อน; ไม่มี escape code เมื่อ redirect

### 🔹 TC-20, TC-21, TC-22 & TC-24: Integrated Game State
- **การทดสอบ:** เล่นครบเกม, ใช้ `answer` กลางเกม, ลบไฟล์ระหว่างเล่น, บันทึกไม่สำเร็จ
- **การยืนยันความถูกต้อง:** history และสถิติต้องสอดคล้องกัน ไม่มีเกมค้าง และข้อมูลที่ผู้ใช้แก้ด้วยมือไม่ถูกเขียนทับ

### 🔹 TC-25: Hint Redraw (ยังไม่ผ่าน)
- **การทดสอบ:** `hint` แล้วทายถูก โดยจับค่า `message` ที่ส่งเข้า `render_game_screen`
- **สาเหตุ:** เทสต์เขียนตามแนวคิดเดิม (ส่ง hint ผ่าน `message=`) แต่โค้ดพิมพ์ hint ตรงใต้กระดานและข้ามการวาดใหม่ในรอบนั้น
- **ผลต่อผู้ใช้:** hint แสดงถูกต้อง ปัญหาอยู่ที่การตรวจของเทสต์
- **แนวทางแก้:** ปรับเทสต์ให้ตรวจ output ของ hint และ `_last_render_lines` หรือแก้โค้ดให้ส่ง `message=`

---

## 🧪 Automated Test Evidence

คำสั่งที่ใช้:

```text
python -m pytest -q
```

ผลล่าสุด (2026-09-29):

```text
1 failed, 71 passed
```

ไฟล์ test ที่เกี่ยวข้อง:

- [tests/test_cli.py](test_cli.py) — 20
- [tests/test_logic.py](test_logic.py) — 10
- [tests/test_word_bank.py](test_word_bank.py) — 13
- [tests/test_sprint3.py](test_sprint3.py) — 17
- [tests/test_boardrenderer.py](test_boardrenderer.py) — 2
- [tests/test_word_api.py](test_word_api.py) — 5
- [tests/test_today_word.py](test_today_word.py) — 5

> หมายเหตุ: เทสต์ของ API ภายนอกใช้ fake response และ monkeypatch เพื่อให้ผล deterministic และไม่ขึ้นกับสถานะอินเทอร์เน็ตขณะรันทดสอบ