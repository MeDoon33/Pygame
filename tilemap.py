"""
tilemap.py
==========
Hệ thống tilemap hoàn chỉnh cho Dice Roguelite.

Cung cấp:
  - MapManager: quản lý toàn bộ tilemap
  - Camera: follow nhân vật (non-static mode) hoặc fixed
  - Tileset rendering: vẽ tile từ spritesheet hoặc tạo placeholder
  - MapEditor: editor bản đồ (F1 toggle)
  - Minimap: bản đồ thu nhỏ góc màn hình (F3 toggle)
  - Procedural generation: tạo map theo theme
"""

import pygame
import json
import random
from typing import Optional, Tuple, List, Dict


class Camera:
    """Quản lý viewport / camera khi có scroll"""
    
    def __init__(self, world_width: int, world_height: int, 
                 screen_width: int, screen_height: int, 
                 follow_mode: bool = False):
        self.world_w = world_width
        self.world_h = world_height
        self.screen_w = screen_width
        self.screen_h = screen_height
        self.follow = follow_mode
        
        self.x = 0.0
        self.y = 0.0
    
    def update(self, target_x: float, target_y: float):
        """Center camera on target (follow_mode=True)"""
        if not self.follow:
            return
        
        self.x = target_x - self.screen_w / 2
        self.y = target_y - self.screen_h / 2
        
        # Clamp to world bounds
        self.x = max(0, min(self.x, self.world_w - self.screen_w))
        self.y = max(0, min(self.y, self.world_h - self.screen_h))
    
    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[int, int]:
        """Convert world coords to screen coords"""
        sx = int(world_x - self.x)
        sy = int(world_y - self.y)
        return sx, sy
    
    def screen_to_world(self, screen_x: float, screen_y: float) -> Tuple[int, int]:
        """Convert screen coords to world coords"""
        wx = int(screen_x + self.x)
        wy = int(screen_y + self.y)
        return wx, wy
    
    def get_rect(self) -> pygame.Rect:
        """Get viewport rectangle in world coords"""
        return pygame.Rect(self.x, self.y, self.screen_w, self.screen_h)


class Tileset:
    """Quản lý tileset và rendering tile"""
    
    # Tile IDs
    EMPTY = 0
    GROUND = 1
    WALL = 2
    WATER = 3
    GRASS = 4
    STONE = 5
    DECORATION = 6

    # Lava / fire theme tile IDs
    LAVA_BASE = 0
    LAVA_HOR = 1
    LAVA_VER = 2
    LAVA_CORNER = 3
    LAVA_CORNER_ALT = 4
    LAVA_BUBBLES = 5
    LAVA_RIPPLE = 6
    BRIDGE_STRAIGHT = 10
    BRIDGE_END = 11
    OBSIDIAN_WALL = 12
    OBSIDIAN_FLOW = 13
    LAVA_POOL = 14
    CRACK = 15

    TILE_NAMES = {
        0: "Empty/Black",
        1: "Lava Horizontal",
        2: "Lava Vertical",
        3: "Lava Corner",
        4: "Lava Corner Alt",
        5: "Lava Bubbles",
        6: "Lava Ripple",
        10: "Obsidian Bridge",
        11: "Bridge End",
        12: "Obsidian Wall",
        13: "Lava Flow Wall",
        14: "Lava Pool",
        15: "Crack",
    }
    
    # Tile colors (placeholder nếu không load spritesheet)
    COLORS = {
        0: (20, 15, 35),      # Empty - dark purple / black base
        1: (220, 100, 20),    # Lava horizontal
        2: (220, 90, 30),     # Lava vertical
        3: (200, 80, 30),     # Lava corner
        4: (190, 70, 40),     # Lava corner alt
        5: (230, 120, 50),    # Lava bubbles
        6: (240, 130, 60),    # Lava ripple
        10: (40, 40, 50),     # Obsidian bridge
        11: (50, 50, 60),     # Bridge end
        12: (35, 35, 45),     # Obsidian wall
        13: (80, 30, 30),     # Lava flow wall
        14: (180, 80, 35),    # Lava pool
        15: (120, 50, 30),    # Crack
    }
    
    def __init__(self, tile_width: int = 16, scale: float = 2.0):
        self.tile_w = tile_width
        self.tile_h = tile_width
        self.scale = scale
        self.display_w = int(tile_width * scale)
        self.display_h = int(tile_width * scale)
        
        self.spritesheet = None
        self.frames = {}  # {tile_id: pygame.Surface}
        self._create_placeholder_frames()
    
    def _create_placeholder_frames(self):
        """Tạo placeholder tile nếu không load spritesheet"""
        for tile_id in sorted(set(list(self.COLORS.keys()) + list(self.TILE_NAMES.keys()))):
            color = self.COLORS.get(tile_id, (80, 80, 80))
            surf = pygame.Surface((self.display_w, self.display_h), pygame.SRCALPHA)
            surf.fill(color)
            pygame.draw.rect(surf, (100, 100, 100), 
                             (0, 0, self.display_w, self.display_h), 1)
            self.frames[tile_id] = surf
    
    def load_spritesheet(self, path: str, tile_width: int = 16, scale: float = 2.0):
        """Load tileset từ spritesheet"""
        try:
            self.tile_w = tile_width
            self.tile_h = tile_width
            self.scale = scale
            self.display_w = int(tile_width * scale)
            self.display_h = int(tile_width * scale)
            
            self.spritesheet = pygame.image.load(path).convert_alpha()
            cols = self.spritesheet.get_width() // tile_width
            rows = self.spritesheet.get_height() // tile_width
            self.frames = {}
            
            # Extract tile frames for the whole sheet
            tile_id = 0
            for row in range(rows):
                for col in range(cols):
                    rect = pygame.Rect(col * tile_width, row * tile_width, 
                                     tile_width, tile_width)
                    frame = self.spritesheet.subsurface(rect)
                    frame = pygame.transform.scale(frame, (self.display_w, self.display_h))
                    self.frames[tile_id] = frame
                    tile_id += 1
        except Exception as e:
            print(f"Could not load tileset: {e}, using placeholder")
            self._create_placeholder_frames()
    
    def get_frame(self, tile_id: int) -> pygame.Surface:
        """Lấy tile surface"""
        return self.frames.get(tile_id, self.frames[0])


class MapData:
    """Lưu trữ dữ liệu bản đồ"""
    
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.data: List[List[int]] = [[0] * cols for _ in range(rows)]
    
    def get(self, x: int, y: int, default: int = 0) -> int:
        """Lấy tile tại vị trí"""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.data[y][x]
        return default
    
    def set(self, x: int, y: int, tile_id: int):
        """Đặt tile tại vị trí"""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.data[y][x] = tile_id
    
    def to_dict(self) -> Dict:
        """Serialize to dict"""
        return {
            'cols': self.cols,
            'rows': self.rows,
            'data': self.data
        }
    
    @staticmethod
    def from_dict(d: Dict) -> 'MapData':
        """Deserialize from dict"""
        m = MapData(d['cols'], d['rows'])
        m.data = d['data']
        return m


class MapGenerator:
    """Tạo map procedurally theo theme"""
    
    @staticmethod
    def generate(cols: int, rows: int, theme: str = "graveyard", 
                 seed: Optional[int] = None) -> MapData:
        """Tạo map mới"""
        if seed is not None:
            random.seed(seed)
        
        m = MapData(cols, rows)
        
        if theme == "dungeon":
            MapGenerator._gen_dungeon(m)
        elif theme == "graveyard":
            MapGenerator._gen_graveyard(m)
        elif theme == "forest":
            MapGenerator._gen_forest(m)
        elif theme == "lava":
            MapGenerator._gen_lava(m)
        elif theme == "icemap":
            MapGenerator._gen_icemap(m)
        elif theme == "naturemap":
            MapGenerator._gen_naturemap(m)
        else:
            MapGenerator._gen_graveyard(m)
        
        return m
    
    @staticmethod
    def _gen_dungeon(m: MapData):
        """Generate dungeon theme"""
        # Fill with ground
        for y in range(m.rows):
            for x in range(m.cols):
                m.set(x, y, Tileset.GROUND)
        
        # Add stone walls around edges
        for x in range(m.cols):
            m.set(x, 0, Tileset.STONE)
            m.set(x, m.rows - 1, Tileset.STONE)
        for y in range(m.rows):
            m.set(0, y, Tileset.STONE)
            m.set(m.cols - 1, y, Tileset.STONE)
        
        # Random interior walls
        for _ in range(m.cols * m.rows // 20):
            x = random.randint(1, m.cols - 2)
            y = random.randint(1, m.rows - 2)
            m.set(x, y, Tileset.WALL)
    
    @staticmethod
    def _gen_graveyard(m: MapData):
        """Generate graveyard theme"""
        # Fill with grass
        for y in range(m.rows):
            for x in range(m.cols):
                m.set(x, y, Tileset.GRASS)
        
        # Add scattered stones
        for _ in range(m.cols * m.rows // 15):
            x = random.randint(0, m.cols - 1)
            y = random.randint(0, m.rows - 1)
            m.set(x, y, Tileset.STONE)
        
        # Patches of dark ground
        for _ in range(5):
            cx = random.randint(2, m.cols - 3)
            cy = random.randint(2, m.rows - 3)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if random.random() < 0.6:
                        m.set(cx + dx, cy + dy, Tileset.GROUND)
    
    @staticmethod
    def _gen_forest(m: MapData):
        """Generate forest theme"""
        # Fill with grass
        for y in range(m.rows):
            for x in range(m.cols):
                m.set(x, y, Tileset.GRASS)
        
        # Random trees/decorations
        for _ in range(m.cols * m.rows // 10):
            x = random.randint(0, m.cols - 1)
            y = random.randint(0, m.rows - 1)
            if random.random() < 0.7:
                m.set(x, y, Tileset.DECORATION)
            else:
                m.set(x, y, Tileset.WALL)
        
        # Water patches
        for _ in range(3):
            cx = random.randint(2, m.cols - 3)
            cy = random.randint(2, m.rows - 3)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if random.random() < 0.4:
                        m.set(cx + dx, cy + dy, Tileset.WATER)
    
    @staticmethod
    def _gen_lava(m: MapData):
        """Generate lava/fire theme using the lava tileset"""
        # Fill with obsidian/lava base
        for y in range(m.rows):
            for x in range(m.cols):
                if random.random() < 0.15:
                    m.set(x, y, Tileset.OBSIDIAN_WALL)
                else:
                    m.set(x, y, Tileset.LAVA_BASE)

        # Add lava rivers and corners
        for x in range(1, m.cols - 1):
            if random.random() < 0.15:
                m.set(x, m.rows // 2, Tileset.LAVA_HOR)
                m.set(x, m.rows // 2 - 1, Tileset.LAVA_HOR)

        for y in range(1, m.rows - 1):
            if random.random() < 0.05:
                m.set(m.cols // 3, y, Tileset.LAVA_VER)
                m.set(m.cols // 3 + 1, y, Tileset.LAVA_VER)

        # Place bridge pieces across lava
        for x in range(3, m.cols - 3, 7):
            m.set(x, m.rows // 2, Tileset.BRIDGE_STRAIGHT)
            m.set(x + 1, m.rows // 2, Tileset.BRIDGE_STRAIGHT)
            m.set(x + 2, m.rows // 2, Tileset.BRIDGE_END)

        # Add detail decoration
        for _ in range(m.cols * m.rows // 30):
            x = random.randint(0, m.cols - 1)
            y = random.randint(0, m.rows - 1)
            tile = random.choice([
                Tileset.LAVA_BUBBLES,
                Tileset.LAVA_RIPPLE,
                Tileset.LAVA_POOL,
                Tileset.CRACK,
                Tileset.OBSIDIAN_FLOW,
            ])
            m.set(x, y, tile)

    @staticmethod
    def _gen_icemap(m: MapData):
        """Generate ice-themed map"""
        for y in range(m.rows):
            for x in range(m.cols):
                if random.random() < 0.12:
                    m.set(x, y, Tileset.STONE)
                else:
                    m.set(x, y, Tileset.WATER)

        # Frozen lakes and cracks
        for _ in range(5):
            cx = random.randint(2, m.cols - 3)
            cy = random.randint(2, m.rows - 3)
            for dx in range(-3, 4):
                for dy in range(-2, 3):
                    if 0 <= cx + dx < m.cols and 0 <= cy + dy < m.rows:
                        if random.random() < 0.7:
                            m.set(cx + dx, cy + dy, Tileset.LAVA_RIPPLE)

        # Ice columns and crystals
        for _ in range(m.cols * m.rows // 25):
            x = random.randint(0, m.cols - 1)
            y = random.randint(0, m.rows - 1)
            if random.random() < 0.5:
                m.set(x, y, Tileset.OBSIDIAN_WALL)
            else:
                m.set(x, y, Tileset.DECORATION)

    @staticmethod
    def _gen_naturemap(m: MapData):
        """Generate nature-themed map"""
        for y in range(m.rows):
            for x in range(m.cols):
                if random.random() < 0.20:
                    m.set(x, y, Tileset.GRASS)
                else:
                    m.set(x, y, Tileset.GROUND)

        for _ in range(m.cols * m.rows // 18):
            x = random.randint(0, m.cols - 1)
            y = random.randint(0, m.rows - 1)
            if random.random() < 0.5:
                m.set(x, y, Tileset.DECORATION)
            else:
                m.set(x, y, Tileset.STONE)

        # Small ponds and streams
        for _ in range(4):
            cx = random.randint(2, m.cols - 3)
            cy = random.randint(2, m.rows - 3)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if 0 <= cx + dx < m.cols and 0 <= cy + dy < m.rows and random.random() < 0.7:
                        m.set(cx + dx, cy + dy, Tileset.WATER)

        # Mossy stone patches
        for _ in range(5):
            cx = random.randint(1, m.cols - 2)
            cy = random.randint(1, m.rows - 2)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if random.random() < 0.8:
                        m.set(cx + dx, cy + dy, Tileset.STONE)


class MapEditor:
    """Editor bản đồ interactiv (F1 toggle)"""
    
    def __init__(self, map_data: MapData, tileset: Tileset, camera: Camera):
        self.map_data = map_data
        self.tileset = tileset
        self.camera = camera
        self.active = False
        self.selected_tile = min(self.tileset.frames.keys()) if self.tileset.frames else Tileset.GROUND
        self.brush_size = 1
    
    def toggle(self):
        """Bật/tắt editor"""
        self.active = not self.active
    
    def handle_event(self, event: pygame.event.Event):
        """Xử lý input editor"""
        if not self.active:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            wx, wy = self.camera.screen_to_world(mx, my)
            tx, ty = wx // self.tileset.display_w, wy // self.tileset.display_h
            
            if event.button == 1:  # Left click = paint
                self.paint(tx, ty, self.selected_tile)
            elif event.button == 3:  # Right click = erase
                self.paint(tx, ty, Tileset.EMPTY)
        
        elif event.type == pygame.MOUSEWHEEL:
            tile_ids = sorted(self.tileset.frames.keys())
            if not tile_ids:
                return
            current_index = tile_ids.index(self.selected_tile) if self.selected_tile in tile_ids else 0
            if event.y > 0:  # Scroll up
                current_index = (current_index + 1) % len(tile_ids)
            else:  # Scroll down
                current_index = (current_index - 1) % len(tile_ids)
            self.selected_tile = tile_ids[current_index]
    
    def paint(self, tx: int, ty: int, tile_id: int):
        """Paint tile"""
        for dx in range(-self.brush_size, self.brush_size + 1):
            for dy in range(-self.brush_size, self.brush_size + 1):
                self.map_data.set(tx + dx, ty + dy, tile_id)
    
    def update(self, mouse_pos: Tuple[int, int]):
        """Update editor state"""
        pass
    
    def draw(self, surf: pygame.Surface):
        """Draw editor UI"""
        if not self.active:
            return
        
        try:
            font = pygame.font.SysFont("segoeui", 14)
        except:
            font = pygame.font.Font(None, 14)
        
        tile_name = self.tileset.TILE_NAMES.get(self.selected_tile, f"Tile {self.selected_tile}")
        info = font.render(
            f"EDITOR ON | Tile: {tile_name} ({self.selected_tile}) | "
            f"Scroll: change | L-Click: paint | R-Click: erase | F1: off",
            True, (200, 200, 100))
        surf.blit(info, (4, surf.get_height() - 22))


class Minimap:
    """Bản đồ thu nhỏ góc màn hình (F3 toggle)"""
    
    def __init__(self, map_data: MapData, width: int = 100, height: int = 80):
        self.map_data = map_data
        self.width = width
        self.height = height
        self.active = True
        self.tile_scale_x = width / map_data.cols
        self.tile_scale_y = height / map_data.rows
    
    def toggle(self):
        self.active = not self.active
    
    def draw(self, surf: pygame.Surface, camera: Optional[Camera] = None):
        """Vẽ minimap ở góc trên phải"""
        if not self.active:
            return
        
        x = surf.get_width() - self.width - 4
        y = 4
        
        # Background
        pygame.draw.rect(surf, (0, 0, 0, 200), 
                        (x, y, self.width, self.height))
        pygame.draw.rect(surf, (100, 100, 100), 
                        (x, y, self.width, self.height), 2)
        
        # Draw tiles
        tile_colors = {
            Tileset.EMPTY: (30, 30, 30),
            Tileset.GROUND: (80, 70, 90),
            Tileset.WALL: (50, 50, 50),
            Tileset.WATER: (50, 100, 150),
            Tileset.GRASS: (100, 150, 80),
            Tileset.STONE: (120, 120, 100),
            Tileset.DECORATION: (180, 120, 80),
            Tileset.LAVA_BASE: (20, 15, 35),
            Tileset.LAVA_HOR: (220, 100, 20),
            Tileset.LAVA_VER: (220, 90, 30),
            Tileset.LAVA_CORNER: (200, 80, 30),
            Tileset.LAVA_CORNER_ALT: (190, 70, 40),
            Tileset.LAVA_BUBBLES: (230, 120, 50),
            Tileset.LAVA_RIPPLE: (240, 130, 60),
            Tileset.BRIDGE_STRAIGHT: (40, 40, 50),
            Tileset.BRIDGE_END: (50, 50, 60),
            Tileset.OBSIDIAN_WALL: (35, 35, 45),
            Tileset.OBSIDIAN_FLOW: (80, 30, 30),
            Tileset.LAVA_POOL: (180, 80, 35),
            Tileset.CRACK: (120, 50, 30),
        }
        
        for ty in range(self.map_data.rows):
            for tx in range(self.map_data.cols):
                tile_id = self.map_data.get(tx, ty)
                color = tile_colors.get(tile_id, (100, 100, 100))
                
                px = x + int(tx * self.tile_scale_x)
                py = y + int(ty * self.tile_scale_y)
                pw = max(1, int(self.tile_scale_x))
                ph = max(1, int(self.tile_scale_y))
                
                pygame.draw.rect(surf, color, (px, py, pw, ph))
        
        # Camera viewport indicator (nếu có camera)
        if camera:
            view_rect = camera.get_rect()
            min_x = x + int(view_rect.x / camera.world_w * self.width)
            min_y = y + int(view_rect.y / camera.world_h * self.height)
            view_w = int(view_rect.width / camera.world_w * self.width)
            view_h = int(view_rect.height / camera.world_h * self.height)
            
            pygame.draw.rect(surf, (200, 200, 50), 
                           (min_x, min_y, view_w, view_h), 2)


class MapManager:
    """Quản lý toàn bộ tilemap system"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_w = screen_width
        self.screen_h = screen_height
        
        self.tileset = Tileset()
        self.map_data: Optional[MapData] = None
        self.camera: Optional[Camera] = None
        self.editor: Optional[MapEditor] = None
        self.minimap: Optional[Minimap] = None
        self.map_image: Optional[pygame.Surface] = None
        
        self.static_background = True  # True = nền tĩnh, False = camera follow
        self.theme = "graveyard"
    
    def load_tileset(self, path: str, tile_w: int = 16, scale: float = 2.0):
        """Load tileset từ file"""
        self.tileset.load_spritesheet(path, tile_width=tile_w, scale=scale)
    
    def load_map_image(self, path: str):
        """Load raw map/background image"""
        try:
            self.map_image = pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"Could not load map image: {e}")
            self.map_image = None

    def generate_map(self, cols: int = 30, rows: int = 20, 
                    theme: str = "graveyard", seed: Optional[int] = None,
                    static_background: bool = True,
                    tileset_path: Optional[str] = None,
                    background_image_path: Optional[str] = None,
                    tile_w: int = 16,
                    scale: float = 1.0):
        """Tạo map mới"""
        self.theme = theme
        self.static_background = static_background
        self.map_image = None
        
        if background_image_path:
            self.load_map_image(background_image_path)
        if tileset_path:
            self.load_tileset(tileset_path, tile_w=tile_w, scale=scale)
        
        self.map_data = MapGenerator.generate(cols, rows, theme, seed)
        
        # Setup camera
        world_w = cols * self.tileset.display_w
        world_h = rows * self.tileset.display_h
        
        self.camera = Camera(world_w, world_h, self.screen_w, self.screen_h,
                           follow_mode=not static_background)
        
        # Setup editor & minimap
        self.editor = MapEditor(self.map_data, self.tileset, self.camera)
        self.minimap = Minimap(self.map_data)
    
    def update(self, player_x: Optional[float] = None, 
               player_y: Optional[float] = None):
        """Cập nhật camera (follow nhân vật nếu non-static)"""
        if self.camera and player_x is not None and player_y is not None:
            self.camera.update(player_x, player_y)
        
        if self.editor:
            self.editor.update(pygame.mouse.get_pos())
    
    def handle_event(self, event: pygame.event.Event):
        """Xử lý input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                if self.editor:
                    self.editor.toggle()
            elif event.key == pygame.K_F3:
                if self.minimap:
                    self.minimap.toggle()
            elif event.key == pygame.K_F2:
                self.save_map("map_edit.json")
        
        if self.editor:
            self.editor.handle_event(event)
    
    def draw(self, surf: pygame.Surface, 
            player_world_pos: Optional[Tuple[float, float]] = None):
        """Vẽ tilemap"""
        if not self.map_data or not self.camera:
            return
        
        if self.map_image:
            bg = self.map_image
            if bg.get_size() != (surf.get_width(), surf.get_height()):
                bg = pygame.transform.smoothscale(bg, (surf.get_width(), surf.get_height()))
            surf.blit(bg, (0, 0))
        else:
            # Get viewport
            view = self.camera.get_rect()
            
            # Draw tiles
            for ty in range(self.map_data.rows):
                for tx in range(self.map_data.cols):
                    tile_id = self.map_data.get(tx, ty)
                    tile_surf = self.tileset.get_frame(tile_id)
                    
                    world_x = tx * self.tileset.display_w
                    world_y = ty * self.tileset.display_h
                    
                    # Cull: chỉ vẽ tile trong viewport
                    if not (world_x + self.tileset.display_w > view.left and 
                           world_x < view.right and
                           world_y + self.tileset.display_h > view.top and
                           world_y < view.bottom):
                        continue
                    
                    screen_x, screen_y = self.camera.world_to_screen(world_x, world_y)
                    surf.blit(tile_surf, (screen_x, screen_y))
        
        # Draw editor UI
        if self.editor:
            self.editor.draw(surf)
        
        # Draw minimap
        if self.minimap:
            self.minimap.draw(surf, self.camera)
    
    def save_map(self, filename: str):
        """Lưu map ra JSON"""
        if not self.map_data:
            return
        
        data = {
            'theme': self.theme,
            'map': self.map_data.to_dict()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Map saved to {filename}")
        except Exception as e:
            print(f"Could not save map: {e}")

    def save_map_image(self, filename: str):
        """Render current map to image file"""
        if not self.map_data:
            return

        if not pygame.get_init():
            pygame.init()

        world_w = self.map_data.cols * self.tileset.display_w
        world_h = self.map_data.rows * self.tileset.display_h
        surf = pygame.Surface((world_w, world_h), pygame.SRCALPHA)

        for ty in range(self.map_data.rows):
            for tx in range(self.map_data.cols):
                tile_id = self.map_data.get(tx, ty)
                tile_surf = self.tileset.get_frame(tile_id)
                surf.blit(tile_surf, (tx * self.tileset.display_w, ty * self.tileset.display_h))

        try:
            pygame.image.save(surf, filename)
            print(f"Map image saved to {filename}")
        except Exception as e:
            print(f"Could not save map image: {e}")

    def load_map(self, filename: str):
        """Load map từ JSON"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.theme = data.get('theme', 'graveyard')
            self.map_data = MapData.from_dict(data['map'])
            
            # Setup camera & tools
            world_w = self.map_data.cols * self.tileset.display_w
            world_h = self.map_data.rows * self.tileset.display_h
            self.camera = Camera(world_w, world_h, self.screen_w, self.screen_h,
                               follow_mode=not self.static_background)
            self.editor = MapEditor(self.map_data, self.tileset, self.camera)
            self.minimap = Minimap(self.map_data)
            
            print(f"Map loaded from {filename}")
        except Exception as e:
            print(f"Could not load map: {e}")


if __name__ == "__main__":
    # Run standalone demo
    import sys
    
    pygame.init()
    SW, SH = 480, 820
    screen = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption("Tilemap Demo — F1:Editor  F3:Minimap  T:Theme  ESC:Thoát")
    clock = pygame.time.Clock()

    mm = MapManager(SW, SH)
    mm.generate_map(theme="graveyard", static_background=False, cols=50, rows=35)

    try:
        font = pygame.font.SysFont("segoeui", 18, bold=True)
    except:
        font = pygame.font.Font(None, 22)

    player_x, player_y = SW / 2, SH / 2
    speed = 3
    theme_idx = 0
    THEMES = ["dungeon", "graveyard", "forest", "lava"]

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_t:
                    theme_idx = (theme_idx + 1) % len(THEMES)
                    mm.generate_map(theme=THEMES[theme_idx], 
                                  static_background=False, cols=50, rows=35)
            mm.handle_event(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += speed

        mm.update(player_x, player_y)

        screen.fill((10, 5, 20))
        mm.draw(screen, player_world_pos=(player_x, player_y))

        # Player indicator
        cam = mm.camera
        if cam:
            sx, sy = cam.world_to_screen(player_x, player_y)
        else:
            sx, sy = int(player_x), int(player_y)
        pygame.draw.circle(screen, (255, 80, 80), (sx, sy), 10)
        pygame.draw.circle(screen, (255, 200, 200), (sx, sy), 10, 2)

        # HUD
        info = font.render(
            f"WASD: move | T: theme ({THEMES[theme_idx]}) | F1: Editor | F2: Save",
            True, (200, 200, 255))
        screen.blit(info, (8, 8))

        pygame.display.flip()

    pygame.quit()
    sys.exit()
