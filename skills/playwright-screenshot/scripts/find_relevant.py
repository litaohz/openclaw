from PIL import Image

img = Image.open("temp.png")

# Scan a wider area to find "Relevant" text
print("Scanning y=755-800 for non-white pixels:")
for y in range(755, 810, 3):
    row = [img.getpixel((x, y)) for x in range(400, 1000, 20)]
    non_white = sum(1 for p in row if any(c < 240 for c in p))
    if non_white > 0:
        print(f"y={y}: {non_white} non-white pixels")
        
print("\\n--- Checking specific x positions at y=760-780 ---")
for x in [430, 450, 500, 550, 600, 700, 800]:
    pixels = [img.getpixel((x, y)) for y in range(760, 790, 5)]
    has_dark = any(any(c < 200 for c in p) for p in pixels)
    if has_dark:
        print(f"x={x}: has dark pixels in y=760-790")
