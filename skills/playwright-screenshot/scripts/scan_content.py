from PIL import Image

img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\correct_3905.png")
print(f"File size: {img.width}x{img.height}")

# Find where content ends by scanning for mostly-white rows
print("\\nScanning for content rows from bottom:")
for y in range(img.height - 1, img.height - 100, -5):
    row = [img.getpixel((x, y)) for x in range(0, img.width, 30)]
    non_white = sum(1 for p in row if p[0] < 240 or p[1] < 240 or p[2] < 240)
    avg_r = sum(p[0] for p in row) / len(row)
    print(f"y={y}: non_white={non_white}, avg_red={avg_r:.0f}")
