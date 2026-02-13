from playwright.sync_api import sync_playwright
from PIL import Image

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
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    avatar = article.locator('[data-testid="Tweet-User-Avatar"]').first
    av_box = avatar.bounding_box()
    
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    page.screenshot(path="temp.png")
    img = Image.open("temp.png")
    
    # VERY tight crop - stop at y=700 (before action bar!)
    left = int(av_box['x']) - 3
    top = int(art_box['y']) - 5
    right = int(ab_box['x'] + ab_box['width']) + 3
    bottom = 700  # Hard-coded to before action bar
    
    print(f"Crop: L={left}, T={top}, R={right}, B={bottom}")
    print(f"Viewport image size: {img.width}x{img.height}")
    
    cropped = img.crop((left, top, right, bottom))
    print(f"After crop: {cropped.width}x{cropped.height}")
    
    # DON'T resize - keep original pixel dimensions
    output = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\y700_noresize.png"
    cropped.save(output, optimize=True)
    
    print(f"Saved without resize: {cropped.width}x{cropped.height}")
    page.close()
