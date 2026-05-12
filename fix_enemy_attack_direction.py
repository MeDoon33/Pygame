#!/usr/bin/env python3
"""
Công cụ để điều chỉnh hướng hoạt ảnh tấn công của quái vật
Cho phép thử nghiệm 4 hướng khác nhau
"""
from PIL import Image
import os

def create_attack_animation(rotation_angle, flip_horizontal=False, flip_vertical=False, name=""):
    """Tạo spritesheet tấn công với các tùy chọn transform"""
    
    # Load original
    img = Image.open('assets/enemy_attack.png')
    w, h = img.size
    frame_width = w // 6
    
    frames_transformed = []
    for i in range(1, 5):  # Frames 1-4
        x1 = i * frame_width
        frame = img.crop((x1, 0, x1 + frame_width, h))
        
        # Apply rotations and flips
        if rotation_angle != 0:
            frame = frame.rotate(rotation_angle, expand=True)
        if flip_horizontal:
            frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
        if flip_vertical:
            frame = frame.transpose(Image.FLIP_TOP_BOTTOM)
        
        frames_transformed.append(frame)
    
    # Pad to uniform size
    max_w = max(f.width for f in frames_transformed)
    max_h = max(f.height for f in frames_transformed)
    
    uniform_frames = []
    for f in frames_transformed:
        uniform = Image.new('RGBA', (max_w, max_h), (0, 0, 0, 0))
        x_offset = (max_w - f.width) // 2
        y_offset = (max_h - f.height) // 2
        uniform.paste(f, (x_offset, y_offset), f)
        uniform_frames.append(uniform)
    
    # Create spritesheet
    new_width = max_w * 4
    new_height = max_h
    new_sheet = Image.new('RGBA', (new_width, new_height))
    
    for i, frame in enumerate(uniform_frames):
        new_sheet.paste(frame, (i * max_w, 0))
    
    # Save
    output_name = f'assets/enemy_attack_4frame{"_" + name if name else ""}.png'
    new_sheet.save(output_name)
    print(f'✓ Saved: {output_name} ({new_sheet.size})')
    print(f'  Rotation: {rotation_angle}°, Flip H: {flip_horizontal}, Flip V: {flip_vertical}')
    
    # Save preview
    os.makedirs('debug_frames', exist_ok=True)
    for i, frame in enumerate(uniform_frames):
        frame.save(f'debug_frames/test_{name}_f{i}.png')

if __name__ == '__main__':
    print('Generating attack animation variants...\n')
    
    # Option 1: Current (rotate 90 CCW)
    create_attack_animation(rotation_angle=90, flip_horizontal=False, flip_vertical=False, name='90ccw')
    
    # Option 2: Rotate 90 CCW + Flip Horizontal
    create_attack_animation(rotation_angle=90, flip_horizontal=True, flip_vertical=False, name='90ccw_fliph')
    
    # Option 3: Rotate 90 CW (opposite of current)
    create_attack_animation(rotation_angle=-90, flip_horizontal=False, flip_vertical=False, name='90cw')
    
    # Option 4: Rotate 90 CW + Flip Horizontal
    create_attack_animation(rotation_angle=-90, flip_horizontal=True, flip_vertical=False, name='90cw_fliph')
    
    print('\n' + '='*60)
    print('Generated 4 variants in assets/:')
    print('1. enemy_attack_4frame_90ccw.png (current)')
    print('2. enemy_attack_4frame_90ccw_fliph.png')
    print('3. enemy_attack_4frame_90cw.png')
    print('4. enemy_attack_4frame_90cw_fliph.png')
    print('\nCheck debug_frames/test_*.png to see which looks correct')
    print('\nThen rename the correct one to: enemy_attack_4frame.png')
    print('='*60)
