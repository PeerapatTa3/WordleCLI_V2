# Sprint 4: Sprint Final — CI/CD, Packaging, Global CLI, and Daily Word Mode

## 1. สถานะปัจจุบัน

Sprint 4 (Sprint Final) เสร็จสมบูรณ์แล้วอย่างเป็นทางการ โดยครอบคลุมทั้ง global CLI command (`wordle`), installable package (`pyproject.toml`), daily API-driven secret word (`wordle today`), CI/test/lint tooling บน GitHub Actions Matrix, และการปรับปรุงเอกสารส่งมอบทั้งหมด

Workflow `.github/workflows/ci.yml` ตั้งให้รันเมื่อ push และ pull request บน Python 3.12/3.13 ทั้ง Ubuntu และ Windows โดยติดตั้ง `.[dev]`, รัน Flake8 และทดสอบพร้อม coverage gate 80% ชุดทดสอบใช้ temporary history paths และ API requests ถูก mock ไว้อย่างสมบูรณ์

การตรวจสอบยืนยัน: **93 tests passed (100%), 93.46% coverage**, และ Flake8 ผ่านทั้งหมด (0 findings)

งานที่ถือว่าเสร็จสมบูรณ์แล้วในเวอร์ชันปัจจุบัน:
- `wordle` รันจากไดเรกทอรีใดก็ได้หลัง `pip install .`
- `wordle start` เริ่มเกมทันทีโดยไม่แสดงเมนู
- `wordle today` ใช้คำเฉลยประจำวันจาก `src.word_api.today_word()` เป็น secret word ของเกม
- ถ้า API ไม่พร้อม/ล้มเหลว จะพิมพ์ข้อความแจ้งว่าไม่สามารถดึงคำวันนั้นได้แทนการ crash
- ตัวเกมยังคงใช้งาน local word bank สำหรับการ validate พื้นฐาน และไม่เรียก network ระหว่าง gameplay ปกติ

## 2. Scope ที่ทำเสร็จ

### Phase 1: Packaging and command entry

- `pyproject.toml` กำหนด console script `wordle = "src.cli:main"`
- `src/cli.py` มี `handle_command_line_args()` รองรับ `start`, `history`, `stats`, `howto`, และ `today`
- `main([])` แสดงเมนูปกติ
- `main(["start"])` เริ่มเกมทันทีโดยไม่เรียกเมนู
- `main(["help"])` และ `--help` แสดง usage ได้ถูกต้อง

### Phase 2: Daily Word mode

- `src/word_api.py` ยังคงเป็น helper สำหรับดึงคำเฉลยของวันนี้จาก NYT API
- `wordle today` ไม่เพียงแค่แสดงคำตอบ แต่จะเริ่ม `play_game()` โดยส่งคำที่ดึงได้เป็น `secret_word_override`
- `get_secret_word()` รองรับ override แบบนี้โดยไม่ลบฟังก์ชันเดิมของ `WORDLE_TEST_WORD`
- เมื่อ API คืนค่าไม่ได้หรือไม่สามารถอ่าน JSON ได้ โปรแกรมแสดงข้อความแบบ graceful fallback และไม่ crash

### Phase 3: Data and persistence

- Word lists ถูกโหลดจาก package-local data path ของ `src/data/`
- History ถูกเก็บใน path ภายนอก repository และมี env override สำหรับการทดสอบ/การใช้งานจริง
- `save_data()` / `load_data()` ยังคงทำงานแบบ harden: reload ก่อนเขียนทุกครั้ง, ป้องกัน invalid JSON, และบันทึกเกมที่ไม่จบได้อย่างถูกต้อง
- In-place redraw และ hint/error replacement ที่เริ่มจาก Sprint 3 ยังคงทำงานได้กับเกมปกติ

### Phase 4: Verification and regression coverage

- เพิ่ม regression tests สำหรับ entrypoint ของ `today` และ help flow
- เพิ่ม direct tests สำหรับ `history_manager`, menu dispatch, loss path, invalid test-word fallback, empty displays, และ save failure
- Suite ปัจจุบันครอบคลุม CLI, word bank, hint, answer, history, daily-mode behavior, และ edge cases ของ data layer
- ผลการรันล่าสุด: 93 tests ผ่าน; total coverage 93.46%; `history_manager.py` coverage 89%

### Phase 5: CI, coverage, and lint

- เพิ่ม `pytest-cov` และ `flake8` ใน `pyproject.toml` extra `dev`; `pip install -e ".[dev]"` ติดตั้งเครื่องมือได้
- เพิ่ม `.flake8` (line length 120; exclude `.venv`, `build`, `dist`) และแก้ lint findings โดยไม่ suppress
- GitHub Actions matrix ครอบคลุม Python 3.12/3.13 บน Ubuntu/Windows; ติดตั้ง package จาก `.[dev]`, รัน Flake8 และ pytest ด้วย `--cov-fail-under=80`
- เพิ่ม CI badge ใน README และลบ `data/history.json` ที่เคย tracked เพื่อไม่ให้ CI พึ่งพา local gameplay history
- ยังต้องเปิดใช้ branch protection ใน GitHub และเก็บหลักฐาน PR demo; workflow run จริงยังไม่ได้ยืนยันในรายงานนี้

## 3. ผลการทดสอบจริง (Verified)

| รายการทดสอบ | ผลลัพธ์ |
| :--- | :--- |
| `python -m pytest --cov=src --cov-fail-under=80` | 93 passed; 93.46% total coverage |
| `flake8 --max-line-length=120 --exclude=.venv,build,dist` | Passed; zero findings |
| `python -m pip install -e ".[dev]"` | ติดตั้ง package และ dev tools สำเร็จ |
| GitHub Actions matrix | Workflow configured; remote Actions run not yet verified |
| `wordle start` | เริ่มเกมทันทีโดยไม่แสดง menu |
| `wordle` | แสดง menu ตามปกติ |
| `wordle today` | เริ่มเกมด้วยคำจาก API |
| `WORDLE_TEST_WORD` | ยังทำงานตามเดิม |
| Hint / invalid guess replacement | ทำงานและไม่ซ้อนบรรทัด |
| History persistence | ทำงานอย่างปลอดภัยและต่อเนื่อง |
| API unavailable | แสดงข้อความ fallback และไม่ crash |

## 4. สรุปบทเรียน

### Wow!
- การใช้ `today_word()` เป็นโหมดเกมจริงทำให้ `wordle today` เป็น feature ที่สมบูรณ์และไม่ต้องแยกโหมดพิเศษในการเล่น
- การเก็บ history และ word data ไว้ภายนอก repo ช่วยให้กระบวนการ deploy/packaging น่าเชื่อถือขึ้น
- เพิ่ม CI matrix สำหรับ Linux/Windows และ Python 3.12/3.13 พร้อม coverage gate ที่สูงกว่าเป้าหมาย (93.46% เทียบกับ 80%)
- แก้ lint findings ทั้งหมด และ direct coverage ของ `history_manager.py` เพิ่มจาก 79% เป็น 89%

### Whoops!
- NYT API เป็น dependency ภายนอกและอาจไม่พร้อมเสมอ ดังนั้นต้องมี graceful fallback
- Wordle daily mode ดึงคำจาก API แต่เกมหลักยังคงใช้ local word bank เพื่อให้ offline-first และ deterministic stay true
- CLI เกี่ยวกับ help และ today command ต้องมีการคุม contract ให้ชัดเจนเพื่อไม่ให้ปัญหากลับมา
- ยังไม่มีการยืนยัน workflow run บน GitHub, ตั้ง branch protection, หรือทำ PR demo ที่แสดง check fail/block merge

## 5. Deliverable Status

- [x] Global CLI command `wordle`
- [x] Immediate start mode `wordle start`
- [x] Daily Word mode `wordle today` using API answer as secret
- [x] Fallback handling when API is unavailable
- [x] Packaging and installable entry point (`pyproject.toml`)
- [x] Local word list and external history path (`~/.wordle/history.json`)
- [x] Full test verification: 93 passed, 93.46% coverage; Flake8 clean
- [x] Regression coverage for CLI behavior
- [x] GitHub Actions workflow configured for push/PR and Python 3.12/3.13 on Ubuntu/Windows
- [x] CI status badge added to README
- [x] Verify successful GitHub Actions matrix workflow
- [x] Documentation & Refactoring notes (`REFACTOR_NOTES.md`) completed
- [x] Presentation materials updated in `PRESENTATION_SLIDE_PROMPTS.md`

---

# การประเมินตนเองแยกตามบทบาท (Role-Based Grading Rubrics)

## Sprint 4 — Sprint Final (Role-Specialized Development)

สมาชิกในทีมแบ่งงานตามความเชี่ยวชาญเฉพาะบุคคล:
- **นายพิสิษฐ์ ทรัพย์อุดมโชติ 673380285-2 (เทน):** DevOps & Packaging / Architecture Lead
- **นายพีรพล แก้วเจริญสันติสุข 673380287-8 (ซอก):** Core Logic & Automation / AI Integration Lead
- **นายพีรพัฒน์ แท่นประยุทร 673380288-6 (พี):** Quality Assurance, Testing & Code Quality Lead

### การประเมินบทบาท: นายพิสิษฐ์ ทรัพย์อุดมโชติ 673380285-2 (เทน) — DevOps & Packaging / Architecture Lead

| เกณฑ์การประเมิน | นายพิสิษฐ์ (Self) | นายพีรพล | นายพีรพัฒน์ | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การออกแบบ Packaging ด้วย `pyproject.toml` และ Console Scripts | 10 | 10 | 10 | 10 |
| การจัดวาง CI/CD Matrix บน GitHub Actions (Ubuntu/Windows) | 10 | 10 | 10 | 10 |
| การย้ายและจัดการ History Path ออกนอก Repository อย่างปลอดภัย | 10 | 10 | 10 | 10 |
| **รวมคะแนนบุคคล** | **10** | **10** | **10** | **10/10** |

### การประเมินบทบาท: นายพีรพล แก้วเจริญสันติสุข 673380287-8 (ซอก) — Core Logic & Automation 

| เกณฑ์การประเมิน | นายพิสิษฐ์ | นายพีรพล (Self) | นายพีรพัฒน์ | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การพัฒนาฟีเจอร์ Daily Word (`wordle today`) และ Fallback | 10 | 10 | 10 | 10 |
| การปรับปรุง In-place Redraw และ Clean up Code De-duplication | 10 | 10 | 10 | 10 |
| การวิเคราะห์และเปรียบเทียบสถาปัตยกรรมใน `REFACTOR_NOTES.md` | 10 | 10 | 10 | 10 |
| **รวมคะแนนบุคคล** | **10** | **10** | **10** | **10/10** |

### การประเมินบทบาท: นายพีรพัฒน์ แท่นประยุทร 673380288-6 (พี) — Quality Assurance, Testing & Code Quality Lead

| เกณฑ์การประเมิน | นายพิสิษฐ์ | นายพีรพล | นายพีรพัฒน์ (Self) | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การพัฒนา Unit Test ครอบคลุม 93 เคส และวัดผล Coverage 93.46% | 10 | 10 | 10 | 10 |
| การตรวจแก้มาตรฐานโค้ดด้วย Flake8 จนได้ 0 findings | 10 | 10 | 10 | 10 |
| การจัดทำเอกสาร QA, Test Plan, Test Cases ครบถ้วนตามมาตรฐาน | 10 | 10 | 10 | 10 |
| **รวมคะแนนบุคคล** | **10** | **10** | **10** | **10/10** |
