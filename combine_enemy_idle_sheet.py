"""
Ghép 6 frame enemy thành spritesheet ngang (enemy_idle.png)
"""
from PIL import Image
import os

# Đường dẫn các frame đã cắt
frame_dir = 'assets/enemy_frames'
output_path = 'assets/enemy_idle.png'
frame_count = 6
frame_w, frame_h = 146, 150

# Tạo ảnh mới (6 frame xếp ngang)
sheet = Image.new('RGBA', (frame_w * frame_count, frame_h))

for i in range(frame_count):
    frame_path = os.path.join(frame_dir, f'enemy_frame_{i}.png')
    frame = Image.open(frame_path)
    sheet.paste(frame, (i * frame_w, 0))

sheet.save(output_path)
print(f'Saved spritesheet: {output_path} ({sheet.size})')
