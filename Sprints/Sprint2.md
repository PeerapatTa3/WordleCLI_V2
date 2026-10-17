# Sprint 2: Back-End App Development — Business Logic & Data Layer

## 1. สถานะปัจจุบัน

Sprint 2 เสร็จสมบูรณ์แล้วและผ่านการตรวจสอบด้วยการรันเทสต์จริงของโปรเจกต์ โดยผลรวม ณ ปิด Sprint: **35 passed** (ปัจจุบันทั้งโปรเจกต์มี 93 เคส ดู [Sprint4.md](Sprint4.md))

## 2. Scope ที่ทำเสร็จ

### Phase 1: Planning

- กำหนดโครงสร้าง Business Logic และ Data Access ใน [PLAN.md](../PLAN.md)
- แยก logic เกมออกจาก CLI เพื่อให้เป็น Domain Model และ data helper ที่ชัดเจน
- กำหนด DoD สำหรับการจัดการคำศัพท์, history, validation, และ exception handling

### Phase 2: Execution

- สร้างคลาส `WordleGame` ใน [src/game_logic.py](../src/game_logic.py)
- แยก `calculate_feedback()` สำหรับคำนวณผลตอบกลับแบบ Wordle
- สร้างฟังก์ชัน `search_history()` และ `filter_history()` สำหรับค้นหาและกรองประวัติ
- สร้าง `save_data()` และ `load_data()` ใน [src/data_manager.py](../src/data_manager.py)
- สร้าง `load_word_pool()` เพื่อโหลดคำศัพท์และ fallback เมื่อไฟล์ว่าง/หาย
- ดึงคำศัพท์จาก Datamuse และตรวจ validity ผ่าน Dictionary API ใน `src/word_api.py`
- เพิ่ม retry และ cache สำหรับ handling API timeout
- **หมายเหตุ:** ส่วน API นี้ถูกแทนที่ใน Sprint 3 ด้วย offline-first word bank (ดู [Sprint3.md](Sprint3.md)); โค้ด Datamuse ย้ายไป `scripts/`

### Phase 3: Review & Testing

- ทดสอบกรณีไฟล์ JSON หายหรือเสียหาย
- ทดสอบคำที่เป็นคำที่มีความหมาย/ไม่มีความหมาย
- ทดสอบการค้นหาและกรองประวัติคำทาย
- ทดสอบการรันโปรเจกต์แบบ end-to-end ผ่าน pytest

---

## 3. ผลการทดสอบจริง (Verified)

| รายการทดสอบ | ผลลัพธ์ |
| :--- | :--- |
| `calculate_feedback()` | สำเร็จ |
| `WordleGame` state tracking | สำเร็จ |
| Search history | สำเร็จ |
| Filter history | สำเร็จ |
| Save/load JSON | สำเร็จ |
| word_pool fallback | สำเร็จ |
| Datamuse/Dictionary API helpers | สำเร็จ (ตอนจบ Sprint 2; ถูกแทนที่ใน Sprint 3) |
| Test suite ของโปรเจกต์ ณ สิ้นสุด Sprint 2 | 35 passed |

---

## 4. สรุปบทเรียน

### Wow!
- Business Logic และ Data Access ถูกแยกจาก UI อย่างชัดเจน
- ระบบสามารถจัดการ file I/O, search/filter, และ API validation ได้ดี
- ปลอดภัยมากขึ้นเมื่อมี API timeout หรือไฟล์เสียหาย

### Whoops!
- เริ่มต้นมีปัญหาเรื่อง import path ของ test และ retry ของ Dictionary API
- ได้แก้ไขแล้วและยืนยันผ่านการทดสอบจริง

---

## 5. Deliverable Status

- [x] Business Logic ของ Wordle ถูกแยกออกจาก Presentation Layer
- [x] Data persistence ด้วย JSON ทำงานได้จริง
- [x] Search, filter, and validation logic ทำงานตามที่กำหนด
- [x] ผ่านการทดสอบอัตโนมัติของโปรเจกต์
- [x] เอกสารและโค้ดสอดคล้องกับสถานะจริงของโปรเจกต์

---

# การประเมินตนเองแยกตามบทบาท (Role-Based Grading Rubrics)

## Sprint 2 — Back-End App Dev

**บทบาท:** Planner = นายพีรพัฒน์ แท่นประยุทร 673380288-6 (ซอก) | Coder = นายพีรพล แก้วเจริญสันติสุข 673380287-8 (พี) | Debugger = นายพิสิษฐ์ ทรัพย์อุดมโชติ 673380285-2 (เทน)

### การประเมินบทบาท Planner (นักวางแผนและสถาปนิก)
### นายพีรพัฒน์ แท่นประยุทร 673380288-6 (ซอก) — Planner

| เกณฑ์การประเมิน                   | นายพีรพัฒน์ (Self) |  นายพีรพล | นายพิสิษฐ์ | สรุปคะแนน (0–10) |
| --------------------------------- | :--------: | :-: | :-: | :--------------: |
| การวางแผนและกำหนดขอบเขตงาน        |     10     |  10 |  10 |        10        |
| การนิยาม Definition of Done (DoD) |     10     |  10 |  10 |        10        |
| การจัดทำเอกสารโครงการ             |     10     |  10 |   9 |       9.67       |
| **รวมคะแนนบุคคล**                 |     10     |  10 | 9.67|   **9.89/10**    |

### การประเมินบทบาท Coder (นักเขียนโค้ด)
### นายพีรพล แก้วเจริญสันติสุข 673380287-8 (พี) — Coder

| เกณฑ์การประเมิน                | นายพีรพัฒน์ | นายพีรพล (Self) | นายพิสิษฐ์ | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-------: | :-: | :--------------: |
| การจัดโครงสร้างโค้ดและโมดูล    |  10 |     10    |  10 |        10        |
| การจัดการอินพุตและสถานะโปรแกรม |  10 |     10    |  10 |        10        |
| มาตรฐานและอ่านง่ายของโค้ด      |  10 |     10    |  10 |        10        |
| **รวมคะแนนบุคคล**              |  10 |     10    |  10 |    **10/10**     |

### การประเมินบทบาท Debugger (นักทดสอบและประกันคุณภาพ)
### นายพิสิษฐ์ ทรัพย์อุดมโชติ 673380285-2 (เทน) — Debugger

| เกณฑ์การประเมิน                | นายพีรพัฒน์ |  นายพีรพล | นายพิสิษฐ์ (Self) | สรุปคะแนน (0–10) |
| ------------------------------ | :-: | :-: | :--------: | :--------------: |
| การทดสอบเคสขอบเขต (Edge Cases) |  10 |  10 |     10     |        10        |
| การจัดการ Exception Handling   |  10 |  10 |     10     |        10        |
| การรายงานผลและการส่งมอบงาน     |  10 |  10 |      8     |       9.33       |
| **รวมคะแนนบุคคล**              |  10 |  10 |    9.33    |   **9.78/10**    |
