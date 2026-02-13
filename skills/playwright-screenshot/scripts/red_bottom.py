from PIL import Image, ImageDraw

img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\fixed_left.png")
print(f"Size: {img.width}x{img.height}")

draw = ImageDraw.Draw(img)
# Paint bottom 80px solid red
draw.rectangle([0, img.height - 80, img.width, img.height], fill='red')
draw.text((200, img.height - 60), f"BOTTOM MARKER", fill='white')
draw.text((180, img.height - 40), f"Image height = {img.height}", fill='white')

img.save(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\red_bottom.png")
print("Saved with red bottom")
