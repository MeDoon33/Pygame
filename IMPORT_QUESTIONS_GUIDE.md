# Hướng dẫn nhập câu hỏi từ file văn bản

## Cách sử dụng

1. **Tại menu chính**, chọn tùy chọn **"Tạo câu hỏi từ file"**
2. **File dialog** sẽ mở ra - chọn file `.txt` từ máy tính của bạn
3. Nếu thành công, bạn sẽ thấy thông báo "Thành công! Import N câu hỏi" trên menu
4. Các câu hỏi sẽ được tự động lưu vào `questions.json` và có sẵn để dùng trong game

## Format file văn bản

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

## Lưu ý

- File phải có mã hóa **UTF-8**
- Nếu đáp án không hợp lệ, nó sẽ mặc định là `0` (đáp án đầu tiên)
- Nếu thiếu phần thưởng, nó sẽ mặc định là `"Sát thương +10%"`
- File dialog chỉ hiển thị file `.txt`, nhưng bạn có thể chọn tất cả file types nếu cần

## Tệp mẫu

Xem file `questions_sample.txt` để xem ví dụ đầy đủ

## Menu

- **Hướng dẫn**: Xem hướng dẫn chơi game và danh sách các câu hỏi đã import
- **Tạo câu hỏi từ file**: Mở file dialog để import câu hỏi từ file `.txt`

