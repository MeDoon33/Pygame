#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tải và sử dụng 4 frames hoạt ảnh tấn công của enemy
Có thể import hàm này để dùng trong game
"""
import pygame
from typing import List

def load_enemy_attack_animation(frame_width=406, frame_height=277, convert_alpha=True) -> List[pygame.Surface]:
    """
    Load 4 frames hoạt ảnh tấn công của enemy
    
    Args:
        frame_width: Chiều rộng frame (mặc định 406)
        frame_height: Chiều cao frame (mặc định 277)
        convert_alpha: Convert với alpha (yêu cầu video mode được set)
    
    Returns:
        List các pygame.Surface đại diện cho 4 frame
    
    Ví dụ:
        frames = load_enemy_attack_animation()
        # Sử dụng frames[0], frames[1], frames[2], frames[3]
    """
    frames = []
    for i in range(4):
        frame_path = f'assets/enemy_frames_attack_4f/enemy_attack_4frame_{i}.png'
        try:
            frame = pygame.image.load(frame_path)
            if convert_alpha:
                try:
                    frame = frame.convert_alpha()
                except:
                    pass  # Nếu video mode chưa set, bỏ qua convert
            # Scale nếu cần
            frame = pygame.transform.scale(frame, (frame_width, frame_height))
            frames.append(frame)
        except Exception as e:
            print(f"Lỗi load frame {i}: {e}")
            # Tạo frame mặc định nếu load thất bại
            default_frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            pygame.draw.circle(default_frame, (255, 0, 0), (frame_width//2, frame_height//2), 20)
            frames.append(default_frame)
    
    return frames


class EnemyAttackAnimator:
    """
    Class quản lý hoạt ảnh tấn công của enemy
    """
    def __init__(self, frame_width=406, frame_height=277, frame_duration=0.2):
        """
        Khởi tạo animator
        
        Args:
            frame_width: Chiều rộng frame
            frame_height: Chiều cao frame
            frame_duration: Thời gian hiển thị mỗi frame (giây)
        """
        self.frames = load_enemy_attack_animation(frame_width, frame_height)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_elapsed = 0.0
        self.is_playing = False
    
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
    
    def is_finished(self) -> bool:
        """Kiểm tra hoạt ảnh đã kết thúc"""
        return not self.is_playing and self.current_frame == 0
    
    def update(self, dt: float):
        """
        Cập nhật trạng thái hoạt ảnh
        
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
                self.is_playing = False
                self.current_frame = 0
    
    def draw(self, surface: pygame.Surface, x: int, y: int):
        """
        Vẽ frame hiện tại
        
        Args:
            surface: Pygame surface để vẽ vào
            x: Tọa độ X
            y: Tọa độ Y
        """
        if 0 <= self.current_frame < len(self.frames):
            surface.blit(self.frames[self.current_frame], (x, y))
    
    def get_current_frame(self) -> pygame.Surface:
        """Lấy frame hiện tại"""
        if 0 <= self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None


if __name__ == "__main__":
    # Demo
    pygame.init()
    
    animator = EnemyAttackAnimator()
    
    print("EnemyAttackAnimator loaded successfully!")
    print(f"Total frames: {len(animator.frames)}")
    print(f"Frame size: {animator.frame_width}x{animator.frame_height}")
    print(f"Frame duration: {animator.frame_duration}s")
    print("\nUsage:")
    print("  from enemy_attack_animation import load_enemy_attack_animation, EnemyAttackAnimator")
    print("  frames = load_enemy_attack_animation()")
    print("  animator = EnemyAttackAnimator()")
    print("  animator.play()")
    print("  animator.update(delta_time)")
    print("  animator.draw(surface, x, y)")
