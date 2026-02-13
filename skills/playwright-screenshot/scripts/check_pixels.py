from PIL import Image

img = Image.open("debug_cropped.png")
print(f"Size: {img.width}x{img.height}")

# Check right edge pixels - if there's sidebar content, right edge won't be white/light
# Sample some pixels from the right edge
right_edge_x = img.width - 10
for y in [100, 200, 300, 400, 500]:
    if y < img.height:
        pixel = img.getpixel((right_edge_x, y))
        print(f"Pixel at ({right_edge_x}, {y}): {pixel}")
