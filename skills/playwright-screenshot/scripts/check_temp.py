from PIL import Image

img = Image.open("temp.png")
print(f"temp.png size: {img.width}x{img.height}")

# Check what's at y=745-760 around x=600
print("\\nPixels at x=600:")
for y in range(740, 770, 2):
    pixel = img.getpixel((600, y))
    is_white = all(p > 250 for p in pixel)
    print(f"y={y}: {pixel} {'(white)' if is_white else ''}")

# Also check where "Relevant" text might be (it has dark pixels)
print("\\nLooking for dark pixels (text) at x=450:")
for y in range(755, 775, 2):
    pixel = img.getpixel((450, y))
    is_dark = any(p < 100 for p in pixel)
    print(f"y={y}: {pixel} {'(dark/text)' if is_dark else ''}")
