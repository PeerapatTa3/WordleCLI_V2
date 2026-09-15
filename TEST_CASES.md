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
| **TC-04** | Word Meaning Validation | ตรวจคำอังกฤษที่มีความหมาย | `HELLO`, `WORLD` | ยอมรับคำ 5 ตัวอักษรที่อยู่ใน API/local fallback | คำทั้งสองคำถูกยอมรับจาก local fallback | **PASSED** |
| **TC-05** | Unknown Word Protection | ป้องกันคำมั่ว | `QZXJK` | ปฏิเสธคำที่ไม่พบใน word sources | คำที่ไม่รู้จักถูกปฏิเสธ | **PASSED** |
| **TC-06** | Wordle Algorithm | คำนวณ feedback | Guess `ALLEY`, Secret `APPLE` | คืนค่า `✓`, `-`, `x` ตามกติกาตัวอักษรซ้ำ | ได้ `['✓', '-', 'x', '-', 'x']` | **PASSED** |
| **TC-07** | API Ingestion | ดึงรายการคำ 5 ตัวอักษร | Datamuse wildcard endpoint | ได้รายการคำภาษาอังกฤษพร้อม score | ได้รายการคำที่ผ่าน filter และสุ่มได้คำใช้งานจริง | **PASSED** |
| **TC-08** | Dictionary Validation | ตรวจ definition ของคำ | Dictionary API + `HELLO` | API คืน meanings และรับคำ | Test fake response ยืนยัน `HELLO` ผ่าน | **PASSED** |
| **TC-14** | Dictionary Reliability | retry และ cache definition | Timeout 2 ครั้ง แล้ว response สำเร็จ | ลองใหม่และจำคำที่ตรวจผ่าน | `WORLD` ผ่านในครั้งที่ 3 และ `UPPER` ใช้ cache ได้ | **PASSED** |
| **TC-09** | JSON Persistence | บันทึก/โหลดประวัติ | History payload | ข้อมูลที่โหลดกลับมาต้องเหมือนข้อมูลที่บันทึก | Round-trip และ corrupted-file handling ผ่าน | **PASSED** |
| **TC-10** | API Fallback | API ล้มเหลว | Network exception / timeout | ใช้ local word pool และโปรแกรมไม่ crash | `HELLO` และ `WORLD` ยังใช้ได้ | **PASSED** |
| **TC-11** | Statistics | คำนวณสถิติผู้เล่น | History หลายเกม | แสดง games, win rate, streak และ distribution | แสดงผลสถิติถูกต้อง | **PASSED** |
| **TC-12** | Hint / Answer | ใช้คำสั่งช่วยระหว่างเล่น | `hint`, `answer` | Hint เปิดตัวอักษรโดยไม่เสียรอบ; answer แสดงเฉลยและจบรอบ | ทั้งสองคำสั่งทำงานตามที่กำหนด | **PASSED** |
| **TC-13** | Legacy History View | ดูประวัติแบบรายเกม | History หลายเกม | แสดงสถานะ, secret word และลำดับคำทายต่อเกม | แสดง `Game 1 (WON...)` และ `Guesses: ... -> ...` | **PASSED** |

---

## 🔬 รายละเอียดเคสการทดสอบเชิงลึก (Detailed Test Case Specs)

### 🔹 TC-01 & TC-02: CLI Menu and Defensive Input
- **การทดสอบ:** เปิดโปรแกรมและเลือกคำสั่งที่ถูกต้อง/ผิด
- **เงื่อนไข:** ใช้ `1` ถึง `5`, รวมถึง `0`, `abc` และค่าว่าง
- **การยืนยันความถูกต้อง:** โปรแกรมต้องไม่หยุดทำงานจาก invalid menu input และต้องแสดงข้อความแจ้งเตือน

### 🔹 TC-03 & TC-05: Guess and Meaning Validation
- **การทดสอบ:** ป้อนคำที่รูปแบบผิด คำที่มีความหมาย และคำสุ่มตัวอักษร
- **เงื่อนไข:** คำต้องยาว 5 ตัวอักษรและเป็นภาษาอังกฤษ
- **การยืนยันความถูกต้อง:** ใช้ Datamuse list, Dictionary API exact lookup และ local fallback ร่วมกัน

### 🔹 TC-06: Wordle Feedback Algorithm
- **การทดสอบ:** ทดสอบ exact match, wrong-position match และ duplicate letters
- **ตัวอย่าง:** `ALLEY` เทียบกับ `APPLE`
- **การยืนยันความถูกต้อง:** ตัวอักษรที่ใช้ได้เท่านั้นจึงได้รับ `-` และตัวที่ตรงตำแหน่งได้รับ `✓`

### 🔹 TC-07 & TC-08: External API Integration
- **การทดสอบ:** ตรวจ response จาก Datamuse และ Dictionary API
- **การยืนยันความถูกต้อง:** กรองคำให้ยาว 5 ตัวอักษร เป็น alphabetic และมี definition เมื่อค้น exact word
- **Error Case:** network failure, timeout, malformed JSON และ empty response ต้องไม่ทำให้เกม crash

### 🔹 TC-09: JSON Persistence
- **การทดสอบ:** บันทึก guess history แล้วโหลดกลับมา
- **การยืนยันความถูกต้อง:** ข้อมูลต้องตรงกันหลัง round-trip และ corrupted JSON ต้องคืนค่า list ว่างอย่างปลอดภัย

### 🔹 TC-11 & TC-12: Integrated Game Features
- **การทดสอบ:** เล่นเกมแล้วเปิด History, Statistics, How to Play รวมถึงใช้ `hint` และ `answer`
- **การยืนยันความถูกต้อง:** state และ history ต้องไม่หาย และคำสั่งช่วยต้องไม่ทำให้ game loop crash

---

## 🧪 Automated Test Evidence

คำสั่งที่ใช้:

```text
.venv\Scripts\python.exe -m pytest -q
```

ผลล่าสุด:

```text
35 passed in 0.13s
```

ไฟล์ test ที่เกี่ยวข้อง:

- [tests/test_cli.py](tests/test_cli.py)
- [tests/test_logic.py](tests/test_logic.py)
- [tests/test_word_api.py](tests/test_word_api.py)

> หมายเหตุ: ผลทดสอบ API ภายนอกใช้ fake response และ monkeypatch เพื่อให้ผล deterministic และไม่ขึ้นกับสถานะอินเทอร์เน็ตขณะรันทดสอบ
