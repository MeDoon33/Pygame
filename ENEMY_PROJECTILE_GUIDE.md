# Enemy Projectile Animation (Hỏa Cầu) - Hướng Dẫn Sử Dụng

## 📋 Tổng Quan

Bạn đã cắt thành công 4 frame từ `hoacau.png` tạo hoạt ảnh đường đạn cho enemy.

### Thông Tin Frames
- **Số frame:** 4
- **Kích thước mỗi frame:** 256 × 175 pixel
- **Định dạng:** PNG với alpha transparency (RGBA)
- **Vị trí lưu:** `assets/enemy_projectiles/`

### Danh Sách Frames
```
assets/enemy_projectiles/
├── hoacau_frame_0.png (quả bóng nhỏ)
├── hoacau_frame_1.png (quả bóng medium)
├── hoacau_frame_2.png (quả bóng lớn - tấn công)
└── hoacau_frame_3.png (hiệu ứng phun lửa)
```

## 🚀 Cách Sử Dụng

### Cách 1: Tạo và Quản Lý Đường Đạn Riêng Lẻ

```python
import pygame
from enemy_projectile_animation import Projectile

pygame.init()

# Tạo quả đạn từ enemy (240, 200) hướng tới player (100, 500)
projectile = Projectile(
    x=240,                  # Vị trí khởi phát X
    y=200,                  # Vị trí khởi phát Y
    target_x=100,           # Mục tiêu X
    target_y=500,           # Mục tiêu Y
    speed=300,              # Tốc độ 300 pixel/giây
    damage=15               # Sát thương 15
)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    projectile.update(dt)
    
    screen.fill((0, 0, 0))
    projectile.draw(screen)
    pygame.display.flip()

pygame.quit()
```

### Cách 2: Quản Lý Danh Sách Đường Đạn

```python
from enemy_projectile_animation import Projectile

class ProjectileManager:
    def __init__(self):
        self.projectiles = []
    
    def fire(self, start_x, start_y, target_x, target_y):
        """Bắn một quả đạn"""
        projectile = Projectile(start_x, start_y, target_x, target_y)
        self.projectiles.append(projectile)
    
    def update(self, dt):
        """Cập nhật tất cả đường đạn"""
        for proj in self.projectiles:
            proj.update(dt)
        
        # Xóa các quả đạn không còn hoạt động
        self.projectiles = [p for p in self.projectiles if p.active]
    
    def draw(self, surface):
        """Vẽ tất cả đường đạn"""
        for proj in self.projectiles:
            proj.draw(surface)
    
    def check_collisions(self, player):
        """Kiểm tra va chạm với player"""
        for proj in self.projectiles:
            if proj.get_rect().colliderect(player.get_rect()):
                player.take_damage(proj.damage)
                proj.active = False

# Sử dụng
manager = ProjectileManager()

# Trong game loop
manager.fire(enemy.x, enemy.y, player.x, player.y)
manager.update(dt)
manager.draw(screen)
manager.check_collisions(player)
```

## 📊 API Reference

### `ProjectileAnimator` Class

**Methods:**
- `play()` - Bắt đầu phát hoạt ảnh
- `stop()` - Dừng hoạt ảnh
- `update(dt)` - Cập nhật frame (gọi mỗi frame với delta time)
- `draw(surface, x, y, rotation)` - Vẽ quả đạn
- `get_current_frame()` - Lấy frame hiện tại

**Thuộc tính:**
- `frames` - Danh sách 4 frame
- `current_frame` - Index frame hiện tại (0-3)
- `is_playing` - Trạng thái phát
- `frame_duration` - Thời gian mỗi frame (mặc định 0.15s)

---

### `Projectile` Class

**Constructor:**
```python
Projectile(x, y, target_x, target_y, speed=200, damage=10)
```

**Tham số:**
- `x, y` - Vị trí khởi phát
- `target_x, target_y` - Mục tiêu
- `speed` - Tốc độ di chuyển (pixel/giây)
- `damage` - Sát thương gây ra

**Methods:**
- `update(dt)` - Cập nhật vị trí và hoạt ảnh
- `draw(surface)` - Vẽ quả đạn
- `get_rect()` - Lấy rect để kiểm tra va chạm

**Thuộc tính:**
- `x, y` - Vị trí hiện tại
- `vx, vy` - Velocity (tốc độ)
- `angle` - Góc xoay (độ)
- `active` - Trạng thái hoạt động
- `life_time` - Thời gian sống
- `animator` - ProjectileAnimator instance

---

## ⚙️ Tùy Chỉnh

### Thay Đổi Tốc Độ Đường Đạn

```python
# Nhanh hơn
projectile = Projectile(x, y, tx, ty, speed=500)

# Chậm hơn
projectile = Projectile(x, y, tx, ty, speed=100)
```

### Thay Đổi Sát Thương

```python
# Sát thương cao
projectile = Projectile(x, y, tx, ty, damage=30)

# Sát thương thấp
projectile = Projectile(x, y, tx, ty, damage=5)
```

### Tùy Chỉnh Frame Duration

```python
animator = ProjectileAnimator(frame_duration=0.1)  # Nhanh hơn
animator = ProjectileAnimator(frame_duration=0.3)  # Chậm hơn
```

### Thay Đổi Kích Thước Quả Đạn

```python
# Phóng to
animator = ProjectileAnimator(frame_width=384, frame_height=262)

# Thu nhỏ
animator = ProjectileAnimator(frame_width=128, frame_height=88)
```

## 🎮 Tích Hợp Vào Game

### Trong Enemy Class

```python
class Enemy:
    def __init__(self):
        self.projectiles = []
        self.attack_timer = 0
        self.attack_cooldown = 2  # 2 giây
    
    def shoot_projectile(self, target_x, target_y):
        """Bắn đường đạn"""
        projectile = Projectile(
            self.x, self.y,
            target_x, target_y,
            speed=250,
            damage=self.atk
        )
        self.projectiles.append(projectile)
    
    def update(self, dt, player):
        self.attack_timer += dt
        
        # Bắn nếu có cooldown
        if self.attack_timer >= self.attack_cooldown:
            self.shoot_projectile(player.x, player.y)
            self.attack_timer = 0
        
        # Cập nhật đường đạn
        for proj in self.projectiles:
            proj.update(dt)
        self.projectiles = [p for p in self.projectiles if p.active]
    
    def draw(self, surface):
        # Vẽ enemy
        # ...
        
        # Vẽ đường đạn
        for proj in self.projectiles:
            proj.draw(surface)
```

### Trong Game Loop

```python
def update(self, dt):
    self.enemy.update(dt, self.player)
    
    # Kiểm tra va chạm đường đạn với player
    for proj in self.enemy.projectiles:
        if proj.get_rect().colliderect(self.player.get_rect()):
            self.player.take_damage(proj.damage)
            proj.active = False
```

## 🎨 Preview

Các frame preview có sẵn tại: `debug_frames/hoacau_frame_X_preview.png`

## 📝 Scripts Liên Quan

- [cut_projectile_frames.py](cut_projectile_frames.py) - Script cắt frames
- [enemy_projectile_animation.py](enemy_projectile_animation.py) - Module hoạt ảnh
- [demo_projectile_animation.py](demo_projectile_animation.py) - Demo hoạt ảnh

## 🐛 Troubleshooting

**Vấn đề:** Import error
```
ModuleNotFoundError: No module named 'enemy_projectile_animation'
```
**Giải pháp:** Đảm bảo file `enemy_projectile_animation.py` trong cùng thư mục game

---

**Vấn đề:** Đường đạn không hiển thị
```python
# Kiểm tra projectile.active
if projectile.active:
    print("Projectile is active")
```
**Giải pháp:** Đảm bảo gọi `draw()` mỗi frame và `active=True`

---

**Vấn đề:** Đường đạn di chuyển sai hướng
**Giải pháp:** Kiểm tra tọa độ target, có thể cần đảo trục Y:
```python
projectile = Projectile(x, y, target_x, -target_y, speed=300)
```

## 📌 Ghi Chú

- Quả đạn tự động xoay hướng tới mục tiêu
- Animation tự động lặp lại khi projectile còn active
- Va chạm sử dụng circular collision (radius-based)
- Max lifetime là 10 giây (sau đó projectile sẽ deactivate)

---

**Tạo bởi:** Enemy Projectile System  
**Ngày tạo:** 2026  
**Phiên bản:** 1.0
