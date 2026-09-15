# QA Report — Sprint 1: Front-End App Dev

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
- [x] Added JSON-based history and word pool persistence
- [x] Added colorized feedback output using `colorama`
- [x] Added fallback word fetching from public API through `src/word_api.py`
- [x] Added unit tests for logic and CLI validation
- [x] Added deterministic tests for API success, invalid responses, network failure, and duplicate removal
- [x] Added edge-case tests for duplicate letters and corrupted JSON
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

**Status:** Sprint 1 and Sprint 2 core features completed; Sprint 3 integration is the next milestone.

**Pull Request Summary:**
- Feature: CLI menu, validation, game loop, feedback scoring, JSON persistence, word-pool management, and API fallback
- Testing: `pytest` executed successfully
- Evidence: `13 passed in 0.04s`
- Updated evidence: `20 passed in 0.19s`

**PR Link:** To be filled when repository PR is created.
