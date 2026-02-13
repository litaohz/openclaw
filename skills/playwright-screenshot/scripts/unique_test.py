from PIL import Image, ImageDraw
import random

# Create a unique filename
rand = random.randint(10000, 99999)
filename = f"unique_test_{rand}.png"

# Create a simple test image
img = Image.new('RGB', (560, 400), color='#00ff00')  # Bright green
draw = ImageDraw.Draw(img)
draw.rectangle([10, 10, 550, 390], outline='black', width=3)
draw.text((180, 180), f"TEST #{rand}", fill='black')
draw.text((150, 220), "This should be GREEN", fill='black')
draw.text((140, 260), "with BLACK border only", fill='black')

output = f"C:\\Users\\taoli1\\.openclaw\\workspace\\ai-news\\screenshots\\2026-02-12\\{filename}"
img.save(output)
print(f"Saved: {filename}")
print(f"Full path: {output}")
