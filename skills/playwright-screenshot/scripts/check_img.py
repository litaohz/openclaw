from PIL import Image

# Load the cropped image
img = Image.open(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\test-xai-v5.png")
print(f"Image size: {img.width}x{img.height}")

# The sidebar content should NOT be in a 560px wide image if we cropped correctly
# Let's check what's at the right edge
print("Right edge should be clean (no sidebar)")
