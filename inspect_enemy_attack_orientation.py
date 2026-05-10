from PIL import Image
import os

frame_dir = 'assets/enemy_frames_attack'
for i in range(6):
    frame_path = os.path.join(frame_dir, f'enemy_attack_frame_{i}.png')
    img = Image.open(frame_path)
    print(frame_path, img.size)
    for ang in [0, 90, -90, 180]:
        out = img.rotate(ang, expand=True)
        out.save(os.path.join('debug_frames', f'attack_frame_{i}_rot{ang}.png'))
print('Generated rotated debug frames for inspection')
