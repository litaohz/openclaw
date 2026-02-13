from PIL import Image
import random

# Load the test_crop_result.png
img = Image.open("test_crop_result.png")
print(f"Original: {img.width}x{img.height}, mode={img.mode}")

# Create a NEW image and paste content into it
new_img = Image.new('RGB', (img.width, img.height), color='white')
new_img.paste(img, (0, 0))

# Verify dimensions
print(f"New image: {new_img.width}x{new_img.height}")

# Add a red bar at the very bottom to mark the edge
from PIL import ImageDraw
draw = ImageDraw.Draw(new_img)
draw.rectangle([0, new_img.height - 10, new_img.width, new_img.height], fill='red')
draw.text((200, new_img.height - 10), "BOTTOM EDGE", fill='white')

rand = random.randint(1000, 9999)
output = f"C:\\Users\\taoli1\\.openclaw\\workspace\\ai-news\\screenshots\\2026-02-12\\repaste_{rand}.png"
new_img.save(output, 'PNG')

# Verify file
check = Image.open(output)
print(f"Saved and verified: {check.width}x{check.height}")

# Check bottom pixels
for y in range(check.height - 15, check.height):
    pixel = check.getpixel((check.width // 2, y))
    is_red = pixel[0] > 200 and pixel[1] < 100
    print(f"y={y}: {pixel} {'(RED)' if is_red else ''}")
