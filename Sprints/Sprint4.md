# Sprint 4: Sprint Final — CI/CD, Packaging, Global CLI, and Daily Word Mode

## 1. สถานะปัจจุบัน

Sprint 4 ยังดำเนินอยู่ โดยส่วนที่ยืนยันผลแล้วประกอบด้วย global CLI command, installable package, daily API-driven secret word, และ CI/test/lint tooling ในเครื่อง

Workflow `.github/workflows/ci.yml` ตั้งให้รันเมื่อ push และ pull request บน Python 3.12/3.13 ทั้ง Ubuntu และ Windows โดยติดตั้ง `.[dev]`, รัน Flake8 และทดสอบพร้อม coverage gate 80% ชุดทดสอบใช้ temporary history paths และ API requests ถูก mock ไว้

การตรวจสอบล่าสุดในเครื่อง Windows/Python 3.13.14: **93 tests passed, 93.46% coverage**, และ Flake8 ผ่านทั้งหมด ยังไม่มีหลักฐานการรัน workflow บน GitHub Actions; branch protection และ PR demo ที่จงใจทำให้ check fail ยังเป็นงาน manual

งานที่ถือว่าเสร็จแล้วในเวอร์ชันปัจจุบัน:
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
- [x] Packaging and installable entry point
- [x] Local word list and external history path
- [x] Full test verification: 93 passed, 93.46% coverage; Flake8 clean
- [x] Regression coverage for CLI behavior
- [x] GitHub Actions workflow configured for push/PR and Python 3.12/3.13 on Ubuntu/Windows
- [x] CI status badge added to README
- [ ] Verify successful GitHub Actions run for the matrix
- [ ] Enable `main` branch protection requiring CI
- [ ] Demonstrate a failing CI check on a PR and capture evidence

---

# การประเมินตนเองแยกตามบทบาท (Role-Based Grading Rubrics)

## Sprint 4 — Sprint Final

**บทบาท:** Planner, Coder, Debugger/QA

### การประเมินบทบาท Planner (นักวางแผนและสถาปนิก)

| เกณฑ์การประเมิน | สมาชิก 1 | สมาชิก 2 | สมาชิก 3 | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การวางแผนและจัดลำดับ workstreams | | | | |
| การกำหนดขอบเขตและ Definition of Done | | | | |
| การเลือกโซลูชันสำหรับ daily API mode และ packaging | | | | |
| **รวมคะแนนบุคคล** | | | | **/10** |

### การประเมินบทบาท Coder (นักเขียนโค้ด)

| เกณฑ์การประเมิน | สมาชิก 1 (Self) | สมาชิก 2 | สมาชิก 3 | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การทำงานตาม architecture และ boundaries | | | | |
| ความถูกต้องของ CLI และ daily-game logic | | | | |
| มาตรฐานและอ่านง่ายของโค้ด | | | | |
| **รวมคะแนนบุคคล** | | | | **/10** |

### การประเมินบทบาท Debugger / QA (นักทดสอบและประกันคุณภาพ)

| เกณฑ์การประเมิน | สมาชิก 1 | สมาชิก 2 (Self) | สมาชิก 3 | สรุปคะแนน (0–10) |
| --- | :---: | :---: | :---: | :---: |
| การทดสอบ behavior และ edge cases | | | | |
| การตรวจสอบ install/runtime และ fallback | | | | |
| การรายงานผลและหลักฐานการยืนยัน | | | | |
| **รวมคะแนนบุคคล** | | | | **/10** |
