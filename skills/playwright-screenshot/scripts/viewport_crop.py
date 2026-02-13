from playwright.sync_api import sync_playwright
from PIL import Image
import os

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
    
    # Hide sidebar
    page.evaluate('document.querySelector(\"[data-testid=sidebarColumn]\").style.display=\"none\"')
    page.wait_for_timeout(300)
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    # KEY: Use absolute page coordinates, NOT article-relative
    # Crop from article top to action bar bottom
    top = int(art_box['y']) - 5
    bottom = int(ab_box['y'] + ab_box['height'])  # EXACT action bar bottom
    left = int(art_box['x']) - 5
    right = int(ab_box['x'] + ab_box['width']) + 5
    
    print(f"Page coords - Top:{top}, Bottom:{bottom}, Left:{left}, Right:{right}")
    print(f"Height will be: {bottom - top}")
    
    # Take VIEWPORT screenshot (not full page, not element)
    temp = "viewport_temp.png"
    page.screenshot(path=temp, full_page=False)
    
    img = Image.open(temp)
    print(f"Viewport: {img.width}x{img.height}")
    
    # Crop using page coordinates
    cropped = img.crop((left, top, right, bottom))
    print(f"Cropped: {cropped.width}x{cropped.height}")
    
    # Resize
    target_width = 560
    ratio = target_width / cropped.width
    final = cropped.resize((target_width, int(cropped.height * ratio)), Image.Resampling.LANCZOS)
    
    output = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\viewport_crop.png"
    final.save(output, optimize=True)
    os.remove(temp)
    
    print(f"Final: {final.width}x{final.height}")
    
    # VERIFY by checking bottom pixels
    for y in [final.height - 20, final.height - 10, final.height - 5]:
        pixels = [final.getpixel((x, y)) for x in [50, 280, 500]]
        avg = sum(sum(p) for p in pixels) / 9
        print(f"y={y}: avg_brightness={avg:.0f}")
    
    page.close()
