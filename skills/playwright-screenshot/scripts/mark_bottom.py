from PIL import Image, ImageDraw

# Load the cropped image
img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\article_cropped.png")
print(f"Image size: {img.width}x{img.height}")

# Draw a red line at the bottom
draw = ImageDraw.Draw(img)
draw.line([(0, img.height-5), (img.width, img.height-5)], fill='red', width=3)
draw.text((10, img.height-25), f"Bottom edge: {img.height}px", fill='red')

# Also draw at y=600 to see where that is
draw.line([(0, 600), (img.width, 600)], fill='blue', width=2)
draw.text((10, 575), "y=600", fill='blue')

img.save(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\marked_bottom.png")
print("Saved with markers")
