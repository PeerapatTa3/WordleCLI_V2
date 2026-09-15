# QA Report — Sprint 1-3 Integration

**Project:** Wordle CLI V.2  
**Sprint:** 1  
**Week:** 12  
**Members:** เทน (Planner), ซอก (Coder), พี (Debugger)

---

## 1. Sprint Progress Summary

- [x] Defined CLI scope and Definition of Done in PLAN.md
- [x] Implemented welcome banner and main menu
- [x] Completed input validation for menu and guess handling
- [x] Added core game logic for Wordle feedback calculation
- [x] Added JSON-based history persistence and read-only word pool loading
- [x] Added colorized feedback output using `colorama`
- [x] Added fallback word fetching from public API through `src/word_api.py`
- [x] Added unit tests for logic and CLI validation
- [x] Added deterministic tests for API success, invalid responses, network failure, and duplicate removal
- [x] Added edge-case tests for duplicate letters and corrupted JSON
- [x] Restored and tested Statistics and How to Play menu features from the legacy project
- [x] Restored word-pool validation so unknown words are rejected
- [x] Added and tested in-game hint and answer commands
- [x] Added validation against the complete filtered API word list with local fallback
- [x] Added exact-word API fallback for meaningful words omitted from the top list
- [x] Kept common words available through local fallback during Dictionary API timeout
- [x] Verified Python-based CLI flow works without crashing

---

## 2. Bug/Validation Report

| Test Case | Observation | Expected | Actual | Status |
|---|---|---|---|---|
| Select menu `0` | User enters invalid menu option | Program shows warning and loops again | Program shows invalid option message and continues | PASS |
| Select menu `abc` | User enters non-numeric text | Program rejects input and asks again | Program rejects input and continues | PASS |
| Guess with short word | User enters `APP` | System rejects as invalid length | Invalid guess message shown | PASS |
| Guess with numbers | User enters `APP1E` | System rejects because not alphabetic | Invalid guess message shown | PASS |
| Guess with spaces | User enters `APP LE` | System rejects because not alphabetic | Invalid guess message shown | PASS |
| Mixed case input | User enters `play` or `PLAY` | All variants should behave the same | Menu input is normalized with `.lower()` | PASS |
| Valid 5-letter word | User enters `APPLE` | Accept and continue | Input accepted and returned uppercase | PASS |
| Duplicate letters | Guess `ALLEY` against `APPLE` | Only available matching letters receive yellow feedback | Feedback is `['✓', '-', 'x', '-', 'x']` | PASS |
| Corrupted history file | JSON cannot be decoded | Loader returns an empty list without crashing | `load_data()` returns `[]` | PASS |
| API network failure | API request raises an exception | Word fetch returns `None` safely | `fetch_random_word()` returns `None` | PASS |
| Duplicate API words | API returns the same word more than once | Word pool contains unique words | `fetch_word_pool()` removes duplicates | PASS |
| Statistics | Saved history contains multiple games | Show win rate, streak, and guess distribution | Statistics summary is displayed correctly | PASS |
| How to Play | User selects the help menu | Explain rules and feedback markers | Help text is displayed | PASS |
| Unknown word | User enters a 5-letter word outside the pool | Reject the guess and ask again | Unknown word is rejected | PASS |
| Hint command | User enters `hint` during a round | Reveal one letter without consuming an attempt | One letter is shown | PASS |
| Answer command | User enters `answer` during a round | Reveal the secret and end the round | Secret word is displayed | PASS |
| Dictionary word | Dictionary API returns a definition for `HELLO` | Accept the meaningful word | `HELLO` is accepted | PASS |
| Unknown dictionary word | Dictionary API returns no entry for `QZXJK` | Reject when no definition exists | Unknown word is rejected | PASS |
| Local fallback words | Dictionary API is unavailable | Accept known local words | `HELLO` and `WORLD` are accepted | PASS |
| Local fallback word | Dictionary API is unavailable | Accept known word `ELECT` | `ELECT` is accepted | PASS |
| Invalid spelling/length | User enters `POFIT` or `PROFIT` | Reject unknown or non-five-letter input | Invalid input is rejected | PASS |

---

## 3. Retrospective

### Wow!
- ระบบ CLI แยกฟังก์ชันได้ชัดเจนตาม Single Responsibility
- การ normalize input ด้วย `.strip()` และ `.lower()` ทำให้ผู้ใช้พิมพ์ผิดแบบเล็ก/ใหญ่หรือมีช่องว่างนำหน้า/ตามหลังยังทำงานได้
- มี automated test ครอบคลุมความผิดพลาดหลักได้อย่างเหมาะสม

### Whoops!
- ในช่วงแรกยังมีความสับสนเรื่องการจัดโครงสร้างไฟล์และ README
- ได้แก้ไขด้วยการใช้ [PLAN.md](./PLAN.md) เป็นแผนงานหลักและจัดโครงสร้างโปรเจกต์ให้ชัดเจนตาม Sprint

---

## 4. Delivery Status

**Status:** Sprint 1-3 core features completed; Sprint Final CI/CD and AI integration remain.

**Pull Request Summary:**
- Feature: CLI menu, validation, game loop, feedback scoring, JSON persistence, statistics, hints, answer reveal, and meaningful-word API fallback
- Testing: `pytest` executed successfully
- Evidence: `33 passed`

**PR Link:** To be filled when repository PR is created.

## 5. Test Plan and Sprint Test Cases

รายละเอียด Test Plan, Test Cases และ Edge Cases แยกตาม Sprint อยู่ที่ [TEST_PLAN.md](./TEST_PLAN.md)
ตาราง Test Cases แบบ Quality Assurance Matrix อยู่ที่ [TEST_CASES.md](./TEST_CASES.md)
