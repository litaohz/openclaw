from PIL import Image, ImageDraw
import random

# Load the cropped screenshot
img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\y700_noresize.png")
print(f"Size: {img.width}x{img.height}")

# Create a composite: original image with markers
draw = ImageDraw.Draw(img)

# Draw horizontal lines every 100px
for y in range(0, img.height, 100):
    draw.line([(0, y), (img.width, y)], fill='red', width=1)
    draw.text((5, y+2), f"y={y}", fill='red')

# Draw vertical lines every 100px  
for x in range(0, img.width, 100):
    draw.line([(x, 0), (x, img.height)], fill='blue', width=1)
    draw.text((x+2, 5), f"x={x}", fill='blue')

# Add size info at top
draw.rectangle([150, 20, 420, 50], fill='yellow')
draw.text((160, 25), f"ACTUAL SIZE: {img.width}x{img.height}", fill='black')

rand = random.randint(1000, 9999)
output = f"C:\\Users\\taoli1\\.openclaw\\workspace\\ai-news\\screenshots\\2026-02-12\\grid_{rand}.png"
img.save(output)
print(f"Saved: grid_{rand}.png")
