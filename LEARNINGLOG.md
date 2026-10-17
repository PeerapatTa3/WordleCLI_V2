# 📓 Learning Log & Responsible AI Prompt Record (Wordle CLI V.2)

**Project Title:** Wordle CLI V.2 — Final Project in Script Programming
**Team Members & Roles:**
- 👩‍💻 **นายพิสิษฐ์ ทรัพย์อุดมโชติ 673380285-2 (เทน):** Planner / PM
- 👨‍💻 **นายพีรพัฒน์ แท่นประยุทร 673380288-6 (ซอก):** Coder / Developer
- 👨‍💻 **นายพีรพล แก้วเจริญสันติสุข 673380287-8 (พี):** Debugger / QA

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
> ⚠️ *Superseded:* colorama ถูกเลิกใช้ใน Sprint 3 (ใช้ `rich` แทน) และ API fallback ถูกแทนที่ด้วย offline word bank
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

### 🔹 Prompt 8: Selecting Meaningful Five-Letter Words
> ⚠️ *Superseded in Sprint 3:* Datamuse ย้ายไป `scripts/` เป็นเครื่องมือ build-time
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

### 🔹 Prompt 10: Restoring Word-Meaning Validation from the Legacy Project
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
> ⚠️ *Superseded in Sprint 3:* ตรวจคำจาก `data/valid_words.txt` แทน API
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
> ⚠️ *Superseded in Sprint 3:* ลบ Dictionary API ออก (ช้า 3-10 วินาทีต่อคำ)
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

### 🔹 Prompt 16: Upgrading to a Rich-based Visual UI
- **Student Prompt:**
  ```text
  แก้ cli.py ปัจจุบันใน GitHub เป็นอันใหม่ที่ใช้ rich แสดงเมนู/กระดานทาย/ประวัติ/สถิติเป็น Panel และ Table พร้อม spinner ระหว่างตรวจคำ
  ```
- **AI Response Summary:**
  แทนที่ `print()`/`input()` ตรง ๆ ด้วย `rich.console.Console` (`console.print`/`console.input`) เพิ่ม `_render_wordle_board()` เพื่อวาดกระดานทายเป็น `Table` ภายใน `Panel` ที่อัปเดตทุกรอบ ใช้ `console.status()` แสดง spinner ระหว่างตรวจคำ และเปลี่ยนเมนู/ประวัติ/สถิติ/how-to-play/hint/answer ให้แสดงผลผ่าน `Panel`/`Table` แทนข้อความธรรมดา เพิ่ม `rich` ใน `requirements.txt`
- **Verified Result:**
  ```text
  `python -c "import src.cli"` imports cleanly; manual play-through renders bordered board/menus correctly.
  ตอนนั้นคาดว่าเทสต์ใน tests/test_cli.py จะพังเพราะเปลี่ยนไปใช้ rich; ตรวจซ้ำใน Sprint 3 พบว่า `console.input` เรียก `input()` ภายใน
  และ capsys ยังจับ output ได้ จึงผ่านครบ (tests/test_cli.py: 20 passed)
  ```

---

### 🔹 Sprint 3 work records (17-19)

> **ทีมต้องเติมช่อง Student Prompt ด้วย prompt จริงที่ใช้** — ส่วน AI Response Summary และ Verified Result ด้านล่างสรุปจากการเปลี่ยนแปลงใน repo และผลรัน `pytest`

### 🔹 Prompt 17: Offline-First Word Bank
- **Student Prompt:**
  ```text
  ปรับระบบ Word Bank ของเกมให้เล่นแบบ Offline ได้ โดยไม่ต้องเรียก Datamuse หรือ Dictionary API ตอนเล่นเกมและให้คำศัพท์ถูกเก็บไว้ในไฟล์ภายในโปรเจกต์ และถ้าไฟล์มีปัญหาก็ยังสามารถรันเกมได้
  จากนั้นให้ช่วยปรับ test ที่เกี่ยวข้องให้ด้วย

  ```
- **AI Response Summary:**
  เลิกเรียก Datamuse/Dictionary API ตอนเล่น เปลี่ยนเป็นไฟล์ `data/answers.txt` และ `data/valid_words.txt` โหลดผ่าน `load_word_bank()` (path จาก `Path(__file__)`, มี default pool เมื่อไฟล์หาย/ว่าง) และตรวจคำด้วย `set` lookup; ย้าย Datamuse ไป `scripts/`; เพิ่ม `scripts/build_wordlists.py`
- **Live Verification Code:**
  ```python
  from src.word_bank import load_word_bank
  answers, valid = load_word_bank(5)
  print(len(answers), len(valid), set(answers) <= set(valid))
  ```
- **Verified Result:**
  ```text
  1984 8636 True; tests/test_word_bank.py: 13 passed (รวมเทสต์ไม่เรียก network และทำงานจากทุก CWD)
  ```

---

### 🔹 Prompt 18: In-Place Redraw and Cleaner Error Handling
- **Student Prompt:**
  ```text
  ปรับหน้าจอ CLI ของเกมให้ดูสะอาดขึ้น โดยไม่ต้อง print ข้อความที่ขึ้นดันต่อกันยาวๆ ทุกครั้งที่มีการทายใหม่หน่อย และอยากให้ข้อความ error และ input เก่าถูกจัดการให้เรียบร้อย และต้องไม่ขัดกับตัว test เดิม

ช่วยเพิ่มหรือแก้ test ที่เกี่ยวข้องด้วย

  ```
- **AI Response Summary:**
  เพิ่ม `erase_lines()`, `clear_screen()`, `render_game_screen()` ให้กระดานวาดทับที่เดิม; `get_guess_input()` ลบบรรทัดที่พิมพ์และ error เดิมก่อนทายใหม่ (รวมถึง input ยาวที่ขึ้นบรรทัดใหม่); ทุกอย่างไม่ทำงานเมื่อ output ไม่ใช่ terminal; hint แสดงใต้กระดานโดยนับบรรทัดเพิ่ม
- **Verified Result:**
  ```text
  erase_lines เรียกด้วย [1, 2, 2] เมื่อผิดสองครั้งแล้วถูก; erase/clear เป็น no-op เมื่อไม่ใช่ terminal
  hint ยังคงแสดงได้ถูกต้องใต้กระดานและเทสต์ได้ปรับให้ตรวจข้อความที่ผู้เล่นเห็นแทนการเช็ค message=
  ```

---

### 🔹 Prompt 19: Refactor and State/Data Hardening
- **Student Prompt:**
  ```text
  refactor โค้ดของเกมให้เป็นระเบียบมากขึ้นหน่อย โดยแยกส่วนที่เกี่ยวกับการแสดงผลและการจัดการ history ออกจาก cli.py 
  แล้วตรวจสอบการจัดการข้อมูลและ state ต่าง ๆ ให้ปลอดภัยขึ้น และทำให้ history จัดการข้อมูลไม่ให้มีข้อมูลผิดรูปแบบหรือบันทึกข้อมูลไม่สำเร็จ
  หลังจากแก้แล้วรัน test ทั้งหมดและตรวจสอบว่ามีอะไร fail อีกหรือไม่

  ```
- **AI Response Summary:**
  แยก `BoardRenderer` และ `history_manager` ออกจาก `cli.py`; เพิ่ม `MAX_ATTEMPTS` / `WORD_LENGTH`; ลบ `colorize_feedback()`; `_persist()` โหลด history ใหม่ก่อนเขียนทุกครั้ง; `HISTORY_PATH` อิงจาก `Path(__file__)`; `load_data()` ทนไฟล์ที่ไม่ใช่ list และ record ที่ไม่ใช่ dict; `answer` ทิ้งเกมที่ไม่จบ; เตือนเมื่อบันทึกไม่สำเร็จ
- **Verified Result:**
  ```text
  tests/test_sprint3.py: 17 passed; full suite: 72 passed in 0.82s
  ```

### 🔹 Sprint 4 work records (20-22)

> **ทีมต้องเติมช่อง Student Prompt ด้วย prompt จริงที่ใช้** — ส่วน AI Response Summary และ Verified Result ด้านล่างสรุปจากการเปลี่ยนแปลงใน repo และผลรัน `pytest`

### 🔹 Prompt 20: Packaging, Console Scripts, and Global CLI Subcommands
- **Student Prompt:**
  ```text
  ช่วยตั้งค่า pyproject.toml ให้โปรเจกต์สามารถติดตั้งผ่าน pip install . และรันคำสั่ง wordle จากที่ไหนก็ได้
  พร้อมเพิ่ม subcommand เช่น wordle start ที่เริ่มเล่นเกมทันทีโดยไม่ต้องผ่านเมนูหลัก, wordle today สำหรับเล่นโหมดคำศัพท์ประจำวัน, และคำสั่ง help/stats/history
  ```
- **AI Response Summary:**
  สร้าง `pyproject.toml` โดยใช้ build-backend เป็น `hatchling` กำหนด `[project.scripts]` ให้ `wordle = "src.cli:main"` และ alias `run-app`; เพิ่ม `handle_command_line_args()` ใน `src/cli.py` เพื่อตรวจสอบและประมวลผลคำสั่งย่อย `start`, `today`, `history`, `stats`, `howto`, และ `help`; โหมด `today` ดึงคำจาก `today_word()` มาใช้เป็นคำเฉลยรอบพิเศษ และมี error handling ป้องกันโปรแกรม crash เมื่อ API ขัดข้อง
- **Live Verification Code:**
  ```powershell
  pip install .
  wordle --help
  wordle start
  wordle today
  ```
- **Verified Result:**
  ```text
  tests/test_entrypoint.py: 9 passed (ครอบคลุม start, today, history, stats, howto, help, และ unknown subcommand)
  ```

---

### 🔹 Prompt 21: CI/CD Matrix on GitHub Actions and Flake8 Linting
- **Student Prompt:**
  ```text
  ออกแบบ GitHub Actions workflow (.github/workflows/ci.yml) สำหรับรันเทสต์อัตโนมัติทุกครั้งที่ push และ pull request
  โดยให้ทดสอบทั้งบน Ubuntu และ Windows กับ Python 3.12 และ 3.13 ติดตั้ง dependencies dev, ตรวจ lint ด้วย flake8, และบังคับ coverage ไม่ต่ำกว่า 80%
  ```
- **AI Response Summary:**
  สร้าง workflow `.github/workflows/ci.yml` ด้วย strategy matrix (`os: [ubuntu-latest, windows-latest]`, `python-version: ["3.12", "3.13"]`); ใช้ `actions/setup-python@v5` พร้อม pip cache; ติดตั้งแพ็กเกจด้วย `pip install -e ".[dev]"`; รัน Flake8 ด้วย config line length 120; รัน `pytest --cov=src --cov-fail-under=80`; ลบไฟล์ `data/history.json` ออกจาก git เพื่อป้องกันไม่ให้ CI พึ่งพาประวัติการเล่นเดิม
- **Verified Result:**
  ```text
  Flake8 แก้ไขครบ 31 findings (0 findings เหลืออยู่); CI workflow รัน lint และ pytest พร้อม coverage gate 80% สำเร็จ
  ```

---

### 🔹 Prompt 22: Closing Test Coverage Gaps and Hardening Edge Cases
- **Student Prompt:**
  ```text
  ตรวจสอบ code coverage ของโปรเจกต์ Wordle CLI และเพิ่ม unit test ปิดจุดที่ยังไม่มีเทสต์คลุม เช่น การคำนวณสถิติใน history_manager เมื่อข้อมูลว่างหรือเป็น format เก่า,
  ทางเลือกเมนูหลัก 1-5, กรณีที่ทายผิดครบ 6 ครั้งจนแพ้, และกรณีบันทึกไฟล์ไม่สำเร็จ
  เพื่อให้ coverage รวมเกิน 80% ตามข้อกำหนด
  ```
- **AI Response Summary:**
  สร้าง `tests/test_history_manager.py` (3 tests) ทดสอบ empty history, legacy records ไม่มี `game_number`, และการนับ win distribution พร้อมรีเซ็ต streak เมื่อแพ้; เพิ่มเทสต์ใน `tests/test_cli.py` สำหรับ menu choices 1-5, invalid menu choice loop, 6-guess loss flow, fallback เมื่อ `WORDLE_TEST_WORD` ผิดกฎ, และ save failure; เพิ่ม coverage ของ `history_manager.py` จาก 79% เป็น 89% และ total coverage ทะลุ 93.46%
- **Verified Result:**
  ```text
  python -m pytest --cov=src --cov-fail-under=80
  93 passed in 2.57s; Total coverage: 93.46%
  ```

---

## 3. Key Learning Outcomes

- การแบ่งชั้นของโปรแกรมช่วยลดความซับซ้อนของโค้ดและทำให้การทดสอบง่ายขึ้น
- การ normalize input ด้วย `.strip()` และ `.lower()` ช่วยลดปัญหาเรื่องตัวพิมพ์และช่องว่าง
- การตรวจสอบความถูกต้องของข้อมูลก่อนประมวลผลช่วยป้องกันข้อผิดพลาดและทำให้โปรแกรมยืนหยัดต่อ invalid input
- การทำ unit test สำหรับ edge case เป็นส่วนสำคัญของ QA และช่วยลดความเสี่ยงก่อนเขียน Sprint ถัดไป
- การใช้ `monkeypatch` ทำให้ทดสอบ network failure และ API response ได้โดยไม่พึ่งพาอินเทอร์เน็ตจริง
- การใช้ `tmp_path` ช่วยทดสอบการอ่านเขียนไฟล์โดยไม่เปลี่ยนแปลงข้อมูลจริงในโฟลเดอร์ `data/`
- การพึ่งพา API ภายนอกทุกคำทายทำให้ช้าและเปราะบาง การย้ายไปใช้ข้อมูลในเครื่อง (offline-first) ทำให้เร็วและทดสอบง่ายขึ้น
- การอ่านไฟล์ประวัติใหม่ก่อนเขียนทุกครั้งช่วยไม่ให้ข้อมูลในหน่วยความจำที่เก่าไปทับไฟล์ที่ถูกแก้ระหว่างรัน
- เมื่อเปลี่ยน design ต้องอัปเดตเทสต์และเอกสารตามทันที
- การทำ Packaging ผ่าน `pyproject.toml` และ console scripts ทำให้โปรเจกต์กลายเป็นเครื่องมือ CLI ที่ติดตั้งและใช้งานได้จริงในทุกโฟลเดอร์
- การตั้งค่า CI/CD Matrix บน GitHub Actions ช่วยการันตีว่าซอฟต์แวร์ทำงานได้ข้ามระบบปฏิบัติการ (Windows & Linux) และหลายเวอร์ชันของ Python
- การบังคับ Code Quality Gates ทั้ง Lint (Flake8) และ Coverage Gate (≥80%) ช่วยป้องกัน code regression และรักษามาตรฐานของโค้ดในระยะยาว

---

## 4. Reflection / Retrospective

### Wow!
- โค้ด CLI มีกระบวนการแยกฟังก์ชันชัดเจนและง่ายต่อการวิเคราะห์
- สามารถทดสอบ valid/invalid input ได้จริงและปรับปรุงความปลอดภัยของโปรแกรม
- เพิ่ม automated test จาก 13 เคสใน Sprint 1 สู่ 72 เคสใน Sprint 3 และ **93 เคสใน Sprint 4** พร้อม Coverage **93.46%**
- (Sprint 3) เล่นได้ offline และตรวจคำทันที; กระดานและ error ไม่ซ้อนกันอีก; `cli.py` เบาลงหลังแยก `BoardRenderer` และ `history_manager`
- (Sprint 4) ติดตั้งและรันคำสั่ง `wordle` ได้ทั่วระบบ; มีโหมด `wordle start` และ `wordle today`; ระบบ CI/CD Matrix บน GitHub Actions รันผ่านฉลุยพร้อม Flake8 Clean

### Whoops!
- (Sprint 3) เปลี่ยนวิธีแสดง hint แล้วเทสต์เก่าไม่ตรง (ค้าง 1 เคส); `colorama` ยังค้างใน `requirements.txt`; เอกสารตามโค้ดไม่ทันจนต้องไล่แก้ทีเดียว
- (Sprint 4) ไฟล์ประวัติเดิม `data/history.json` ที่ถูก commit ไว้ใน repo ทำให้การทดสอบ CI เกิดผลข้างเคียง จึงต้องลบทิ้งและย้ายไปใช้ User Directory (`~/.wordle/history.json`)
- API ดึงคำประจำวันจากภายนอกอาจมี downtime จึงต้องออกแบบ graceful handling ไม่ให้โปรแกรม crash

---

## 5. Evidence of Work

- Package metadata & scripts: [pyproject.toml](./pyproject.toml), [.flake8](./.flake8)
- CI/CD workflow: [.github/workflows/ci.yml](./.github/workflows/ci.yml)
- Entry points: [game.py](./game.py), [cli.py](./cli.py)
- Presentation layer: [src/cli.py](./src/cli.py), [src/board_renderer.py](./src/board_renderer.py)
- Game logic: [src/game_logic.py](./src/game_logic.py), [src/history_manager.py](./src/history_manager.py)
- Data access & assets: [src/data_manager.py](./src/data_manager.py), [src/word_bank.py](./src/word_bank.py), [src/data/](./src/data), [src/word_api.py](./src/word_api.py)
- Build-time tools: [scripts/build_wordlists.py](./scripts/build_wordlists.py), [scripts/word_api.py](./scripts/word_api.py)
- Tests: [tests/](./tests) (93 เคส, 8 ไฟล์, Coverage 93.46%)
- Architectural & Refactoring Notes: [REFACTOR_NOTES.md](./REFACTOR_NOTES.md)
- Plan: [PLAN.md](./PLAN.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- QA: [QA_REPORT.md](./QA_REPORT.md), [Sprint4_todo.md](./Sprint4_todo.md), [Sprints/](./Sprints)