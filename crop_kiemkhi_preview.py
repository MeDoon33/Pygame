from PIL import Image
img = Image.open('assets/kiemkhi.png')
print('size', img.size)
w, h = img.size
crops = [
    (0, 0, w//3, h),
    (w//3, 0, 2*w//3, h),
    (2*w//3, 0, w, h),
    (0, 0, w, h//2),
    (0, h//2, w, h)
]
for i, box in enumerate(crops):
    crop = img.crop(box)
    crop.save(f'debug_frames/kiemkhi_crop{i}.png')
    print(i, box, crop.size)