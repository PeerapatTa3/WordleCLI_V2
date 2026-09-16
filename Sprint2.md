# Sprint 2: Back-End App Development — Business Logic & Data Layer

## 1. สถานะปัจจุบัน

Sprint 2 เสร็จสมบูรณ์แล้วและผ่านการตรวจสอบด้วยการรันเทสต์จริงของโปรเจกต์ โดยผลรวม: **35 passed**

## 2. Scope ที่ทำเสร็จ

### Phase 1: Planning

- กำหนดโครงสร้าง Business Logic และ Data Access ใน [PLAN.md](PLAN.md)
- แยก logic เกมออกจาก CLI เพื่อให้เป็น Domain Model และ data helper ที่ชัดเจน
- กำหนด DoD สำหรับการจัดการคำศัพท์, history, validation, และ exception handling

### Phase 2: Execution

- สร้างคลาส `WordleGame` ใน [src/game_logic.py](src/game_logic.py)
- แยก `calculate_feedback()` สำหรับคำนวณผลตอบกลับแบบ Wordle
- สร้างฟังก์ชัน `search_history()` และ `filter_history()` สำหรับค้นหาและกรองประวัติ
- สร้าง `save_data()` และ `load_data()` ใน [src/data_manager.py](src/data_manager.py)
- สร้าง `load_word_pool()` เพื่อโหลดคำศัพท์และ fallback เมื่อไฟล์ว่าง/หาย
- ดึงคำศัพท์จาก Datamuse และตรวจ validity ผ่าน Dictionary API ใน [src/word_api.py](src/word_api.py)
- เพิ่ม retry และ cache สำหรับ handling API timeout

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
| Datamuse/Dictionary API helpers | สำเร็จ |
| Test suite ของโปรเจกต์ | 35 passed |

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