# PLAN.md — Miniproject_WordleCLI
> ร่างแผนงานทั้ง 4 Sprint (แต่ละ Sprint ควรแยกเป็นไฟล์ `PLAN.md` ของตัวเอง หรือ commit ทับใน Sprint ถัดไปตามที่ทีมตกลงกัน)

---

# Sprint 1: Front-End App Dev

## 0. บทบาททีม (Team Roles)
| บทบาท | ผู้รับผิดชอบ |
|---|---|
| Planner / PM | เทน |
| Coder | ซอก |
| Debugger / QA | พี |

## 1. เป้าหมาย (Goal)
ปรับโครงสร้าง CLI ของเกม Wordle ให้แยกเป็นฟังก์ชันย่อยตามหน้าที่ในชั้น Presentation Layer พร้อมตรวจสอบความถูกต้องของอินพุต

## 2. ขอบเขตระบบ (Scope)
- แสดงข้อความต้อนรับ (banner)
- แสดงเมนูหลัก: Play / View History / View Statistics / How to Play / Exit
- รับคำสั่งจากผู้ใช้ พร้อม `.strip()` และแปลงตัวพิมพ์ให้เป็นมาตรฐาน
- ตรวจสอบอินพุตคำทาย (ความยาวตรง 5 ตัวอักษร, เป็นตัวอักษรล้วน และอยู่ใน word pool)
- รองรับคำสั่งระหว่างเล่น `hint` และ `answer`

## 3. ฟังก์ชันที่ต้องส่งมอบ
| ฟังก์ชัน | หน้าที่ |
|---|---|
| `display_welcome_message()` | แสดง banner ต้อนรับเข้าเกม |
| `display_menu()` | แสดงเมนู 1-5 |
| `get_menu_choice()` | รับ+ทำความสะอาดอินพุตเมนู (`.strip()`) |
| `get_guess_input(word_length, valid_words)` | รับคำทายหรือคำสั่ง `hint`/`answer` |
| `is_valid_guess(guess, word_length, valid_words)` | ตรวจความยาว/ตัวอักษร/การอยู่ในคลังคำ |
| `display_hint()` / `display_answer()` | แสดงคำใบ้หรือคำเฉลยระหว่างเล่น |
| `main()` | ควบคุม while-loop หลัก เรียกใช้ฟังก์ชันข้างต้น |

## 4. Definition of Done (DoD)
- [x] เลือกเมนูนอกช่วง 1-5 (เช่น `0`, `abc`, ว่าง) ต้องไม่ทำโปรแกรมพัง และแสดงข้อความแจ้งเตือน
- [x] คำทายที่ความยาวไม่ตรง 5 ตัวอักษร หรือมีตัวเลข/สัญลักษณ์ปน ต้องถูกปฏิเสธและให้กรอกใหม่
- [x] คำทายที่ไม่อยู่ใน word pool ต้องถูกปฏิเสธ
- [x] พิมพ์ตัวเล็ก/ใหญ่ปนกัน (`play`, `PLAY`, `Play`) ต้องทำงานเหมือนกัน
- [x] ทุกฟังก์ชันมี Docstring อธิบายหน้าที่
- [x] โค้ดไม่มีฟังก์ชันใดยาวเกินจำเป็น (แยกตาม Single Responsibility)

## 5. Edge Case ที่ต้องทดสอบ (Debugger)
- เมนู: ค่าว่าง, ตัวอักษร, ตัวเลขนอกช่วง, ช่องว่างนำหน้า/ตามหลัง
- คำทาย: สั้น/ยาวเกิน 5, มีตัวเลข, มีช่องว่างตรงกลาง, พิมพ์เล็กทั้งหมด

## 6. Deliverable
- PR พร้อมสรุป **Wow!** / **Whoops!**
- รายงาน QA (Observation / Expected / Actual) ตามแบบฟอร์ม
- Test Plan และ Test Cases: [TEST_PLAN.md](./tests/TEST_PLAN.md)
- ตาราง Test Cases: [TEST_CASES.md](./tests/TEST_CASES.md)

---

# Sprint 2: Back-End App Dev

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
- เชื่อม Datamuse API สำหรับคำอังกฤษ 5 ตัวอักษร พร้อม fallback ไป local word pool
  - *(หมายเหตุ: ออกแบบเดิมของ Sprint 2 — ถูกแทนที่ใน Sprint 3 ด้วย offline-first word bank)*
- รองรับ `WORDLE_TEST_WORD` สำหรับการทดสอบแบบกำหนดคำเฉลย โดยไม่เปิดเผยคำตอบในโหมดปกติ

## 3. ฟังก์ชัน/คลาสที่ต้องส่งมอบ
| ฟังก์ชัน/คลาส | หน้าที่ |
|---|---|
| `class WordleGame` | เก็บ state ของเกม (secret_word, attempts, word_length) เป็น Domain Model |
| `calculate_feedback(guess, secret_word)` | คำนวณ ✓/-/x แยกจาก loop |
| `search_history(history, keyword)` | ค้นหาคำที่เคยทายจาก `guess_history` |
| `filter_history(history, condition)` | กรอง เช่น เฉพาะคำที่ทายถูก |
| `save_data(filepath, data)` | เขียนข้อมูลลง JSON พร้อม `try-except` |
| `load_data(filepath)` | โหลดข้อมูล พร้อมจัดการกรณีไฟล์ไม่พบ (`FileNotFoundError`) |
| `load_word_pool(filepath)` | โหลดคลังคำแบบอ่านอย่างเดียวและสร้างค่าเริ่มต้นเมื่อไฟล์หาย |
| `fetch_random_word()` | ดึงคำที่มีความหมายจาก Datamuse และกรองตาม score |
| `fetch_valid_words()` | ดึงและคืนรายการคำ 5 ตัวอักษรทั้งหมดที่ผ่านการกรองจาก Datamuse |
| `is_valid_dictionary_word()` | ตรวจ exact word ว่ามี definition จาก Dictionary API |
| `DICTIONARY_RETRIES` / `DICTIONARY_CACHE` | retry การตรวจ definition และจำคำที่ตรวจผ่านแล้ว |

## 4. Definition of Done (DoD)
- [x] `guess_history` ถูกบันทึกลงไฟล์ JSON และโหลดกลับมาได้ถูกต้องเมื่อเปิดโปรแกรมใหม่
- [x] ไฟล์ข้อมูลหายหรือเสียหาย → โปรแกรมไม่ crash (จับด้วย try-except พร้อมสร้างไฟล์ใหม่/ค่าเริ่มต้น)
- [x] มีฟังก์ชัน Search ที่คืนผลลัพธ์ถูกต้องเมื่อค้นคำที่มี/ไม่มีใน history
- [x] มีฟังก์ชัน Filter ที่แยกคำทายถูก/ผิดได้ถูกต้อง
- [x] Business Logic (`WordleGame`, `calculate_feedback`) ไม่เรียก `print()`/`input()` โดยตรง (แยกจาก Presentation Layer)
- [x] word pool เป็นข้อมูลอ่านอย่างเดียวสำหรับเกม ไม่มีเมนูให้ผู้ใช้ลบคำ
- [x] API ล้มเหลวแล้วเกมยังใช้ local word pool ต่อได้

## 5. Edge Case ที่ต้องทดสอบ (Debugger)
- โหลดไฟล์ที่ไม่มีอยู่จริง / ไฟล์ JSON รูปแบบผิด
- ค้นหา/กรองด้วย history ว่างเปล่า
- บันทึกไฟล์ตอนไม่มีสิทธิ์เขียน (permission)

## 6. Deliverable
- PR พร้อมสรุป **Wow!** / **Whoops!**
- ตัวอย่างไฟล์ข้อมูลที่ถูกบันทึก (เช่น `history.json`)
- Test Plan และ Test Cases: [TEST_PLAN.md](./tests/TEST_PLAN.md)
- ตาราง Test Cases: [TEST_CASES.md](./tests/TEST_CASES.md)

---

# Sprint 3: Full-Stack App Dev

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
- ให้ State ของเกม (word bank, history, ผลของแต่ละตา) sync ระหว่างการเล่นและเมนูต่างๆ อย่างถูกต้อง
- เพิ่มการจัดการ Edge Case ที่เกิดเฉพาะตอนระบบทำงานร่วมกัน เช่น ไฟล์ข้อมูลถูกแก้ไข/ลบระหว่างรัน, บันทึกไม่สำเร็จ, เกมที่ยอมแพ้กลางคัน
- **Offline-first word bank:** ใช้ local word list ทั้งการสุ่มคำเฉลยและตรวจคำทาย เล่นได้ทั้ง online/offline
  - `data/answers.txt` = คำเฉลย, `data/valid_words.txt` = คำที่ทายได้ (`answers ⊆ valid_words` เสมอ)
  - ไม่มีการเรียก network ตอนเล่น ตรวจคำด้วย `set` lookup (เดิม Dictionary API ต่อคำทายช้า 3-10 วินาที)
  - โค้ด Datamuse ย้ายไป `scripts/` เป็นเครื่องมือ build-time (ยกเลิกแนวคิด `api_cache.json` / `refresh_from_api`)
- **In-place redraw:** กระดานวาดทับที่เดิม, คำที่พิมพ์ไม่ค้างบนจอ, error ของคำทายผิดแทนที่บรรทัดเดิม, ไม่ส่ง escape code เมื่อ output ไม่ใช่ terminal
- **Refactor เพื่อ Single Responsibility:** แยก `BoardRenderer` และ `history_manager` ออกจาก `cli.py`

## 3. งานที่ต้องส่งมอบ
| งาน | รายละเอียด |
|---|---|
| Integration ของทุก Layer | `main()` เรียก Presentation → Business Logic → Data Access ตามลำดับชัดเจน |
| State Management | ทุกเมนูเห็นข้อมูลชุดเดียวกัน; โหลด history ใหม่จากดิสก์ก่อนเขียนทุกครั้ง (`_persist`) |
| `load_word_bank(length)` | ใน `src/word_bank.py` คืน `(answers, valid_words)` จากไฟล์ local (path จาก `Path(__file__)`); ไฟล์หาย/ว่างใช้ `DEFAULT_WORD_POOL` |
| `is_valid_guess()` (ปรับปรุง) | ตรวจความยาว/ตัวอักษร/อยู่ใน `valid_words` ด้วย membership test (ไม่เรียก network) |
| `scripts/build_wordlists.py` | สร้าง `data/answers.txt` / `data/valid_words.txt` จาก source word list ครั้งเดียวแล้ว commit |
| `erase_lines()` / `clear_screen()` / `render_game_screen()` | redraw กระดานในที่เดิม |
| `BoardRenderer`, `history_manager` | แยกการวาดตารางและการคำนวณสถิติออกจาก `cli.py` |
| `MAX_ATTEMPTS`, `WORD_LENGTH` | แทนตัวเลข 6 / 5 ที่กระจายในโค้ด |
| `HISTORY_PATH` | อิงจาก `Path(__file__)` (เตรียมพร้อมสำหรับ global command ใน Sprint Final) |

## 4. Definition of Done (DoD)
- [x] เล่นเกมจบ 1 ตา → history ถูกบันทึกลงไฟล์ทันที ไม่ต้องรอปิดโปรแกรม
- [x] สลับเมนูไปมา (เล่น → ดู history → ดูสถิติ → เล่นอีกครั้ง) ข้อมูลต้อง consistent ไม่มีค่าตกหล่น
- [x] ทดสอบ end-to-end ตั้งแต่เปิดโปรแกรมจนปิด ไม่มี unhandled exception
- [x] ใช้ `hint` และ `answer` ระหว่างเล่นได้โดยไม่ทำให้เกม crash
- [x] เปิดเกมโดยไม่ต้องใช้อินเทอร์เน็ต → สุ่มคำและตรวจคำทายจาก local (มีเทสต์ยืนยันว่า `load_word_bank()` ไม่เปิด socket)
- [x] ตรวจคำทายแต่ละครั้งเสร็จทันที (ไม่รอ network)
- [x] ไม่มีการเรียก API ตอนเล่น จึงไม่มีกรณี API ช้า/ล่ม/timeout ที่ทำให้เกมค้าง
- [x] คำเฉลยทุกคำอยู่ใน `valid_words` เสมอ (answers ⊆ valid_words)
- [x] `WORDLE_TEST_WORD` ยังใช้งานได้ และคำนั้นถูกนับเป็นคำที่ทายได้
- [x] ไฟล์ word list หาย/ว่าง → ใช้ default pool ได้
- [x] ไฟล์ history ถูกลบ/แก้ระหว่างเล่น → ไม่ถูกเขียนทับด้วยข้อมูลเก่าในหน่วยความจำ
- [x] บันทึก history ไม่สำเร็จ → เตือนผู้เล่น 1 ครั้ง ไม่ crash
- [ ] `pytest` ผ่านทั้งหมด (ปัจจุบัน 71 จาก 72 เคส — เหลือ `test_hint_message_is_passed_to_next_redraw` ที่คาดพฤติกรรมต่างจากโค้ดปัจจุบัน)
- [ ] Manual check: Windows Terminal + Unix terminal, กระดานเดียวบนจอ, error ทับบรรทัดเดิมเมื่อผิดหลายครั้งติด

## 5. Edge Case ที่ต้องทดสอบ (Debugger)
- ปิดโปรแกรมกลางเกม (เมนู 5) แล้วเปิดใหม่ ข้อมูลต้องยังอยู่ครบ
- แก้ไข/ลบไฟล์ข้อมูลด้วยมือระหว่างที่โปรแกรมกำลังรัน
- เปิดเกมตอน offline
- `answers.txt` / `valid_words.txt` หาย ว่าง หรือมีแต่คำความยาวผิด → ใช้ built-in default ได้
- `history.json` ไม่ใช่ list (`{}`, `"abc"`, `42`, `null`) หรือมี record ที่ไม่ใช่ dict
- ใช้ `answer` กลางเกมแล้วดู history/สถิติ ต้องไม่มีเกมค้าง
- ป้อนคำผิดหลายครั้งติดกัน error ต้องไม่ซ้อน
- รันเกมจาก working directory อื่น ต้องใช้ history.json ไฟล์เดิม
- redirect output ไปไฟล์ ต้องไม่มี escape code หลุด

## 6. Deliverable
- PR พร้อมสรุป **Wow!** / **Whoops!**
- Diagram หรือคำอธิบายสั้นๆ ว่าแต่ละ Layer เชื่อมกันอย่างไร (ดู "สถาปัตยกรรม" ใน [README.md](./README.md))
- สรุปผล Sprint: [Sprints/Sprint3.md](./Sprints/Sprint3.md)
- Test Plan และ Test Cases: [TEST_PLAN.md](./tests/TEST_PLAN.md)
- ตาราง Test Cases: [TEST_CASES.md](./tests/TEST_CASES.md)

---

# Sprint Final: DevOps, CI/CD & AI Integration

## 0. บทบาททีม (Team Roles)
> Sprint นี้ไม่หมุนเวียนบทบาทตาม Planner/Coder/Debugger แล้ว เพราะตามสเปกกำหนดให้ทำงานตามความเชี่ยวชาญเฉพาะบุคคล (เทน / ซอก / พี ตกลงแบ่งงาน CI/CD, Testing, AI Integration กันเองตามถนัด)

## 1. เป้าหมาย (Goal)
เพิ่มระบบทดสอบอัตโนมัติ ตั้งค่า CI/CD ผ่าน GitHub Actions และผนวกฟีเจอร์ AI/Automation เข้ากับโปรเจกต์ พร้อมสรุปแนวทางต่อยอด

## 2. ขอบเขตระบบ (Scope)
- เขียน Unit Test ครอบคลุม Business Logic (`calculate_feedback`, `search_history`, `filter_history`, `save_data`/`load_data`, `load_word_bank`, `is_valid_guess`) — ส่วนใหญ่มีแล้วจาก Sprint 1-3 (72 เคส) งานที่เหลือคือวัด coverage
- ตั้งค่า GitHub Actions workflow: รัน Linting + Unit Test อัตโนมัติทุกครั้งที่ push/PR
- เพิ่มฟีเจอร์ AI หรือ Automation Agent เช่น วิเคราะห์สถิติการเล่น หรือแนะนำคำใบ้อัตโนมัติ
- สรุปอุปสรรคที่พบตลอด Sprint 1-3 และแนวทาง Refactor
- **Packaging ให้รันได้ทั่วเครื่อง (global install):** ทำให้เรียกเกมด้วยคำสั่ง `wordle` จาก terminal ไดเรกทอรีไหนก็ได้ ไม่ต้อง `cd` เข้า repo หรือพิมพ์ `python game.py`
  - path ของ `history.json` / `answers.txt` / `valid_words.txt` อิงจาก `Path(__file__)` แล้ว (ทำใน Sprint 3) — เหลือตรวจตอนติดตั้งแบบ package จริง และเพิ่ม `package-data` สำหรับไฟล์ `data/`
  - เพิ่ม `pyproject.toml` พร้อม `[project.scripts]` ให้ `wordle = "src.cli:main"` เป็น entry point
  - เพิ่มคำสั่งย่อย `wordle start` (ด้วย `argparse`) ให้เริ่มเกมทันทีโดยไม่ต้องผ่าน banner/เมนู

## 3. งานที่ต้องส่งมอบ
| งาน | รายละเอียด |
|---|---|
| `tests/test_logic.py` | Unit test ด้วย `unittest` หรือ `pytest` |
| `.github/workflows/ci.yml` | Workflow รัน lint (เช่น `flake8`) + test อัตโนมัติ |
| ฟีเจอร์ AI/Automation | เช่น สรุปสถิติคำที่ทายบ่อย หรือ agent ช่วยวิเคราะห์ผล |
| `pyproject.toml` | Package metadata + `[project.scripts]` entry point (`wordle`) + `package-data` สำหรับไฟล์ word list |
| `wordle start` subcommand | `argparse` sub-command เริ่มเกมทันที ข้าม banner/เมนู |
| เอกสารสรุป Refactor | เปรียบเทียบทางเลือกโครงสร้างข้อมูล/สถาปัตยกรรมที่ใช้จริงกับทางเลือกอื่น (รวมกรณี validate คำผ่าน API ต่อคำทาย (3-10 วินาที, ต้องใช้ network) vs local set ใน Sprint 3) และตัวเลือก class extraction ที่ยังไม่ทำ: `HistoryRepository`, `GameSession`, `ConsoleUI` |

## 4. Definition of Done (DoD)
- [ ] Unit test ครอบคลุมฟังก์ชันหลักของ Business/Data Layer อย่างน้อย 80% ของเคสสำคัญ (ปกติ + edge case)
- [ ] CI pipeline รันผ่านอัตโนมัติเมื่อเปิด PR และ block การ merge ถ้า test ไม่ผ่าน
- [ ] ฟีเจอร์ AI ทำงานได้จริงและสาธิตได้ใน Live Demo
- [ ] มีเอกสารสรุปปัญหาเทคนิคที่พบใน Sprint 1-3 พร้อมวิธีแก้ไข
- [ ] รันคำสั่ง `wordle` ได้จากไดเรกทอรีใดก็ได้หลัง `pip install` (path ของไฟล์ข้อมูลไม่ผูกกับ CWD)
- [ ] `wordle start` เริ่มเกมได้ทันทีโดยไม่แสดง banner/เมนู ส่วน `wordle` เปล่ายังทำงานเหมือนเดิม

## 5. สิ่งที่ต้องเตรียมนำเสนอ (5 ส่วนตาม Rubric)
1. ปัญหา สถาปัตยกรรม และ UML Class Diagram
2. Tech stack, เวอร์ชัน Python, ไลบรารี, Design Pattern ที่ใช้
3. Live Demo ครบทุกฟังก์ชัน + Algorithm (search/filter/sort) + ทดสอบ error
4. สรุปปัญหาเทคนิคที่พบ + การเปรียบเทียบทางเลือก
5. สาธิต CI/CD บน GitHub Actions + ฟีเจอร์ AI + คำสั่ง `wordle` / `wordle start` แบบ global + แนวทางต่อยอด

## 6. Deliverable
- Repository พร้อม CI/CD ที่ทำงานจริง
- โค้ด, เอกสาร, รายงานทั้งหมดของโปรเจกต์ (final artifacts)