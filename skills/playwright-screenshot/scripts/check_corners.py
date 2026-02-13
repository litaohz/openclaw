from PIL import Image

img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\viewport_crop.png")

# Check left side at bottom
print("Bottom-left corner (x=0-100):")
for y in range(img.height - 30, img.height, 3):
    pixels = [img.getpixel((x, y)) for x in range(0, 100, 10)]
    non_white = sum(1 for p in pixels if p[0] < 250 or p[1] < 250 or p[2] < 250)
    print(f"y={y}: non_white={non_white}/10, first_pixel={pixels[0]}")

print("\\nBottom-right corner (x=460-560):")
for y in range(img.height - 30, img.height, 3):
    pixels = [img.getpixel((x, y)) for x in range(460, 560, 10)]
    non_white = sum(1 for p in pixels if p[0] < 250 or p[1] < 250 or p[2] < 250)
    print(f"y={y}: non_white={non_white}/10, last_pixel={pixels[-1]}")
