from PIL import Image

# Load the temp file before it was deleted
# Let's create a new test
img = Image.new('RGB', (1400, 2000), color='white')

# Draw a red rectangle at the crop area
from PIL import ImageDraw
draw = ImageDraw.Draw(img)
draw.rectangle([423, 47, 995, 753], outline='red', width=3)
draw.text((500, 400), "CROP AREA", fill='red')

img.save("test_crop_area.png")

# Now crop it
cropped = img.crop((423, 47, 995, 753))
cropped.save("test_cropped_result.png")
print(f"Original: {img.width}x{img.height}")
print(f"Cropped: {cropped.width}x{cropped.height}")
print(f"Expected: {995-423}x{753-47} = 572x706")
