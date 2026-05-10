"""
Ghép các frame lại theo chiều dọc thành enemy.png mới
"""
from PIL import Image
import os

# Load các frame
frames = []
for i in range(4):
    frame = Image.open(f'assets/enemy_frames/enemy_frame_{i}.png')
    frames.append(frame)
    print(f"Loaded frame {i}: {frame.size}")

# Kích thước: 219x150 mỗi frame
# Ghép dọc: 219x600 (4 frame x 150px)
frame_width = 219
frame_height = 150
new_height = frame_height * 4

# Tạo spritesheet mới
new_img = Image.new('RGBA', (frame_width, new_height), (0, 0, 0, 0))

# Dán các frame từ trên xuống dưới
for i, frame in enumerate(frames):
    y_offset = i * frame_height
    new_img.paste(frame, (0, y_offset))
    print(f"Pasted frame {i} at y={y_offset}")

# Lưu file mới
new_img.save('assets/enemy.png')
print(f"\n✅ Đã ghép lại enemy.png theo chiều dọc: {new_img.size}")
print("File lưu tại: assets/enemy.png")
