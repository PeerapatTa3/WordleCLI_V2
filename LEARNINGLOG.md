# 📓 Learning Log & Responsible AI Prompt Record (Wordle CLI V.2)

**Project Title:** Wordle CLI V.2 — Final Project in Script Programming
**Team Members & Roles:**
- 👩‍💻 **เทน:** Planner / PM
- 👨‍💻 **ซอก:** Coder / Developer
- 👨‍💻 **พี:** Debugger / QA

---

## 1. Context & Educational Rationale

เพื่อปฏิบัติตามหลักการของการพัฒนาซอฟต์แวร์เชิงวัตถุและการออกแบบแบบแยกชั้น (Separation of Concerns) เอกสารฉบับนี้จึงเก็บข้อมูลเชิงทฤษฎี ปัญหาและแนวทางการแก้ปัญหา รวมถึงคำถามที่ใช้ร่วมกับ AI เพื่อช่วยวิเคราะห์และออกแบบโปรเจกต์ Wordle CLI ให้มีโครงสร้างที่ชัดเจนและทนต่อข้อผิดพลาดได้ดี

---

## 2. Records of AI Prompts & Responses

### 🔹 Prompt 1: Designing the CLI Menu and Input Validation
- **Student Prompt:**
  ```text
  เขียนโปรแกรม Wordle CLI ใน Python โดยมีฟังก์ชัน display_welcome_message(), display_menu(), get_menu_choice(), is_valid_guess(), get_guess_input() และ main() ให้แยกหน้าที่ชัดเจนและตรวจสอบอินพุตอย่างปลอดภัย
  ```
- **AI Response Summary:**
  แนะนำให้แยกฟังก์ชันตามหน้าที่แต่ละอย่าง เช่น การแสดงข้อความ, การแสดงเมนู, การคัดกรองอินพุต, และการทำ while loop หลักอย่างชัดเจน รวมถึงการใช้ `.strip()` และ `.lower()` เพื่อ normalize input
- **Live Verification Code:**
  ```python
  from cli import get_menu_choice, is_valid_guess, get_guess_input

  print(get_menu_choice())
  print(is_valid_guess("APPLE", 5))
  print(get_guess_input(5))
  ```

---

### 🔹 Prompt 2: Validating Guess Input and Defensive Handling
- **Student Prompt:**
  ```text
  อธิบายวิธีตรวจสอบคำทาย Wordle ที่ผิดพลาด เช่น ความยาวไม่ตรง 5 ตัว, มีตัวเลข, มีช่องว่าง, มีสัญลักษณ์ และพิมพ์เล็ก/ใหญ่ผสมกัน
  ```
- **AI Response Summary:**
  ใช้ `len()` ตรวจความยาว, `isalpha()` ตรวจว่าเป็นตัวอักษรล้วน, และ `strip()` ลบช่องว่างก่อนประเมิน นอกจากนี้ควรป้องกันค่า `None` และคืนค่า `False` สำหรับกรณีที่ไม่ผ่านเงื่อนไข
- **Live Verification Code:**
  ```python
  def is_valid_guess(guess, word_length):
      if guess is None:
          return False
      normalized = guess.strip()
      if len(normalized) != word_length:
          return False
      if not normalized.isalpha():
          return False
      return True

  print(is_valid_guess("APPLE", 5))
  print(is_valid_guess("APP 1E", 5))
  print(is_valid_guess("app", 5))
  ```

---

### 🔹 Prompt 3: Designing a Clean CLI Loop
- **Student Prompt:**
  ```text
  ออกแบบ main() สำหรับเกม Wordle ให้มีเมนูเล่น / ดูประวัติ / ดูสถิติ / วิธีเล่น / ออกจากเกม พร้อมการแสดงข้อความแจ้งเตือนเมื่ออินพุตผิด
  ```
- **AI Response Summary:**
  ควรใช้ `while True` สำหรับลูปหลัก, ใช้ `if/elif/else` สำหรับเมนู, และแยกฟังก์ชันสาขาให้อยู่คนละส่วน เพื่อให้โปรแกรมไม่พังเมื่อกรอกค่าผิด
- **Live Verification Code:**
  ```python
  def main():
      while True:
          choice = input("Choose an option (1-5): ").strip().lower()
          if choice == "1":
              print("Play Wordle")
          elif choice == "2":
              print("View history")
          elif choice == "3":
                print("View statistics")
              elif choice == "4":
                print("How to play")
              elif choice == "5":
              print("Goodbye!")
              break
          else:
              print("Invalid option")
  ```

---

### 🔹 Prompt 4: Preparing the Project for Future Sprint 2 and 3
- **Student Prompt:**
  ```text
  อธิบายแนวทางต่อยอดจาก Sprint 1 ไปสู่ Sprint 2 และ Sprint 3 สำหรับ Wordle CLI โดยมี Business Logic, Data Access, Search/Filter, JSON persistence และ Integration
  ```
- **AI Response Summary:**
  ควรแยกชั้นเป็น Presentation, Business Logic, Data Access อย่างชัดเจน โดยให้ `main()` เรียกใช้แอปพลิเคชันผ่าน interface เดียว และเก็บ state ของเกมอย่างสอดคล้องกันตลอดการเล่น
- **Live Verification Code:**
  ```python
  class WordleGame:
      def __init__(self, secret_word, word_length=5):
          self.secret_word = secret_word.upper()
          self.word_length = word_length
          self.attempts = 0

  def calculate_feedback(guess, secret_word):
      return ["✓", "-", "x"]
  ```

---

### 🔹 Prompt 5: Adding Colorized Feedback and Offline Fallback
- **Student Prompt:**
  ```text
  เพิ่มฟีเจอร์สีให้ผลลัพธ์ Wordle แบบ ✓, -, x และทำให้โปรแกรมรองรับ Windows โดยใช้ colorama พร้อม fallback เมื่อ API ดึงคำไม่ได้
  ```
- **AI Response Summary:**
  ใช้ `colorama.init(autoreset=True)` และ `Fore.GREEN`, `Fore.YELLOW`, `Fore.RED` เพื่อให้ output สีทำงานบน Windows ได้ดี ส่วนการดึงคำจาก API ให้มี fallback เป็น local word pool เพื่อไม่ให้ระบบล้มเมื่อไม่มี internet
- **Live Verification Code:**
  ```python
  from colorama import Fore, Style, init
  from src.word_api import fetch_random_word

  init(autoreset=True)
  print(Fore.GREEN + "✓" + Style.RESET_ALL)
  print(fetch_random_word(5))
  ```

---

### 🔹 Prompt 6: Building Automated Tests for Logic, Persistence, and API Fallback
- **Student Prompt:**
  ```text
  เพิ่ม pytest ให้ครอบคลุม Wordle feedback ที่มีตัวอักษรซ้ำ, การ normalize ตัวพิมพ์, corrupted JSON, API response ที่ถูกต้องหรือผิดรูปแบบ, network failure และการตัดคำซ้ำใน word pool พร้อมบันทึกผลการทดสอบลงเอกสาร
  ```
- **AI Response Summary:**
  แนะนำให้แยก test ตามความรับผิดชอบของโมดูล ใช้ `tmp_path` สำหรับไฟล์ชั่วคราว, ใช้ `monkeypatch` แทนการเรียก API จริง และสร้าง fake response เพื่อทดสอบทั้ง success path และ failure path อย่าง deterministic
- **Live Verification Code:**
  ```python
  def test_fetch_random_word_returns_none_on_request_failure(monkeypatch):
      monkeypatch.setattr("src.word_api.requests.get", raise_request_error)
      assert fetch_random_word() is None

  def test_calculate_feedback_handles_duplicate_letters():
      assert calculate_feedback("ALLEY", "APPLE") == ["✓", "-", "x", "-", "x"]
  ```
- **Test Command:**
  ```text
  python -m pytest -q
  ```
- **Verified Result:**
  ```text
  20 passed in 0.19s
  ```

---

### 🔹 Prompt 7: Restoring Legacy Statistics and How-to-Play Features
- **Student Prompt:**
  ```text
  นำฟีเจอร์ที่มีใน Wordle CLI เวอร์ชันเก่ากลับมาใส่เวอร์ชันใหม่ ได้แก่ Statistics และ How to Play โดยยังคง JSON persistence, Colorama และ API fallback ไว้
  ```
- **AI Response Summary:**
  เพิ่มเมนู Statistics สำหรับคำนวณ Games Played, Win Rate, Current Streak และ Guess Distribution จาก history รวมทั้งเพิ่มเมนู How to Play อธิบายกติกาและสัญลักษณ์ feedback โดยเพิ่ม `game_number` ให้แต่ละรอบเพื่อแยกสถิติระหว่างเกม
- **Live Verification Code:**
  ```python
  history = [
      {"correct": False, "attempt": 1, "game_number": 1},
      {"correct": True, "attempt": 3, "game_number": 1},
      {"correct": True, "attempt": 2, "game_number": 2},
  ]
  display_statistics(history)
  display_how_to_play()
  ```
- **Test Command:**
  ```text
  python -m pytest -q
  ```
- **Verified Result:**
  ```text
  22 passed
  ```

---

### 🔹 Prompt 10: Selecting Meaningful Five-Letter Words
- **Student Prompt:**
  ```text
  เปลี่ยน API ให้ดึงคำอังกฤษที่มีความหมายจำนวนมากขึ้น ไม่เอาคำสุ่มที่แปลกหรือไม่มีความหมาย และยังต้องใช้ fallback local pool ได้เมื่อ API ล้มเหลว
  ```
- **AI Response Summary:**
  เปลี่ยนไปใช้ Datamuse API แบบ `sp=?????&max=1000` ซึ่งคืนคำศัพท์พร้อมคะแนนความนิยม ระบบกรองคำ 5 ตัวอักษรและตัดคำที่มี score ต่ำกว่า `1000` ก่อนสุ่มใช้งาน
- **Live Verification Code:**
  ```python
  from src.word_api import fetch_random_word

  print(fetch_random_word())
  ```
- **Verified Result:**
  ```text
  Datamuse response accepted; full suite: 25 passed
  ```

---

### 🔹 Prompt 8: Restoring Word-Meaning Validation from the Legacy Project
- **Student Prompt:**
  ```text
  แก้ระบบตรวจคำทายให้เหมือนโปรเจกต์เก่า คือไม่รับแค่คำที่เป็นตัวอักษร 5 ตัว แต่ต้องเป็นคำที่อยู่ใน word pool ด้วย และต้องไม่ทำให้คำตอบที่มาจาก API ถูกปฏิเสธ
  ```
- **AI Response Summary:**
  เพิ่ม `valid_words` แบบ optional ให้ `is_valid_guess()` และ `get_guess_input()` เพื่อรักษา API เดิม พร้อมส่ง word pool รวมกับ secret word เข้าไปตรวจใน `play_game()` ทำให้คำที่ไม่มีในคลังถูกปฏิเสธ แต่คำตอบจาก API ยังเดาได้
- **Live Verification Code:**
  ```python
  assert is_valid_guess("HELLO", 5, {"APPLE", "GRAPE"}) is False
  assert is_valid_guess("apple", 5, {"APPLE", "GRAPE"}) is True
  ```
- **Verified Result:**
  ```text
  23 passed
  ```

---

### 🔹 Prompt 11: Adding Hint and Answer Commands
- **Student Prompt:**
  ```text
  เพิ่มฟังก์ชัน hint และ answer ระหว่างเล่นเกม โดย hint เปิดตัวอักษรทีละตำแหน่งโดยไม่เสียรอบ และ answer แสดงคำเฉลยเพื่อใช้ทดสอบ
  ```
- **AI Response Summary:**
  เพิ่มคำสั่ง `hint` และ `answer` ใน input loop แยก `display_hint()` กับ `display_answer()` ออกจาก game loop เพื่อให้ทดสอบได้ง่ายและไม่กระทบจำนวน attempt ของผู้เล่น
- **Live Verification Code:**
  ```text
  Enter a 5-letter word: hint
  Hint: Letter 1 is 'A'.
  Enter a 5-letter word: answer
  Answer: APPLE
  ```
- **Verified Result:**
  ```text
  Hint and answer tests passed; full suite: 28 passed
  ```

---

### 🔹 Prompt 12: Validating Guesses Against the Full API Word List
- **Student Prompt:**
  ```text
  ให้ระบบเช็คคำที่ผู้เล่นกรอกจากคำอังกฤษ 5 ตัวอักษรทั้งหมดที่ API ดึงมาได้ ไม่จำกัดเฉพาะคำใน local word pool และยังต้อง fallback ได้เมื่อ API ล้มเหลว
  ```
- **AI Response Summary:**
  เพิ่ม `fetch_valid_words()` เพื่อคืนรายการคำทั้งหมดที่ผ่าน length, alphabetic และ score filtering จาก Datamuse แล้วใช้รายการนี้เป็น `valid_words` ใน `play_game()` หาก API คืนค่าว่างจึง fallback ไป local word pool
- **Test Command:**
  ```text
  python -m pytest -q
  ```
- **Verified Result:**
  ```text
  29 passed
  ```

---

### 🔹 Prompt 13: Accepting Meaningful Words Outside the Top API List
- **Student Prompt:**
  ```text
  คำที่มีความหมายอย่าง HELLO ถูกปฏิเสธ เพราะไม่อยู่ในรายการ wildcard 1,000 คำ ให้ตรวจคำจริงเพิ่มเติมด้วย exact-word API โดยยังปฏิเสธคำมั่ว
  ```
- **AI Response Summary:**
  Datamuse wildcard endpoint ไม่ได้คืนคำศัพท์ทั้งหมด จึงเพิ่ม `is_valid_dictionary_word()` สำหรับตรวจคำที่ผู้เล่นกรอกกับ `dictionaryapi.dev` เมื่อคำไม่อยู่ในรายการหลัก
- **Verified Result:**
  ```text
  Dictionary API integration tests passed; unknown word rejected; full suite: 31 passed
  ```

---

### 🔹 Prompt 15: Restoring the Legacy Grouped History View
- **Student Prompt:**
  ```text
  ปรับ View History ของเวอร์ชันใหม่ให้เหมือนโปรเจกต์เก่า โดยรวมข้อมูลเป็นรายเกม แสดงสถานะ WON/LOST คำเฉลย และลำดับคำที่ทาย
  ```
- **AI Response Summary:**
  จัดกลุ่ม history ด้วย `game_number`, เพิ่ม `secret_word` ใน record ใหม่ และแสดงสรุปแต่ละเกมเป็น `Game N (STATUS, secret: WORD)` พร้อมลำดับคำทายด้วยลูกศร
- **Verified Result:**
  ```text
  Legacy grouped history test passed; full suite: 33 passed
  ```

---

### 🔹 Prompt 14: Keeping Common Words Available During API Timeout
- **Student Prompt:**
  ```text
  HELLO และ WORLD เป็นคำมีความหมายแต่ใช้ไม่ได้เมื่อ Dictionary API timeout ให้แก้โดยไม่รับคำมั่วและยังเล่นคำมาตรฐานได้
  ```
- **AI Response Summary:**
  เพิ่มคำมาตรฐานไว้ใน local read-only word pool และรวม local pool กับรายการจาก Datamuse ทุกครั้ง ทำให้ API ล่มหรือ timeout แล้วคำจริงยังใช้ได้
- **Verified Result:**
  ```text
  HELLO and WORLD accepted from local fallback; full suite: 32 passed
  ```

---

### 🔹 Prompt 9: Adding a Safe Manual Test Answer Mode
- **Student Prompt:**
  ```text
  เพิ่มวิธีทดสอบเกมแบบกำหนดคำเฉลยเองได้ เพื่อให้ทดสอบชนะหรือแพ้ได้ง่าย แต่โหมดปกติต้องยังสุ่มคำและไม่เปิดเผยคำตอบ
  ```
- **AI Response Summary:**
  เพิ่มตัวแปรสภาพแวดล้อม `WORDLE_TEST_WORD` สำหรับกำหนดคำเฉลยชั่วคราว เมื่อไม่ได้กำหนดตัวแปร ระบบยังใช้ API และ local pool ตามปกติ และจะแสดงคำเฉลยเฉพาะเมื่อเปิด test mode
- **Live Verification Code:**
  ```powershell
  $env:WORDLE_TEST_WORD="APPLE"
  python game.py
  ```
- **Verified Result:**
  ```text
  Test mode helper passed; full suite: 24 passed
  ```

---

## 3. Key Learning Outcomes

- การแบ่งชั้นของโปรแกรมช่วยลดความซับซ้อนของโค้ดและทำให้การทดสอบง่ายขึ้น
- การ normalize input ด้วย `.strip()` และ `.lower()` ช่วยลดปัญหาเรื่องตัวพิมพ์และช่องว่าง
- การตรวจสอบความถูกต้องของข้อมูลก่อนประมวลผลช่วยป้องกันข้อผิดพลาดและทำให้โปรแกรมยืนหยัดต่อ invalid input
- การทำ unit test สำหรับ edge case เป็นส่วนสำคัญของ QA และช่วยลดความเสี่ยงก่อนเขียน Sprint ถัดไป
- การใช้ `monkeypatch` ทำให้ทดสอบ network failure และ API response ได้โดยไม่พึ่งพาอินเทอร์เน็ตจริง
- การใช้ `tmp_path` ช่วยทดสอบการอ่านเขียนไฟล์โดยไม่เปลี่ยนแปลงข้อมูลจริงในโฟลเดอร์ `data/`

---

## 4. Reflection / Retrospective

### Wow!
- โค้ด CLI มีกระบวนการแยกฟังก์ชันชัดเจนและง่ายต่อการวิเคราะห์
- สามารถทดสอบ valid/invalid input ได้จริงและปรับปรุงความปลอดภัยของโปรแกรม
- เพิ่ม automated test จาก 13 เป็น 22 เคส และครอบคลุม business logic, persistence, API fallback และ legacy-compatible CLI features มากขึ้น

### Whoops!
- ในช่วงแรกยังคงมีความสับสนเรื่องโครงสร้างโมดูลและการจัดการเอกสาร README
- ได้แก้ไขโดยปรับใช้แผนงานใน [PLAN.md](./PLAN.md) และจัดทีมตามบทบาทตาม Sprint

---

## 5. Evidence of Work

- CLI implementation: [cli.py](./cli.py)
- Entry point: [game.py](./game.py)
- Game logic: [src/game_logic.py](./src/game_logic.py)
- Data manager: [src/data_manager.py](./src/data_manager.py)
- Live word API fallback: [src/word_api.py](./src/word_api.py)
- Tests: [tests/test_cli.py](./tests/test_cli.py) and [tests/test_logic.py](./tests/test_logic.py)
- API tests: [tests/test_word_api.py](./tests/test_word_api.py)
- Plan: [PLAN.md](./PLAN.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
