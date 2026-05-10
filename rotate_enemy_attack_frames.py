from PIL import Image
import os

# Rotate enemy attack frames 90 degrees clockwise to face downward
frame_dir = 'assets/enemy_frames_attack'
for i in range(6):
    frame_path = os.path.join(frame_dir, f'enemy_attack_frame_{i}.png')
    img = Image.open(frame_path)
    rotated = img.rotate(-90, expand=True)  # Rotate 90 degrees clockwise, expand to fit
    rotated.save(frame_path)
    print(f'Rotated {frame_path}')

# Regenerate spritesheet
from combine_enemy_attack_sheet import *  # Import to run the combine script
print("Frames rotated and spritesheet regenerated.")