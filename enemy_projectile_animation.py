#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hoạt ảnh đường đạn hỏa cầu của enemy
Module này quản lý hoạt ảnh và vật lý của đường đạn
"""
import pygame
import math
from typing import List, Tuple

# ==================== PROJECTILE ANIMATOR ====================

class ProjectileAnimator:
    """Quản lý hoạt ảnh của quả hỏa cầu"""
    
    def __init__(self, frame_width=256, frame_height=175, frame_duration=0.15):
        """
        Khởi tạo animator cho quả đạn
        
        Args:
            frame_width: Chiều rộng frame (default: 256)
            frame_height: Chiều cao frame (default: 175)
            frame_duration: Thời gian mỗi frame (giây)
        """
        self.frames = self._load_projectile_frames(frame_width, frame_height)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_elapsed = 0.0
        self.is_playing = False
    
    def _load_projectile_frames(self, frame_width, frame_height) -> List[pygame.Surface]:
        """Load 4 frames của quả đạn"""
        frames = []
        for i in range(4):
            frame_path = f'assets/enemy_projectiles/hoacau_frame_{i}.png'
            try:
                frame = pygame.image.load(frame_path)
                # Scale nếu cần
                frame = pygame.transform.scale(frame, (frame_width, frame_height))
                frames.append(frame)
            except Exception as e:
                print(f"Lỗi load projectile frame {i}: {e}")
                # Tạo frame mặc định nếu thất bại
                default_frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                pygame.draw.circle(default_frame, (255, 150, 0), (frame_width//2, frame_height//2), 20)
                frames.append(default_frame)
        return frames
    
    def play(self):
        """Bắt đầu phát hoạt ảnh"""
        self.is_playing = True
        self.current_frame = 0
        self.time_elapsed = 0.0
    
    def stop(self):
        """Dừng hoạt ảnh"""
        self.is_playing = False
        self.current_frame = 0
        self.time_elapsed = 0.0
    
    def update(self, dt: float):
        """
        Cập nhật hoạt ảnh
        
        Args:
            dt: Delta time (giây)
        """
        if not self.is_playing:
            return
        
        self.time_elapsed += dt
        if self.time_elapsed >= self.frame_duration:
            self.current_frame += 1
            self.time_elapsed = 0.0
            
            if self.current_frame >= len(self.frames):
                self.current_frame = 0  # Loop
    
    def get_current_frame(self) -> pygame.Surface:
        """Lấy frame hiện tại"""
        if 0 <= self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None
    
    def draw(self, surface: pygame.Surface, x: int, y: int, rotation: float = 0):
        """
        Vẽ quả đạn
        
        Args:
            surface: Pygame surface để vẽ vào
            x: Tọa độ X
            y: Tọa độ Y
            rotation: Góc xoay (độ)
        """
        frame = self.get_current_frame()
        if frame is None:
            return
        
        # Xoay frame nếu cần
        if rotation != 0:
            frame = pygame.transform.rotate(frame, rotation)
        
        # Vẽ căn giữa
        rect = frame.get_rect(center=(x, y))
        surface.blit(frame, rect)


# ==================== PROJECTILE CLASS ====================

class Projectile:
    """
    Đường đạn hỏa cầu của enemy
    """
    
    def __init__(self, x: int, y: int, target_x: int, target_y: int, 
                 speed: float = 200, damage: int = 10):
        """
        Khởi tạo quả đạn
        
        Args:
            x, y: Vị trí khởi phát
            target_x, target_y: Vị trí mục tiêu
            speed: Tốc độ pixel/giây
            damage: Sát thương gây ra
        """
        self.x = float(x)
        self.y = float(y)
        self.start_x = x
        self.start_y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.damage = damage
        self.active = True
        self.life_time = 0
        self.max_life_time = 10  # 10 giây max
        
        # Tính vector hướng
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0
            self.vy = 0
        
        # Animation
        self.animator = ProjectileAnimator()
        self.animator.play()
        
        # Góc xoay (lật ngược 180 độ để hỏa cầu hướng đúng)
        self.angle = math.degrees(math.atan2(dy, dx)) + 180
        
        # Size
        self.radius = 20
    
    def update(self, dt: float):
        """Cập nhật vị trí và hoạt ảnh"""
        if not self.active:
            return
        
        # Cập nhật vị trí
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life_time += dt
        
        # Cập nhật hoạt ảnh
        self.animator.update(dt)
        
        # Kiểm tra khoảng cách hoặc thời gian
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Nếu đến gần đích hoặc quá lâu, deactivate
        if dist < 30 or self.life_time > self.max_life_time:
            self.active = False
    
    def draw(self, surface: pygame.Surface):
        """Vẽ quả đạn"""
        if not self.active:
            return
        
        self.animator.draw(surface, int(self.x), int(self.y), self.angle)
    
    def get_rect(self) -> pygame.Rect:
        """Lấy rect để kiểm tra va chạm"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)


if __name__ == "__main__":
    # Demo
    pygame.init()
    
    animator = ProjectileAnimator()
    
    print("ProjectileAnimator loaded successfully!")
    print(f"Total frames: {len(animator.frames)}")
    print(f"Frame size: {animator.frame_width}x{animator.frame_height}")
    print(f"Frame duration: {animator.frame_duration}s")
    print("\nUsage:")
    print("  from enemy_projectile_animation import ProjectileAnimator, Projectile")
    print("  animator = ProjectileAnimator()")
    print("  projectile = Projectile(x, y, target_x, target_y)")
    print("  projectile.update(delta_time)")
    print("  projectile.draw(surface)")
