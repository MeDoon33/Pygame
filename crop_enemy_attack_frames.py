"""
Cắt enemy_attack.png thành 6 frame tấn công riêng lẻ
"""
from PIL import Image
import os

# Ensure output directories exist
os.makedirs('debug_frames', exist_ok=True)
os.makedirs('assets/enemy_frames_attack', exist_ok=True)

img = Image.open('assets/enemy_attack.png')
print(f'Enemy attack image size: {img.size}')

w, h = img.size
frame_count = 6
frame_width = w // frame_count

frames = []
for i in range(frame_count):
    x1 = i * frame_width
    frame = img.crop((x1, 0, x1 + frame_width, h))
    frame.save(f'assets/enemy_frames_attack/enemy_attack_frame_{i}.png')
    frames.append(frame)
    print(f"Frame {i}: saved as enemy_attack_frame_{i}.png ({frame.size})")

# Hiển thị các frame preview
for i, frame in enumerate(frames):
    frame.save(f'debug_frames/enemy_attack_frame_{i}_preview.png')

print(f"\n✅ Đã cắt {frame_count} frame từ enemy_actack.png")
print("Các file frame lưu tại: assets/enemy_frames_attack/")
