"""
Ghép 6 frame tấn công thành spritesheet ngang (enemy_attack.png)
"""
from PIL import Image
import os

# Đường dẫn các frame đã cắt
frame_dir = 'assets/enemy_frames_attack'
output_path = 'assets/enemy_attack.png'
frame_count = 6

# Lấy kích thước frame từ frame đầu tiên
frame0 = Image.open(os.path.join(frame_dir, 'enemy_attack_frame_0.png'))
original_w, original_h = frame0.size

# Target size to match idle animation
target_w, target_h = 146, 150

# Tạo ảnh mới (6 frame xếp ngang)
sheet = Image.new('RGBA', (target_w * frame_count, target_h))

for i in range(frame_count):
    frame_path = os.path.join(frame_dir, f'enemy_attack_frame_{i}.png')
    frame = Image.open(frame_path)
    # Xoay frame về hướng xuống (90 độ theo chiều kim đồng hồ)
    frame = frame.rotate(-90, expand=True)
    # Resize frame to target size
    frame = frame.resize((target_w, target_h), Image.Resampling.LANCZOS)
    sheet.paste(frame, (i * target_w, 0))

sheet.save(output_path)
print(f'Saved spritesheet: {output_path} ({sheet.size})')
