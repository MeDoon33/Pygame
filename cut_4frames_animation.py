#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cắt 4 frame từ enemy_attack.png và tạo hoạt ảnh
"""
from PIL import Image
import pygame
import os
import sys

# Ensure output directories exist
os.makedirs('debug_frames', exist_ok=True)
os.makedirs('assets/enemy_frames_attack_4f', exist_ok=True)

# ===== STEP 1: CẮT 4 FRAME TỪ ENEMY_ATTACK.PNG =====
print("=" * 50)
print("STEP 1: Cắt 4 frame từ enemy_attack.png")
print("=" * 50)

img = Image.open('assets/enemy_attack.png')
print(f'Kích thước ảnh gốc: {img.size}')

w, h = img.size
frame_count = 4
frame_width = w // frame_count

frames_pil = []
for i in range(frame_count):
    x1 = i * frame_width
    frame = img.crop((x1, 0, x1 + frame_width, h))
    frame.save(f'assets/enemy_frames_attack_4f/enemy_attack_4frame_{i}.png')
    frames_pil.append(frame)
    print(f"Frame {i}: Lưu tại enemy_attack_4frame_{i}.png (kích thước: {frame.size})")

# Hiển thị các frame preview
for i, frame in enumerate(frames_pil):
    frame.save(f'debug_frames/enemy_attack_4frame_{i}_preview.png')

print(f"\n✅ Đã cắt {frame_count} frame từ enemy_attack.png")
print("Các file frame lưu tại: assets/enemy_frames_attack_4f/")

# ===== STEP 2: TẠO HOẠT ẢNH =====
print("\n" + "=" * 50)
print("STEP 2: Tạo hoạt ảnh với pygame")
print("=" * 50)

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
FRAME_DELAY = 0.2  # Thời gian mỗi frame (giây)

# Tạo cửa sổ
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Enemy Attack Animation (4 Frames)")
clock = pygame.time.Clock()

# Load frames
frame_size = (frames_pil[0].width, frames_pil[0].height)
print(f"Kích thước frame: {frame_size}")

frames_pygame = []
for i in range(frame_count):
    frame_path = f'assets/enemy_frames_attack_4f/enemy_attack_4frame_{i}.png'
    frame_surface = pygame.image.load(frame_path).convert_alpha()
    frames_pygame.append(frame_surface)

print(f"✅ Đã load {len(frames_pygame)} frames vào pygame")

# Animation state
current_frame = 0
time_elapsed = 0.0

# Vị trí hiển thị frame (giữa màn hình)
frame_x = (WINDOW_WIDTH - frame_size[0]) // 2
frame_y = (WINDOW_HEIGHT - frame_size[1]) // 2

print(f"\nNhấn ESC hoặc đóng cửa sổ để thoát")
print(f"Animation frame delay: {FRAME_DELAY:.1f}s\n")

# Main animation loop
running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Update animation
    time_elapsed += dt
    if time_elapsed >= FRAME_DELAY:
        current_frame = (current_frame + 1) % frame_count
        time_elapsed = 0.0
    
    # Draw
    screen.fill((50, 50, 50))  # Dark background
    
    # Draw current frame
    screen.blit(frames_pygame[current_frame], (frame_x, frame_y))
    
    # Draw frame counter
    font = pygame.font.Font(None, 36)
    counter_text = font.render(f"Frame: {current_frame + 1}/{frame_count}", True, (255, 255, 255))
    screen.blit(counter_text, (20, 20))
    
    # Draw instructions
    font_small = pygame.font.Font(None, 24)
    instr_text = font_small.render("ESC to exit", True, (200, 200, 200))
    screen.blit(instr_text, (20, 70))
    
    pygame.display.flip()

pygame.quit()

print("\n" + "=" * 50)
print("✅ HOÀN THÀNH!")
print("=" * 50)
print(f"4 frames đã được cắt và lưu tại: assets/enemy_frames_attack_4f/")
print(f"Hoạt ảnh đã chạy thành công!")
