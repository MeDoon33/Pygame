# 🧪 Hướng dẫn kiểm tra tính năng import câu hỏi

## Tính năng mới được thêm vào

✅ **Hỗ trợ nhiều loại file**:
- `.txt` (Text files) - UTF-8, ASCII, Latin-1
- `.doc` (Word 97-2003) - với python-docx
- `.docx` (Word 2007+) - với python-docx

✅ **Kiểm tra xác thực file**:
1. File không được rỗng
2. File phải là file văn bản (không phải nhị phân)
3. Nội dung file phải hợp lệ và đầy đủ

✅ **Thông báo lỗi chi tiết**:
- Hiển thị emoji ✅ ❌ ⚠️ cho dễ nhận biết
- Mô tả rõ ràng nguyên nhân lỗi
- Hướng dẫn cách khắc phục

---

## 1️⃣ Kiểm tra loại file

### Test Case 1: File .txt hợp lệ
```
1. Tạo file `test_questions.txt` trong thư mục Pygame/
2. Copy nội dung từ `questions_sample.txt`
3. Chọn menu "Tạo câu hỏi từ file"
4. Chọn file `test_questions.txt`
5. Kỳ vọng: ✅ "Thành công: Tìm thấy X câu hỏi"
```

### Test Case 2: File .docx (nếu cài python-docx)
```
1. Cài đặt: pip install python-docx
2. Tạo file Word mới (.docx)
3. Paste nội dung câu hỏi
4. Lưu file
5. Import vào game
6. Kỳ vọng: ✅ "Thành công: Tìm thấy X câu hỏi"
```

### Test Case 3: File .doc (nếu cài python-docx)
```
1. Sử dụng Word cũ hoặc Save As .doc
2. Paste nội dung câu hỏi
3. Import vào game
4. Kỳ vọng: ✅ "Thành công: Tìm thấy X câu hỏi"
```

---

## 2️⃣ Kiểm tra file rỗng

### Test Case 4: File rỗng
```
1. Tạo file `empty.txt` (không có nội dung)
2. Import vào game
3. Kỳ vọng: ❌ "Lỗi: File rỗng. Vui lòng chọn file có nội dung"
```

### Test Case 5: File chỉ có khoảng trắng
```
1. Tạo file `whitespace.txt` (chỉ có spaces, newlines)
2. Import vào game
3. Kỳ vọng: ❌ "Lỗi: File không có nội dung văn bản hợp lệ"
```

---

## 3️⃣ Kiểm tra file văn bản

### Test Case 6: File nhị phân (ảnh)
```
1. Chọn file ảnh (*.png, *.jpg)
2. Import vào game
3. Kỳ vọng: ❌ "Lỗi: File không phải là file văn bản"
```

### Test Case 7: File nhị phân (Video)
```
1. Chọn file video (*.mp4, *.avi)
2. Import vào game
3. Kỳ vọng: ❌ "Lỗi: File không phải là file văn bản"
```

### Test Case 8: File .zip
```
1. Chọn file .zip
2. Import vào game
3. Kỳ vọng: ❌ "Lỗi: File không phải là file văn bản"
```

---

## 4️⃣ Kiểm tra nội dung câu hỏi

### Test Case 9: File không có câu hỏi hợp lệ
```
1. Tạo file `invalid.txt` với nội dung:
   Some random text
   Not a question
2. Import vào game
3. Kỳ vọng: ❌ "Lỗi: Không tìm thấy câu hỏi hợp lệ trong file"
```

### Test Case 10: Câu hỏi thiếu thông tin
```
1. Tạo file `incomplete.txt`:
   Câu hỏi không đầy đủ?
   Option 1
   Option 2
   (không đủ 4 option)

2. Import vào game
3. Kỳ vọng: ❌ "Lỗi: Không tìm thấy câu hỏi hợp lệ trong file"
```

### Test Case 11: File có mix valid + invalid questions
```
1. Tạo file `mixed.txt`:
   [Câu hỏi valid với đầy đủ thông tin]
   [Câu hỏi không hợp lệ]
   [Câu hỏi valid khác]

2. Import vào game
3. Kỳ vọng: ✅ "Thành công: Tìm thấy 2 câu hỏi"
            (bỏ qua câu hỏi không hợp lệ)
```

---

## 5️⃣ Kiểm tra mã hóa file

### Test Case 12: File UTF-8 với tiếng Việt
```
1. Tạo file với nội dung tiếng Việt
2. Lưu với mã hóa UTF-8
3. Import vào game
4. Kỳ vọng: ✅ "Thành công: Tìm thấy X câu hỏi"
            (hiển thị tiếng Việt đúng)
```

### Test Case 13: File Latin-1 (fallback encoding)
```
1. Tạo file với mã hóa Latin-1
2. Import vào game
3. Kỳ vọng: ✅ "Thành công: ..."
```

---

## 6️⃣ Kiểm tra hành vi người dùng

### Test Case 14: Hủy file dialog (Esc)
```
1. Chọn "Tạo câu hỏi từ file"
2. Nhấn ESC để hủy
3. Kỳ vọng: Quay lại menu, không có lỗi
```

### Test Case 15: Import lại file
```
1. Import file lần đầu tiên → ✅ Success
2. Import file khác lần thứ hai
3. Kỳ vọng: Câu hỏi cũ được thay thế bằng câu mới
```

---

## 📋 Checklist kiểm tra

- [ ] ✅ Import .txt thành công
- [ ] ✅ Import .docx thành công (nếu cài python-docx)
- [ ] ✅ Import .doc thành công (nếu cài python-docx)
- [ ] ❌ File rỗng → Lỗi đúng
- [ ] ❌ File binary → Lỗi đúng
- [ ] ❌ Không có câu hỏi valid → Lỗi đúng
- [ ] ✅ File mixed (valid + invalid) → Bỏ qua invalid
- [ ] ✅ Tiếng Việt → Hiển thị đúng
- [ ] ✅ Cancel dialog → Không lỗi

---

## 🔧 Cài đặt thêm (để hỗ trợ .docx, .doc)

```bash
# Cài đặt python-docx
pip install python-docx

# Xác nhận cài đặt thành công
python -c "from docx import Document; print('✅ python-docx installed')"
```

---

## 📝 Ghi chú phát triển

### Các hàm được thêm mới:

1. **`is_file_empty(file_path: str) -> bool`**
   - Kiểm tra file có rỗng không
   
2. **`is_text_file(file_path: str) -> bool`**
   - Kiểm tra file có phải văn bản không
   
3. **`extract_text_from_docx(file_path: str) -> str`**
   - Trích xuất text từ .docx
   
4. **`extract_text_from_doc(file_path: str) -> str`**
   - Trích xuất text từ .doc
   
5. **`read_text_content(file_path: str) -> tuple[bool, str]`**
   - Đọc nội dung file, hỗ trợ nhiều format

### Các hàm được cập nhật:

1. **`open_file_chooser()`**
   - Thêm hỗ trợ .doc, .docx
   - Cập nhật filetypes dialog
   
2. **`import_questions_from_file(file_path)`**
   - Thêm kiểm tra file rỗng
   - Thêm kiểm tra file văn bản
   - Cập nhật thông báo lỗi với emoji
   - Hỗ trợ .doc, .docx

---

## 🐛 Khắc phục lỗi

### Lỗi: "⚠️  Thư viện python-docx chưa được cài đặt"

**Giải pháp:**
```bash
pip install python-docx
```

### Lỗi: "File không phải là file văn bản"

**Giải pháp:**
- Kiểm tra đuôi file (phải là .txt, .doc, .docx)
- Nếu là file khác, hãy chuyển đổi sang một trong các định dạng được hỗ trợ

### Lỗi: "Không thể đọc file"

**Giải pháp:**
- Kiểm tra file có bị hỏng không
- Cố gắng mở file bằng text editor (Notepad, VS Code)
- Lưu lại file với mã hóa UTF-8

