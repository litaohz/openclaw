from PIL import Image
img = Image.open(r'C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\test-v12.png')
print(f'Actual file size: {img.width}x{img.height}')

# Check right edge pixels
for y in [100, 300, 500]:
    pixel = img.getpixel((img.width - 5, y))
    print(f'Right edge pixel at y={y}: {pixel}')
