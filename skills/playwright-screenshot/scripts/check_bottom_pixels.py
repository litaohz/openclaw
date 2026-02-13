from PIL import Image

img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\article_cropped.png")
print(f"Size: {img.width}x{img.height}")

# Check pixels at the bottom
for y in [640, 645, 650, 654]:
    # Sample across the row
    pixels = [img.getpixel((x, y)) for x in [50, 280, 500]]
    print(f"y={y}: {pixels}")
