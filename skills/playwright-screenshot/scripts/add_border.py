from PIL import Image, ImageDraw

# Load the cropped image
img = Image.open(r'C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\test-v12.png')
print(f'Size: {img.width}x{img.height}')

# Add a thick red border to verify boundaries
draw = ImageDraw.Draw(img)
draw.rectangle([0, 0, img.width-1, img.height-1], outline='red', width=5)
draw.text((10, 10), f'{img.width}x{img.height}', fill='red')

img.save(r'C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\bordered_test.png')
print('Saved with red border')
