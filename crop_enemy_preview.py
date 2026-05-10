"""
Crop enemy spritesheet into individual frames
Similar to crop_kiemkhi_preview.py for player
"""
from PIL import Image
import os

# Ensure debug_frames directory exists
os.makedirs('debug_frames', exist_ok=True)

# Load enemy image
img = Image.open('assets/enemy (2).png')
print(f'Enemy image size: {img.size}')

w, h = img.size

# If it's a horizontal spritesheet, divide into equal parts
# Try common frame counts: 2, 3, 4, 6, 8
frame_counts_to_try = [2, 3, 4, 6, 8]

for frame_count in frame_counts_to_try:
    frame_width = w // frame_count
    print(f"\n--- Testing {frame_count} frames ({frame_width}x{h} each) ---")
    
    for i in range(frame_count):
        x1 = i * frame_width
        crop = img.crop((x1, 0, x1 + frame_width, h))
        crop.save(f'debug_frames/enemy_frame_{frame_count}x_{i}.png')
        print(f"Frame {i}: {crop.size}")
