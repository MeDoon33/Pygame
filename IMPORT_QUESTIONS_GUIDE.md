# Hướng dẫn nhập câu hỏi từ file văn bản

## Cách sử dụng

1. **Tại menu chính**, chọn tùy chọn **"Tạo câu hỏi từ file"**
2. **File dialog** sẽ mở ra - chọn file từ máy tính của bạn
   - Hỗ trợ các định dạng: `.txt`, `.doc`, `.docx`
3. Hệ thống sẽ tự động:
   - ✅ Kiểm tra file có rỗng không
   - ✅ Kiểm tra file có phải văn bản không
   - ✅ Xác thực nội dung câu hỏi
4. Nếu thành công, bạn sẽ thấy thông báo "✅ Thành công! Import N câu hỏi" trên menu
5. Các câu hỏi sẽ được tự động lưu vào `questions.json` và có sẵn để dùng trong game

## Định dạng file văn bản được hỗ trợ

### ✅ Được hỗ trợ

1. **Text files (.txt)**
   - Mã hóa: UTF-8, ASCII, Latin-1
   - Cách tạo: Dùng Notepad, VS Code, hoặc bất kỳ text editor nào
   - Lưu với mã hóa UTF-8 để hỗ trợ tiếng Việt

2. **Word documents (.docx)**
   - Word 2007 trở lên
   - Yêu cầu thư viện: `python-docx`
   - Cài đặt: `pip install python-docx`
   - Sao chép nội dung từ Word rồi lưu thành file

3. **Word documents (.doc)**
   - Word 97-2003
   - Cũng yêu cầu `python-docx`
   - Có thể chuyển đổi sang `.docx` để dễ sử dụng

### Format nội dung câu hỏi

Mỗi câu hỏi được định dạng như sau:

```
Câu hỏi?
Option 1
Option 2
Option 3
Option 4
Correct: 1
Reward: Tên reward

[dòng trống]

Câu hỏi tiếp theo?
...
```

### Giải thích:
- **Câu hỏi**: Dòng đầu tiên là câu hỏi (kết thúc bằng `?`)
- **4 lựa chọn**: Tiếp theo là 4 lựa chọn (mỗi dòng một)
- **Correct**: Chỉ số đáp án đúng (từ 1 đến 4)
- **Reward**: Phần thưởng khi trả lời đúng
- **Dòng trống**: Các câu hỏi cách nhau bằng một dòng trống

## Ví dụ

```
Python được phát triển bởi ai?
Guido van Rossum
Dennis Ritchie
Bjarne Stroustrup
James Gosling
Correct: 1
Reward: Sát thương +50%

Năm nào Python được ra mắt?
1989
1991
1995
2000
Correct: 2
Reward: Hồi máu 50HP
```

## Kiểm tra và xác thực

Hệ thống sẽ tự động kiểm tra:

### 1️⃣ File có rỗng không?
- ❌ Nếu file rỗng, sẽ hiển thị: "Lỗi: File rỗng"
- ✅ File phải có nội dung

### 2️⃣ File có phải văn bản không?
- ❌ Nếu file là file nhị phân (ảnh, video, .zip), sẽ lỗi
- ❌ File .pdf không được hỗ trợ
- ✅ Chỉ hỗ trợ: .txt, .doc, .docx

### 3️⃣ Nội dung có hợp lệ không?
- ❌ Nếu thiếu thông tin bắt buộc (câu hỏi, 4 option, correct, reward)
- ❌ Nếu không tìm thấy câu hỏi nào hợp lệ
- ✅ Hệ thống tự động bỏ qua các câu hỏi không hợp lệ

## Lưu ý

- **File UTF-8**: File phải có mã hóa **UTF-8** để hỗ trợ tiếng Việt
- **Đáp án mặc định**: Nếu đáp án không hợp lệ, nó sẽ mặc định là `0` (đáp án đầu tiên)
- **Reward mặc định**: Nếu thiếu phần thưởng, nó sẽ mặc định là `"Sát thương +10%"`
- **Loại file**: File dialog mở ra sẽ ưu tiên `.txt` nhưng bạn có thể chọn `.doc` hoặc `.docx`

## Cài đặt thư viện (tùy chọn)

Để hỗ trợ file Word (.docx, .doc), cần cài đặt thư viện `python-docx`:

```bash
pip install python-docx
```

**Không cài đặt**: Chỉ sử dụng được file `.txt`

## Tệp mẫu

Xem file `questions_sample.txt` để xem ví dụ đầy đủ

## Menu

- **Hướng dẫn**: Xem hướng dẫn chơi game và danh sách các câu hỏi đã import
- **Tạo câu hỏi từ file**: Mở file dialog để import câu hỏi từ file (`.txt`, `.doc`, `.docx`)

## Thông báo lỗi phổ biến

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-----------|----------|
| "File rỗng" | File không có nội dung | Kiểm tra file, thêm nội dung hoặc chọn file khác |
| "File không phải là file văn bản" | File là nhị phân (ảnh, video, zip) | Chọn file .txt, .doc hoặc .docx |
| "Không thể trích xuất text từ .docx" | Thư viện `python-docx` chưa cài | Cài: `pip install python-docx` |
| "Không tìm thấy câu hỏi hợp lệ" | Format sai hoặc thiếu thông tin | Kiểm tra format theo hướng dẫn |
| "Lỗi đọc file: [...]" | File bị hỏng hoặc mã hóa lạ | Thử mở file bằng text editor khác, lưu UTF-8 |

