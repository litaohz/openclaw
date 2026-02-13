from PIL import Image

# Check the cropped image
img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\y700_noresize.png")
print(f"Cropped: {img.width}x{img.height}")

# Check bottom area
print("\\nBottom pixels at x=280 (center):")
for y in range(img.height - 30, img.height, 2):
    pixel = img.getpixel((280, y))
    print(f"y={y}: {pixel}")

# Check where action bar icons would be (dark pixels)
print("\\nScanning for non-white rows:")
for y in range(img.height - 100, img.height, 5):
    row = [img.getpixel((x, y)) for x in range(0, img.width, 50)]
    non_white = sum(1 for p in row if p[0] < 240 or p[1] < 240 or p[2] < 240)
    if non_white > 0:
        print(f"y={y}: {non_white} non-white pixels")
