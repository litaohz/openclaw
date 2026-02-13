from PIL import Image

img = Image.open("marked_full.png")
print(f"Size: {img.width}x{img.height}")

# Check what's at y=0 (should be top of page - navigation bar area)
print("\\nPixels at y=0-10 (should be top of page):")
for y in range(0, 20, 5):
    pixel = img.getpixel((100, y))
    print(f"y={y}: {pixel}")

# Check what's at y=50 (should be near tweet header)
print("\\nPixels at y=50-60:")
for y in range(50, 70, 5):
    pixel = img.getpixel((300, y))
    print(f"y={y}: {pixel}")

# Check y=700-760 area
print("\\nPixels at y=700-760 (action bar area):")
for y in range(700, 770, 10):
    pixel = img.getpixel((500, y))
    print(f"y={y}: {pixel}")
