from PIL import Image

# Check the temp.png (viewport screenshot)
img = Image.open("temp.png")
print(f"Viewport: {img.width}x{img.height}")

# Check pixels around y=700 at x=500 (middle of content)
print("\\nPixels at x=500 (content area):")
for y in range(690, 720, 2):
    pixel = img.getpixel((500, y))
    print(f"y={y}: {pixel}")

print("\\nPixels at x=700 (action bar area):")
for y in range(690, 720, 2):
    pixel = img.getpixel((700, y))
    print(f"y={y}: {pixel}")
