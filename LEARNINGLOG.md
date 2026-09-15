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
  ออกแบบ main() สำหรับเกม Wordle ให้มีเมนู 1-4, เลือกเล่น / ดูประวัติ / ลบคำ / ออกจากเกม พร้อมการแสดงข้อความแจ้งเตือนเมื่ออินพุตผิด
  ```
- **AI Response Summary:**
  ควรใช้ `while True` สำหรับลูปหลัก, ใช้ `if/elif/else` สำหรับเมนู, และแยกฟังก์ชันสาขาให้อยู่คนละส่วน เพื่อให้โปรแกรมไม่พังเมื่อกรอกค่าผิด
- **Live Verification Code:**
  ```python
  def main():
      while True:
          choice = input("Choose an option (1-4): ").strip().lower()
          if choice == "1":
              print("Play Wordle")
          elif choice == "2":
              print("View history")
          elif choice == "3":
              print("Remove word")
          elif choice == "4":
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
- เพิ่ม automated test จาก 13 เป็น 21 เคส และครอบคลุม business logic, persistence และ API fallback มากขึ้น

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
