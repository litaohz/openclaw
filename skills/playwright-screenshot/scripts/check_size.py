from PIL import Image

img = Image.open("debug_cropped.png")
print(f"debug_cropped.png: {img.width}x{img.height}")

img2 = Image.open("debug_full.png")
print(f"debug_full.png: {img2.width}x{img2.height}")
