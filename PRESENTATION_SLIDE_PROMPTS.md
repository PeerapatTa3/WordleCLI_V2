# Presentation Slide Prompts — Wordle CLI V.2

## ส่วนที่ 1: ปัญหา สถาปัตยกรรม และการออกแบบ (20%)
- อธิบายปัญหาที่โปรเจกต์นี้แก้ไข: การทายคำศัพท์แบบ CLI ที่ต้องมีการตรวจสอบอินพุตและโครงสร้างชัดเจน
- อธิบายประโยชน์ต่อผู้ใช้: รันง่าย, ใช้งานเร็ว, ปลอดภัยกับข้อมูลที่ป้อนผิด
- นำเสนอแผนผังชั้นของโปรเจกต์: Presentation Layer / Business Logic Layer / Data Access Layer
- วาด UML class diagram แบบง่ายสำหรับ `WordleGame`, `CLI`, และ `DataManager` ในอนาคต

## ส่วนที่ 2: Stack เทคโนโลยีและมาตรฐานการพัฒนา (10%)
- ระบุ Python 3.x เป็นภาษาหลัก
- ระบุไลบรารี: `colorama`, `pytest`, `requests`
- อธิบายการใช้ Datamuse API เพื่อดึงคำอังกฤษ 5 ตัวอักษรที่มีคะแนนความนิยม พร้อม local fallback
- บอกว่าโครงสร้างโค้ดแยกตามชั้นเพื่อให้ดูเรียบร้อยและพัฒนาได้ต่อเนื่อง
- อธิบายแนวคิดการออกแบบ: Separation of Concerns, Single Responsibility, Defensive Programming

## ส่วนที่ 3: การสาธิตฟังก์ชันและการทดสอบจริง (40%)
- สาธิตการรันโปรแกรมจาก `python game.py`
- แสดงเมนูหลักและการเลือกเมนูที่ผิด เช่น 0, abc, ว่าง
- สาธิตเมนู Statistics และ How to Play
- แสดงคำทายที่ผิดพลาด เช่น สั้น, ยาว, มีตัวเลข, มีช่องว่าง
- สาธิตการปฏิเสธคำที่ไม่มีใน word pool
- สาธิตการใช้ `hint` และ `answer` ระหว่างเล่น
- อธิบาย `WORDLE_TEST_WORD` สำหรับการทดสอบด้วยคำเฉลยที่กำหนดเอง
- แสดงความสามารถของ `get_guess_input()` ที่กรอกใหม่จนกว่าจะถูกต้อง
- สาธิต logic ของการคำนวณ feedback, การบันทึก history และ JSON persistence

## ส่วนที่ 4: ปัญหาทางเทคนิค การแก้ไข และการเปรียบเทียบ (15%)
- สรุปความท้าทายหลัก เช่น การแยก Presentation จาก Business Logic
- บอกว่าใช้การ normalize input และ word-pool validation เพื่อป้องกันข้อผิดพลาด
- อธิบายการจัดการ API ล้มเหลวด้วย local word pool fallback
- เปรียบเทียบแบบการเขียนโค้ดรวมในเดียวกับแบบแยกฟังก์ชันว่าแบบไหนสะอาดและทนต่อการขยายงานมากกว่า

## ส่วนที่ 5: ระบบ DevOps, CI/CD Pipeline และแนวโน้ม AI Integration (15%)
- ระบุว่า automated tests มี 28 เคส และ CI/CD ผ่าน GitHub Actions ยังเป็นงาน Sprint Final
- นำเสนอ automation ปัจจุบัน: hint, answer mode และสรุปสถิติการเล่น
- บอกปัจจัยที่ต้องพัฒนาต่อ เช่น GitHub Actions, coverage report และ AI feature

---

## Suggested Demo Script
1. เปิด project และอธิบายวัตถุประสงค์สั้น ๆ
2. รัน `python game.py`
3. แสดงเมนู 1-5
4. ทดสอบ `0` และ `abc` ให้เห็นการป้องกัน invalid input
5. ป้อนคำทายที่ผิด เช่น `app`, `APP1E`, `HELLO WORLD`
6. สาธิต `hint` และ `answer` ระหว่างเล่น
7. เปิดดู Statistics และ History
8. สรุปว่า Sprint Final จะต่อยอดด้วย CI/CD และ AI integration

---

## Sample Q&A Prompts
- ทำไมต้องแยก Layer?
- ค่า `strip().lower()` ช่วยอะไร?
- ทำไมต้องมี unit test สำหรับ validation?
- ถ้าคำทายผิดพลาดจะจัดการอย่างไร?
- Sprint ต่อไปจะเพิ่มอะไรบ้าง?
