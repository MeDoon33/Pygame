#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: Hiển thị hoạt ảnh đường đạn hỏa cầu
"""
import pygame
from enemy_projectile_animation import ProjectileAnimator, Projectile
import math

# Khởi tạo pygame
pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Enemy Projectile Animation Demo")
clock = pygame.time.Clock()

# Tạo animator
animator = ProjectileAnimator()
animator.play()

print("=" * 60)
print("PROJECTILE ANIMATION DEMO")
print("=" * 60)
print(f"Frames loaded: {len(animator.frames)}")
print(f"Frame size: {animator.frame_width}x{animator.frame_height}")
print(f"Animation speed: {animator.frame_duration}s per frame")
print("\nControls:")
print("  SPACE - Reset animation")
print("  ESC   - Exit")
print("=" * 60 + "\n")

# Tạo projectile di chuyển từ trái sang phải
projectile = Projectile(
    x=100, y=300,
    target_x=WINDOW_WIDTH - 100, target_y=300,
    speed=300,
    damage=15
)

running = True
angle = 0

while running:
    dt = clock.tick(FPS) / 1000.0
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                # Reset projectile
                projectile = Projectile(
                    x=100, y=300,
                    target_x=WINDOW_WIDTH - 100, target_y=300,
                    speed=300,
                    damage=15
                )
                angle = 0
    
    # Update
    projectile.update(dt)
    angle += 180 * dt  # Xoay nhanh để demo
    
    # Nếu projectile hết, tạo cái mới
    if not projectile.active:
        projectile = Projectile(
            x=100, y=300,
            target_x=WINDOW_WIDTH - 100, target_y=300,
            speed=300,
            damage=15
        )
    
    # Draw
    screen.fill((30, 30, 40))
    
    # Vẽ lưới
    for x in range(0, WINDOW_WIDTH, 50):
        pygame.draw.line(screen, (60, 60, 80), (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, 50):
        pygame.draw.line(screen, (60, 60, 80), (0, y), (WINDOW_WIDTH, y))
    
    # Vẽ đường đạn
    projectile.draw(screen)
    
    # Vẽ vị trí khởi phát
    pygame.draw.circle(screen, (100, 255, 100), (int(projectile.start_x), int(projectile.start_y)), 10)
    
    # Vẽ mục tiêu
    pygame.draw.circle(screen, (255, 100, 100), (projectile.target_x, projectile.target_y), 15, 3)
    
    # Thông tin
    font = pygame.font.Font(None, 28)
    info = [
        f"Position: ({projectile.x:.0f}, {projectile.y:.0f})",
        f"Frame: {projectile.animator.current_frame + 1}/4",
        f"Life time: {projectile.life_time:.2f}s",
        f"Active: {projectile.active}",
        f"Speed: 300 px/s",
        "",
        "SPACE - Reset | ESC - Exit"
    ]
    
    y_offset = 20
    for text in info:
        t = font.render(text, True, (255, 255, 255))
        screen.blit(t, (20, y_offset))
        y_offset += 35
    
    pygame.display.flip()

pygame.quit()
print("\n✅ Demo ended")
