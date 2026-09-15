# PLAN.md — Miniproject_WordleCLI (Sprint1)
> ร่างแผนงานทั้ง 4 Sprint (แต่ละ Sprint ควรแยกเป็นไฟล์ `PLAN.md` ของตัวเอง หรือ commit ทับใน Sprint ถัดไปตามที่ทีมตกลงกัน)

---

# Sprint 1: Front-End App Dev
**สัปดาห์ที่ 12 | นำเสนอ 15-16/9/69 | ส่ง 18/9/69**

## 0. บทบาททีม (Team Roles)
| บทบาท | ผู้รับผิดชอบ |
|---|---|
| Planner / PM | เทน |
| Coder | ซอก |
| Debugger / QA | พี |

## 1. เป้าหมาย (Goal)
ปรับโครงสร้าง CLI ของเกม Wordle จากโค้ดปัจจุบันที่รวมทุกอย่างไว้ในฟังก์ชันเดียว (`run_wordle_cli()`) ให้แยกเป็นฟังก์ชันย่อยตามหน้าที่ในชั้น Presentation Layer พร้อมตรวจสอบความถูกต้องของอินพุต

## 2. ขอบเขตระบบ (Scope)
- แสดงข้อความต้อนรับ (banner)
- แสดงเมนูหลัก 4 ตัวเลือก: Play / View & Sort History / Remove Word / Exit
- รับคำสั่งจากผู้ใช้ พร้อม `.strip()` และแปลงตัวพิมพ์ให้เป็นมาตรฐาน
- ตรวจสอบอินพุตคำทาย (ความยาวตรง 5 ตัวอักษร, เป็นตัวอักษรล้วน)

## 3. ฟังก์ชันที่ต้องส่งมอบ
| ฟังก์ชัน | หน้าที่ |
|---|---|
| `display_welcome_message()` | แสดง banner ต้อนรับเข้าเกม |
| `display_menu()` | แสดงเมนู 1-4 |
| `get_menu_choice()` | รับ+ทำความสะอาดอินพุตเมนู (`.strip()`) |
| `get_guess_input(word_length)` | รับคำทาย, บังคับ `.upper().strip()` |
| `is_valid_guess(guess, word_length)` | ตรวจความยาว/ตัวอักษรล้วน คืนค่า True/False |
| `main()` / `run_wordle_cli()` | ควบคุม while-loop หลัก เรียกใช้ฟังก์ชันข้างต้น |

## 4. Definition of Done (DoD)
- [ ] เลือกเมนูนอกช่วง 1-4 (เช่น `0`, `abc`, ว่าง) ต้องไม่ทำโปรแกรมพัง และแสดงข้อความแจ้งเตือน
- [ ] คำทายที่ความยาวไม่ตรง 5 ตัวอักษร หรือมีตัวเลข/สัญลักษณ์ปน ต้องถูกปฏิเสธและให้กรอกใหม่
- [ ] พิมพ์ตัวเล็ก/ใหญ่ปนกัน (`play`, `PLAY`, `Play`) ต้องทำงานเหมือนกัน
- [ ] ทุกฟังก์ชันมี Docstring อธิบายหน้าที่
- [ ] โค้ดไม่มีฟังก์ชันใดยาวเกินจำเป็น (แยกตาม Single Responsibility)

## 5. Edge Case ที่ต้องทดสอบ (Debugger)
- เมนู: ค่าว่าง, ตัวอักษร, ตัวเลขนอกช่วง, ช่องว่างนำหน้า/ตามหลัง
- คำทาย: สั้น/ยาวเกิน 5, มีตัวเลข, มีช่องว่างตรงกลาง, พิมพ์เล็กทั้งหมด

## 6. Deliverable
- PR พร้อมสรุป **Wow!** / **Whoops!**
- รายงาน QA (Observation / Expected / Actual) ตามแบบฟอร์ม

---

# Sprint 2: Back-End App Dev
**สัปดาห์ที่ 13 | นำเสนอ 22-23/9/69 | ส่ง 25/9/69**

## 0. บทบาททีม (Team Roles) — สลับจาก Sprint 1
| บทบาท | ผู้รับผิดชอบ |
|---|---|
| Planner / PM | ซอก |
| Coder | พี |
| Debugger / QA | เทน |

## 1. เป้าหมาย (Goal)
แยก Business Logic และ Data Access ออกจาก CLI ให้เป็นชั้นอิสระ พร้อมเพิ่มฟังก์ชัน Search/Filter, การจัดการไฟล์ และ Exception Handling ที่ยังขาดอยู่ในโค้ดปัจจุบัน

## 2. ขอบเขตระบบ (Scope)
- ย้าย logic เกม (สุ่มคำ, คำนวณ feedback ✓/-/x) ออกจาก loop หลัก
- เพิ่มฟังก์ชัน Search และ Filter ต่อยอดจาก Sort ที่มีอยู่แล้ว
- เพิ่ม Data Persistence: บันทึก/โหลด `guess_history` และ/หรือ word pool ลงไฟล์ JSON
- ครอบข้อผิดพลาดที่อาจเกิดขึ้น (อ่าน/เขียนไฟล์, อินพุตผิดประเภท) ด้วย `try-except`

## 3. ฟังก์ชัน/คลาสที่ต้องส่งมอบ
| ฟังก์ชัน/คลาส | หน้าที่ |
|---|---|
| `class WordleGame` | เก็บ state ของเกม (secret_word, attempts, word_length) เป็น Domain Model |
| `calculate_feedback(guess, secret_word)` | คำนวณ ✓/-/x แยกจาก loop |
| `search_history(history, keyword)` | ค้นหาคำที่เคยทายจาก `guess_history` |
| `filter_history(history, condition)` | กรอง เช่น เฉพาะคำที่ทายถูก |
| `save_data(filepath, data)` | เขียนข้อมูลลง JSON พร้อม `try-except` |
| `load_data(filepath)` | โหลดข้อมูล พร้อมจัดการกรณีไฟล์ไม่พบ (`FileNotFoundError`) |

## 4. Definition of Done (DoD)
- [ ] `guess_history` ถูกบันทึกลงไฟล์ JSON และโหลดกลับมาได้ถูกต้องเมื่อเปิดโปรแกรมใหม่
- [ ] ไฟล์ข้อมูลหายหรือเสียหาย → โปรแกรมไม่ crash (จับด้วย try-except พร้อมสร้างไฟล์ใหม่/ค่าเริ่มต้น)
- [ ] มีฟังก์ชัน Search ที่คืนผลลัพธ์ถูกต้องเมื่อค้นคำที่มี/ไม่มีใน history
- [ ] มีฟังก์ชัน Filter ที่แยกคำทายถูก/ผิดได้ถูกต้อง
- [ ] Business Logic (`WordleGame`, `calculate_feedback`) ไม่เรียก `print()`/`input()` โดยตรง (แยกจาก Presentation Layer)

## 5. Edge Case ที่ต้องทดสอบ (Debugger)
- โหลดไฟล์ที่ไม่มีอยู่จริง / ไฟล์ JSON รูปแบบผิด
- ค้นหา/กรองด้วย history ว่างเปล่า
- บันทึกไฟล์ตอนไม่มีสิทธิ์เขียน (permission)

## 6. Deliverable
- PR พร้อมสรุป **Wow!** / **Whoops!**
- ตัวอย่างไฟล์ข้อมูลที่ถูกบันทึก (เช่น `history.json`)

---

# Sprint 3: Full-Stack App Dev
**สัปดาห์ที่ 14 | นำเสนอ 29-30/9/69 | ส่ง 2/10/69**

## 0. บทบาททีม (Team Roles) — สลับจาก Sprint 2
| บทบาท | ผู้รับผิดชอบ |
|---|---|
| Planner / PM | พี |
| Coder | เทน |
| Debugger / QA | ซอก |

## 1. เป้าหมาย (Goal)
เชื่อมต่อ Front-End (Sprint 1) และ Back-End (Sprint 2) เข้าด้วยกันให้ทำงานเป็นระบบเดียวสมบูรณ์ จัดการ State ให้สอดคล้องกันตลอดการเล่น และครอบคลุม Edge Case ที่เกิดจากการเชื่อมต่อ

## 2. ขอบเขตระบบ (Scope)
- ปรับ `main()` ให้เรียกใช้ทั้งฟังก์ชัน Presentation (Sprint 1) และ Business/Data Layer (Sprint 2) ผ่าน interface เดียวกัน
- ให้ State ของเกม (word_pool, guess_history, ผลของแต่ละตา) sync ระหว่างเมนูต่างๆ อย่างถูกต้อง (เช่น ลบคำออกจาก pool แล้วต้องไม่สุ่มคำนั้นได้อีก)
- เพิ่มการจัดการ Edge Case ที่เกิดเฉพาะตอนระบบทำงานร่วมกัน เช่น pool ว่างระหว่างเล่น, ไฟล์ข้อมูลถูกแก้ไขระหว่างรัน

## 3. งานที่ต้องส่งมอบ
| งาน | รายละเอียด |
|---|---|
| Integration ของทุก Layer | `main()` เรียก Presentation → Business Logic → Data Access ตามลำดับชัดเจน |
| State Management | ตรวจสอบว่าทุกเมนู (Play/History/Remove/Exit) เห็นข้อมูลชุดเดียวกันที่อัปเดตล่าสุด |
| Edge Case: Full Integration | เช่น ลบคำจน pool ว่าง → auto-reset, บันทึกไฟล์ทุกครั้งที่จบเกม |

## 4. Definition of Done (DoD)
- [ ] เล่นเกมจบ 1 ตา → history ถูกบันทึกลงไฟล์ทันที ไม่ต้องรอปิดโปรแกรม
- [ ] ลบคำออกจาก pool แล้ว เริ่มเกมใหม่ต้องไม่สุ่มคำที่ถูกลบไปแล้ว
- [ ] สลับเมนูไปมา (เล่น → ดู history → ลบคำ → เล่นอีกครั้ง) ข้อมูลต้อง consistent ไม่มีค่าตกหล่น
- [ ] ทดสอบ end-to-end ตั้งแต่เปิดโปรแกรมจนปิด ไม่มี unhandled exception

## 5. Edge Case ที่ต้องทดสอบ (Debugger)
- ลบคำจนหมด pool ระหว่างเล่นหลายรอบติดกัน
- ปิดโปรแกรมกลางเกม (เมนู 4) แล้วเปิดใหม่ ข้อมูลต้องยังอยู่ครบ
- แก้ไข/ลบไฟล์ข้อมูลด้วยมือระหว่างที่โปรแกรมกำลังรัน

## 6. Deliverable
- PR พร้อมสรุป **Wow!** / **Whoops!**
- Diagram หรือคำอธิบายสั้นๆ ว่าแต่ละ Layer เชื่อมกันอย่างไร (เตรียมไว้ใช้ตอนนำเสนอส่วนที่ 1)

---

# Sprint Final: DevOps, CI/CD & AI Integration
**สัปดาห์ที่ 15 | นำเสนอ 6-7/10/69 | ส่ง 16/10/69**

## 0. บทบาททีม (Team Roles)
> Sprint นี้ไม่หมุนเวียนบทบาทตาม Planner/Coder/Debugger แล้ว เพราะตามสเปกกำหนดให้ทำงานตามความเชี่ยวชาญเฉพาะบุคคล (เทน / ซอก / พี ตกลงแบ่งงาน CI/CD, Testing, AI Integration กันเองตามถนัด)

## 1. เป้าหมาย (Goal)
เพิ่มระบบทดสอบอัตโนมัติ ตั้งค่า CI/CD ผ่าน GitHub Actions และผนวกฟีเจอร์ AI/Automation เข้ากับโปรเจกต์ พร้อมสรุปแนวทางต่อยอด

## 2. ขอบเขตระบบ (Scope)
- เขียน Unit Test ครอบคลุม Business Logic (`calculate_feedback`, `search_history`, `filter_history`, `save_data`/`load_data`)
- ตั้งค่า GitHub Actions workflow: รัน Linting + Unit Test อัตโนมัติทุกครั้งที่ push/PR
- เพิ่มฟีเจอร์ AI หรือ Automation Agent เช่น วิเคราะห์สถิติการเล่น หรือแนะนำคำใบ้อัตโนมัติ
- สรุปอุปสรรคที่พบตลอด Sprint 1-3 และแนวทาง Refactor

## 3. งานที่ต้องส่งมอบ
| งาน | รายละเอียด |
|---|---|
| `tests/test_logic.py` | Unit test ด้วย `unittest` หรือ `pytest` |
| `.github/workflows/ci.yml` | Workflow รัน lint (เช่น `flake8`) + test อัตโนมัติ |
| ฟีเจอร์ AI/Automation | เช่น สรุปสถิติคำที่ทายบ่อย หรือ agent ช่วยวิเคราะห์ผล |
| เอกสารสรุป Refactor | เปรียบเทียบทางเลือกโครงสร้างข้อมูล/สถาปัตยกรรมที่ใช้จริงกับทางเลือกอื่น |

## 4. Definition of Done (DoD)
- [ ] Unit test ครอบคลุมฟังก์ชันหลักของ Business/Data Layer อย่างน้อย 80% ของเคสสำคัญ (ปกติ + edge case)
- [ ] CI pipeline รันผ่านอัตโนมัติเมื่อเปิด PR และ block การ merge ถ้า test ไม่ผ่าน
- [ ] ฟีเจอร์ AI ทำงานได้จริงและสาธิตได้ใน Live Demo
- [ ] มีเอกสารสรุปปัญหาเทคนิคที่พบใน Sprint 1-3 พร้อมวิธีแก้ไข

## 5. สิ่งที่ต้องเตรียมนำเสนอ (5 ส่วนตาม Rubric)
1. ปัญหา สถาปัตยกรรม และ UML Class Diagram
2. Tech stack, เวอร์ชัน Python, ไลบรารี, Design Pattern ที่ใช้
3. Live Demo ครบทุกฟังก์ชัน + Algorithm (search/filter/sort) + ทดสอบ error
4. สรุปปัญหาเทคนิคที่พบ + การเปรียบเทียบทางเลือก
5. สาธิต CI/CD บน GitHub Actions + ฟีเจอร์ AI + แนวทางต่อยอด

## 6. Deliverable
- Repository พร้อม CI/CD ที่ทำงานจริง
- โค้ด, เอกสาร, รายงานทั้งหมดของโปรเจกต์ (final artifacts)
