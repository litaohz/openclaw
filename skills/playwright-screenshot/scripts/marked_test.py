from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
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
    
    # Get action bar position
    article = page.locator('article').first
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    # Take screenshot
    page.screenshot(path="marked.png")
    
    img = Image.open("marked.png")
    draw = ImageDraw.Draw(img)
    
    # Draw horizontal lines at key Y positions
    lines = [
        (int(ab_box['y']), 'green', 'AB_TOP'),
        (int(ab_box['y'] + ab_box['height']), 'red', 'AB_BOTTOM'),
        (763, 'blue', 'CROP_LINE'),
    ]
    
    for y, color, label in lines:
        draw.line([(0, y), (1400, y)], fill=color, width=3)
        draw.text((10, y - 20), f"{label} y={y}", fill=color)
    
    # Save full screenshot with marks
    img.save("marked_full.png")
    
    # Now crop at y=763 and see what we get
    cropped = img.crop((425, 47, 1000, 763))
    
    rand = random.randint(1000, 9999)
    output = f"C:\\Users\\taoli1\\.openclaw\\workspace\\ai-news\\screenshots\\2026-02-12\\marked_{rand}.png"
    cropped.save(output)
    
    print(f"Saved marked_{rand}.png ({cropped.width}x{cropped.height})")
    print(f"Action bar: y={ab_box['y']:.0f} to {ab_box['y']+ab_box['height']:.0f}")
    page.close()
