# Enemy Attack Animation (4 Frames) - Hướng Dẫn Sử Dụng

## 📋 Tổng Quan

Bạn đã cắt thành công 4 frame từ `enemy_attack.png` và tạo hoạt ảnh tấn công cho enemy.

### Thông Tin Frames
- **Số frame:** 4
- **Kích thước mỗi frame:** 406 × 277 pixel
- **Định dạng:** PNG với alpha transparency (RGBA)
- **Vị trí lưu:** `assets/enemy_frames_attack_4f/`

### Danh Sách Frames
```
assets/enemy_frames_attack_4f/
├── enemy_attack_4frame_0.png (frame 1)
├── enemy_attack_4frame_1.png (frame 2)
├── enemy_attack_4frame_2.png (frame 3)
└── enemy_attack_4frame_3.png (frame 4)
```

## 🚀 Cách Sử Dụng

### Cách 1: Import Module (Khuyến Nghị)

Sử dụng module tiện ích `enemy_attack_animation.py`:

```python
import pygame
from enemy_attack_animation import load_enemy_attack_animation, EnemyAttackAnimator

# Khởi tạo pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Cách A: Lấy danh sách frames trực tiếp
frames = load_enemy_attack_animation()
print(f"Đã load {len(frames)} frames")

# Cách B: Sử dụng class EnemyAttackAnimator (tự động quản lý)
animator = EnemyAttackAnimator(
    frame_width=406,
    frame_height=277,
    frame_duration=0.2  # 0.2 giây mỗi frame = 5 FPS animation
)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                animator.play()  # Bắt đầu hoạt ảnh khi nhấn Space
    
    animator.update(dt)
    
    screen.fill((0, 0, 0))
    animator.draw(screen, 200, 150)
    pygame.display.flip()

pygame.quit()
```

### Cách 2: Load Thủ Công

```python
import pygame

pygame.init()

frames = []
for i in range(4):
    frame = pygame.image.load(f'assets/enemy_frames_attack_4f/enemy_attack_4frame_{i}.png').convert_alpha()
    frames.append(frame)

# Sử dụng frames trong animation loop
current_frame = 0
frame_time = 0.2  # giây

for event in pygame.event.get():
    # ... xử lý events ...
    
# Update
frame_time -= dt
if frame_time <= 0:
    current_frame = (current_frame + 1) % 4
    frame_time = 0.2

# Draw
screen.blit(frames[current_frame], (x, y))
```

## 📊 API Reference

### `load_enemy_attack_animation(frame_width=406, frame_height=277) -> List[pygame.Surface]`
Load 4 frames hoạt ảnh tấn công.

**Tham số:**
- `frame_width` (int): Chiều rộng của frame (default: 406)
- `frame_height` (int): Chiều cao của frame (default: 277)

**Trả về:** List chứa 4 pygame.Surface objects

---

### `EnemyAttackAnimator` Class

**Methods:**
- `play()` - Bắt đầu phát hoạt ảnh
- `stop()` - Dừng hoạt ảnh
- `update(dt: float)` - Cập nhật trạng thái (gọi mỗi frame với delta time)
- `draw(surface, x, y)` - Vẽ frame hiện tại lên surface
- `is_finished() -> bool` - Kiểm tra hoạt ảnh đã xong
- `get_current_frame() -> pygame.Surface` - Lấy frame hiện tại

**Thuộc tính:**
- `frames` - Danh sách frames
- `current_frame` - Index frame hiện tại (0-3)
- `is_playing` - Trạng thái phát hoạt ảnh
- `frame_duration` - Thời gian mỗi frame (giây)

---

## ⚙️ Tùy Chỉnh

### Thay Đổi Tốc Độ Hoạt Ảnh

```python
# Hoạt ảnh nhanh hơn (0.1s mỗi frame = 10 FPS)
animator = EnemyAttackAnimator(frame_duration=0.1)

# Hoạt ảnh chậm hơn (0.5s mỗi frame = 2 FPS)
animator = EnemyAttackAnimator(frame_duration=0.5)
```

### Thay Đổi Kích Thước Frame

```python
# Phóng to 2x
frames = load_enemy_attack_animation(frame_width=812, frame_height=554)

# Thu nhỏ 0.5x
frames = load_enemy_attack_animation(frame_width=203, frame_height=138)
```

### Hoạt ảnh Vòng Lặp

```python
class LoopingEnemyAttackAnimator(EnemyAttackAnimator):
    def update(self, dt: float):
        if not self.is_playing:
            return
        
        self.time_elapsed += dt
        if self.time_elapsed >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.time_elapsed = 0.0

animator = LoopingEnemyAttackAnimator()
animator.play()  # Sẽ lặp vô tận
```

## 🎨 Preview

Các frame preview có sẵn tại: `debug_frames/enemy_attack_4frame_X_preview.png`

## 📝 Scripts Liên Quan

- `cut_4frames_animation.py` - Script cắt frames và tạo animation
- `enemy_attack_animation.py` - Module tiện ích animation
- `crop_enemy_attack_frames.py` - Cắt 6 frames (cũ)
- `combine_enemy_attack_sheet.py` - Ghép frames thành spritesheet

## 🐛 Troubleshooting

**Vấn đề:** Import error
```python
ModuleNotFoundError: No module named 'pygame'
```
**Giải pháp:** Cài đặt pygame
```bash
pip install pygame
```

**Vấn đề:** Không tìm thấy file frames
```
FileNotFoundError: assets/enemy_frames_attack_4f/enemy_attack_4frame_0.png
```
**Giải pháp:** Chạy `cut_4frames_animation.py` để tạo frames

**Vấn đề:** Frame bị mờ/giãn
**Giải pháp:** Kiểm tra kích thước frame khi load:
```python
frames = load_enemy_attack_animation(frame_width=406, frame_height=277)
```

## 📌 Ghi Chú

- Tất cả frames đều hỗ trợ transparency (alpha channel)
- Khi resize, tốt nhất sử dụng `pygame.transform.scale()` để giữ chất lượng
- Đối với animation vòng lặp, sử dụng modulo (`% 4`) để quay lại frame 0
- Frame rate khuyến nghị: 60 FPS (delta time ~0.016s)

---

**Tạo bởi:** Enemy Animation System  
**Ngày tạo:** 2026  
**Phiên bản:** 1.0
