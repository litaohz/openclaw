from PIL import Image, ImageDraw

# Create a simple test image - solid color with text
img = Image.new('RGB', (560, 400), color='#7c3aed')  # Purple
draw = ImageDraw.Draw(img)
draw.text((150, 180), "TEST IMAGE", fill='white')
draw.text((120, 220), "560 x 400 pixels", fill='white')
draw.text((140, 260), "No sidebar!", fill='yellow')

img.save(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\test-solid.png")
print("Saved test-solid.png")
