from playwright.sync_api import sync_playwright
from PIL import Image
import random

CDP_URL = "http://localhost:9222"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0]
    page = context.new_page()
    page.set_viewport_size({"width": 1400, "height": 2000})
    
    url = "https://x.com/xai/status/2021667200885829667"
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector('article', timeout=15000)
    page.wait_for_timeout(3500)
    
    page.evaluate('document.querySelector(\"[data-testid=sidebarColumn]\").style.display=\"none\"')
    page.wait_for_timeout(500)
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    avatar = article.locator('[data-testid="Tweet-User-Avatar"]').first
    av_box = avatar.bounding_box()
    
    page.screenshot(path="scan.png")
    img = Image.open("scan.png")
    
    # Scan to find where content ACTUALLY ends
    # Start from y=700 and find the last row with significant non-white content
    print("Scanning for content end:")
    last_content_y = 700
    for y in range(700, 900, 2):
        # Sample pixels across the tweet area (x=430-700)
        row = [img.getpixel((x, y)) for x in range(430, 700, 10)]
        non_white = sum(1 for p in row if any(c < 230 for c in p))
        if non_white >= 3:  # Significant content
            last_content_y = y
            print(f"y={y}: {non_white} content pixels")
    
    print(f"\\nLast significant content at y={last_content_y}")
    
    # Crop: use avatar left, and stop at last_content_y
    left = int(av_box['x']) - 3
    top = int(art_box['y']) - 5
    right = 1000  # Wide enough
    
    # Find the action bar's VISUAL bottom by looking for the last row with icon pixels
    # Icons are gray (around 100-150 brightness)
    action_bar_visual_end = 700
    for y in range(720, 770, 2):
        row = [img.getpixel((x, y)) for x in range(450, 900, 20)]
        has_icons = any(100 < min(p) < 200 for p in row)
        if has_icons:
            action_bar_visual_end = y
            
    print(f"Action bar visual end: {action_bar_visual_end}")
    
    # Set bottom to just after action bar icons end
    bottom = action_bar_visual_end + 5
    
    print(f"\\nFinal crop: L={left}, T={top}, R={right}, B={bottom}")
    
    cropped = img.crop((left, top, right, bottom))
    
    # Resize
    target_width = 560
    ratio = target_width / cropped.width
    final = cropped.resize((target_width, int(cropped.height * ratio)), Image.Resampling.LANCZOS)
    
    rand = random.randint(1000, 9999)
    output = f"C:\\Users\\taoli1\\.openclaw\\workspace\\ai-news\\screenshots\\2026-02-12\\scan_{rand}.png"
    final.save(output, optimize=True)
    
    print(f"\\nSaved: scan_{rand}.png ({final.width}x{final.height})")
    page.close()
