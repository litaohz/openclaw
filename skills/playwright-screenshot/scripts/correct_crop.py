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
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    # Get Time element - this is the last row we want to include
    time_el = page.locator('time').first
    time_box = time_el.bounding_box()
    
    # Get Views text
    views = page.locator('text=/Views|意见/').first
    views_box = views.bounding_box() if views.count() > 0 else None
    
    avatar = article.locator('[data-testid="Tweet-User-Avatar"]').first
    av_box = avatar.bounding_box()
    
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    print(f"Article: y={art_box['y']:.0f} to {art_box['y']+art_box['height']:.0f}")
    print(f"Time: y={time_box['y']:.0f} to {time_box['y']+time_box['height']:.0f}")
    if views_box: print(f"Views: y={views_box['y']:.0f} to {views_box['y']+views_box['height']:.0f}")
    print(f"Action bar: y={ab_box['y']:.0f} to {ab_box['y']+ab_box['height']:.0f}")
    
    page.screenshot(path="temp.png")
    img = Image.open("temp.png")
    
    # CORRECT crop: include up to action bar bottom
    left = int(av_box['x']) - 3
    top = int(art_box['y']) - 5
    right = int(ab_box['x'] + ab_box['width']) + 3
    bottom = int(ab_box['y'] + ab_box['height'])  # Action bar bottom = 756
    
    print(f"\\nCrop: L={left}, T={top}, R={right}, B={bottom}")
    print(f"Expected height: {bottom - top}")
    
    cropped = img.crop((left, top, right, bottom))
    print(f"Cropped: {cropped.width}x{cropped.height}")
    
    # Add grid to verify
    draw = ImageDraw.Draw(cropped)
    for y in range(0, cropped.height, 100):
        draw.line([(0, y), (cropped.width, y)], fill='red', width=1)
        draw.text((5, y+2), f"y={y}", fill='red')
    draw.rectangle([150, 20, 420, 50], fill='yellow')
    draw.text((160, 25), f"SIZE: {cropped.width}x{cropped.height}", fill='black')
    
    rand = random.randint(1000, 9999)
    output = f"C:\\Users\\taoli1\\.openclaw\\workspace\\ai-news\\screenshots\\2026-02-12\\correct_{rand}.png"
    cropped.save(output)
    
    print(f"Saved: correct_{rand}.png")
    page.close()
