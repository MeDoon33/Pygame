#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cắt các frame đường đạn từ hoacau.png và tạo hoạt ảnh
"""
from PIL import Image
import os

# Ensure output directories exist
os.makedirs('assets/enemy_projectiles', exist_ok=True)
os.makedirs('debug_frames', exist_ok=True)

# ===== PHÂN TÍCH FILE HOACAU.PNG =====
print("=" * 60)
print("PHÂN TÍCH FILE HOACAU.PNG")
print("=" * 60)

img = Image.open('assets/hoacau.png')
w, h = img.size
print(f'Kích thước ảnh gốc: {w} × {h} pixel')

# Hiển thị ảnh gốc
img.save('debug_frames/hoacau_original.png')
print(f"✅ Ảnh gốc lưu tại: debug_frames/hoacau_original.png")

# ===== CẮT CÁC FRAME =====
print("\n" + "=" * 60)
print("CẮT FRAMES ĐƯỜNG ĐẠN")
print("=" * 60)

# Cắt 4 frame từ spritesheet ngang
frame_count = 4
frame_width = w // frame_count

print(f"Cắt {frame_count} frames, mỗi frame {frame_width} × {h} pixel")

# Cắt các frame
for i in range(frame_count):
    x1 = i * frame_width
    x2 = x1 + frame_width
    frame = img.crop((x1, 0, x2, h))
    frame.save(f'assets/enemy_projectiles/hoacau_frame_{i}.png')
    print(f"Frame {i}: {frame.size} - Lưu tại hoacau_frame_{i}.png")

# Hiển thị preview
for i in range(frame_count):
    frame = Image.open(f'assets/enemy_projectiles/hoacau_frame_{i}.png')
    frame.save(f'debug_frames/hoacau_frame_{i}_preview.png')

print(f"\n✅ Đã cắt {frame_count} frame từ hoacau.png")
print("Các file frame lưu tại: assets/enemy_projectiles/")
print("\n" + "=" * 60)
print("THÔNG TIN CẤU HÌNH HOẠT ẢNH")
print("=" * 60)
print(f"Frame width:  {frame_width}")
print(f"Frame height: {h}")
print(f"Total frames: {frame_count}")
print(f"Thích hợp để: Đường đạn tấn công của enemy")
