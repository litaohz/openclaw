from PIL import Image

img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\article_cropped.png")

# Find where action bar ends by looking for the row that's mostly white
# Action bar has icons, below it should be divider line, then white space, then next content

for y in range(580, 660, 5):
    row_pixels = [img.getpixel((x, y)) for x in range(0, 560, 50)]
    avg_brightness = sum(sum(p) for p in row_pixels) / (len(row_pixels) * 3)
    non_white = sum(1 for p in row_pixels if p[0] < 250 or p[1] < 250 or p[2] < 250)
    print(f"y={y}: avg_brightness={avg_brightness:.0f}, non_white_count={non_white}")
