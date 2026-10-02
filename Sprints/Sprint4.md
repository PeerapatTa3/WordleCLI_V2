# Sprint 4: Sprint Final — Packaging, Global CLI, and Daily Word Mode

## 1. สถานะปัจจุบัน

Sprint 4 ได้บรรลุส่วนสำคัญของโครงการที่มีผลลัพธ์ตรวจสอบแล้ว: global CLI command, installable package, daily API-driven secret word, และการรันเกมแบบจริงโดยใช้คำตอบประจำวันจาก NYT endpoint

การจัดระเบียบชุดทดสอบยังคงดำเนินต่อ: โครงสร้างการทดสอบที่เคยรวมไว้ใน `tests/test_sprint3.py` ถูกย้ายเข้าไฟล์ที่เกี่ยวข้องตามความเหมาะสม (`tests/test_cli.py` และ `tests/test_entrypoint.py`) แล้วลบไฟล์เดิมออก เพื่อให้โครงสร้างชุดทดสอบสอดคล้องกับการใช้งานจริงของโปรเจกต์

การตรวจสอบล่าสุด: `python -m pytest -q` → **82 passed in 1.13s**

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
- Suite ปัจจุบันครอบคลุม CLI, word bank, hint, answer, history, and daily-mode behavior
- ผลการรายงานจากการรันจริง: 82 tests ผ่านทั้งหมด

## 3. ผลการทดสอบจริง (Verified)

| รายการทดสอบ | ผลลัพธ์ |
| :--- | :--- |
| `python -m pytest -q` | 82 passed |
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
- การรัน full suite ผ่านโดยมีหลักฐานชัดเจน แสดงว่าการเปลี่ยนแปลงล่าสุดยังคงสอดคล้องกับระบบเดิม

### Whoops!
- NYT API เป็น dependency ภายนอกและอาจไม่พร้อมเสมอ ดังนั้นต้องมี graceful fallback
- Wordle daily mode ดึงคำจาก API แต่เกมหลักยังคงใช้ local word bank เพื่อให้ offline-first และ deterministic stay true
- CLI เกี่ยวกับ help และ today command ต้องมีการคุม contract ให้ชัดเจนเพื่อไม่ให้ปัญหากลับมา

## 5. Deliverable Status

- [x] Global CLI command `wordle`
- [x] Immediate start mode `wordle start`
- [x] Daily Word mode `wordle today` using API answer as secret
- [x] Fallback handling when API is unavailable
- [x] Packaging and installable entry point
- [x] Local word list and external history path
- [x] Full test verification with real pytest run
- [x] Regression coverage for CLI behavior

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
