from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

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
    
    # Get coordinates
    article = page.locator('article').first
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    like_btn = article.locator('[data-testid="like"]').first
    like_box = like_btn.bounding_box()
    
    print(f"Action bar: y={ab_box['y']:.1f} to {ab_box['y']+ab_box['height']:.1f}")
    print(f"Like button: y={like_box['y']:.1f} to {like_box['y']+like_box['height']:.1f}")
    
    # Screenshot
    page.screenshot(path="precision_test.png", full_page=False)
    
    img = Image.open("precision_test.png")
    draw = ImageDraw.Draw(img)
    
    # Draw lines at key Y positions
    for y, color, label in [
        (int(ab_box['y']), 'green', 'action_bar_top'),
        (int(ab_box['y'] + ab_box['height']), 'red', 'action_bar_bottom'),
        (int(like_box['y']), 'blue', 'like_top'),
        (int(like_box['y'] + like_box['height']), 'cyan', 'like_bottom'),
    ]:
        draw.line([(400, y), (1000, y)], fill=color, width=2)
        draw.text((1010, y-10), f"{label}={y}", fill=color)
    
    # Crop to show this area
    section = img.crop((400, 680, 1100, 800))
    section.save(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\precision_lines.png")
    print("Saved precision_lines.png")
    
    page.close()
