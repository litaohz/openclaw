from PIL import Image

img = Image.open("test_crop_result.png")
print(f"Cropped image: {img.width}x{img.height}")

# The blue line was drawn at y=763 in the original
# After cropping with top=47, it should be at y=763-47=716
# But our image height is 716, so the line is AT the edge

# Check if there's any blue at y=715 (last row)
print("\\nChecking last few rows for blue line:")
for y in [713, 714, 715]:
    row = [img.getpixel((x, y)) for x in range(0, img.width, 30)]
    blues = [p for p in row if p[2] > 200]
    print(f"y={y}: {len(blues)} blue pixels, samples: {row[:3]}")

# The CROP_LINE was at y=763, which after top=47 offset = y=716
# But image height is 716, so y=716 is OUT OF BOUNDS
# Last valid y is 715

print("\\nImage height is 716, so y=716 (the CROP_LINE) is outside the image")
print("This is correct - the blue line should be exactly at the crop boundary")
