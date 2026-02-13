from PIL import Image

# Load the marked full image
img = Image.open("marked_full.png")
print(f"Original: {img.width}x{img.height}")

# Crop (425, 47, 1000, 763)
left, top, right, bottom = 425, 47, 1000, 763
print(f"Crop box: L={left}, T={top}, R={right}, B={bottom}")
print(f"Expected size: {right-left}x{bottom-top}")

cropped = img.crop((left, top, right, bottom))
print(f"Actual cropped size: {cropped.width}x{cropped.height}")

# Save
cropped.save("test_crop_result.png")

# Check what's at the bottom of the cropped image
print("\\nBottom pixels of cropped image:")
for y in range(cropped.height - 30, cropped.height, 5):
    # Check for blue pixels (the CROP_LINE)
    row = [cropped.getpixel((x, y)) for x in range(0, cropped.width, 50)]
    has_blue = any(p[2] > 200 and p[0] < 100 and p[1] < 100 for p in row)
    print(f"y={y}: has_blue={has_blue}, sample={row[0]}")
