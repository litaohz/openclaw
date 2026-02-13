from PIL import Image, ImageDraw

# Create exact size image
img = Image.new('RGB', (560, 500), color='#1da1f2')  # Twitter blue
draw = ImageDraw.Draw(img)

# Draw border
draw.rectangle([0, 0, 559, 499], outline='white', width=3)

# Add size text
draw.text((200, 230), "560 x 500", fill='white')
draw.text((180, 260), "EXACT SIZE TEST", fill='white')

# Draw lines at specific Y positions
for y in [100, 200, 300, 400, 490]:
    draw.line([(0, y), (560, y)], fill='yellow', width=1)
    draw.text((10, y-15), f"y={y}", fill='yellow')

output = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\size_test_560x500.png"
img.save(output)

# Verify
check = Image.open(output)
print(f"Saved and verified: {check.width}x{check.height}")
