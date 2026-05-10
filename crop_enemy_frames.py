"""
Cắt enemy.png thành các frame riêng lẻ
"""
from PIL import Image
import os

# Ensure debug_frames directory exists
os.makedirs('debug_frames', exist_ok=True)
os.makedirs('assets/enemy_frames', exist_ok=True)

# Load enemy image (6 frames horizontally)
img = Image.open('assets/enemy.png')
print(f'Enemy image size: {img.size}')

w, h = img.size
frame_count = 6
frame_width = w // frame_count

frames = []
for i in range(frame_count):
    x1 = i * frame_width
    frame = img.crop((x1, 0, x1 + frame_width, h))
    frame.save(f'assets/enemy_frames/enemy_frame_{i}.png')
    frames.append(frame)
    print(f"Frame {i}: saved as enemy_frame_{i}.png ({frame.size})")

# Hiển thị các frame
for i, frame in enumerate(frames):
    frame.save(f'debug_frames/enemy_frame_{i}_preview.png')

print(f"\n✅ Đã cắt {frame_count} frame từ enemy.png")
print("Các file frame lưu tại: assets/enemy_frames/")
print("\nBạn muốn ghép lại như thế nào?")
print("- Dọc (4 frame xếp theo chiều dọc)?")
print("- Giữ nguyên ngang?")
print("- Khác?")
