from PIL import Image

# Check the viewport_crop.png we created earlier
img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\viewport_crop.png")
print(f"viewport_crop.png size: {img.width}x{img.height}")

# Check bottom area
print("\\nBottom pixels at x=280 (center):")
for y in range(img.height - 30, img.height, 2):
    pixel = img.getpixel((280, y))
    print(f"y={y}: {pixel}")

# Check what the bottom 20 rows look like
print("\\nAverage brightness of bottom rows:")
for y in range(img.height - 20, img.height, 2):
    row_avg = sum(sum(img.getpixel((x, y))) for x in range(0, 560, 20)) / (28 * 3)
    print(f"y={y}: avg={row_avg:.0f}")
