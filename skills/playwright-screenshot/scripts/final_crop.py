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
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    avatar = article.locator('[data-testid="Tweet-User-Avatar"]').first
    av_box = avatar.bounding_box()
    
    # Find the LAST element we want - the like button bottom
    like_btn = article.locator('[data-testid="like"]').first
    like_box = like_btn.bounding_box()
    
    print(f"Article: y={art_box['y']:.0f}")
    print(f"Like button: y={like_box['y']:.0f} to {like_box['y']+like_box['height']:.0f}")
    
    # Find what's below the action bar
    relevant = page.locator('text=/Relevant|相关/').first
    if relevant.count() > 0:
        r_box = relevant.bounding_box()
        print(f"Relevant: y={r_box['y']:.0f}")
    
    page.screenshot(path="temp.png")
    img = Image.open("temp.png")
    
    # Crop: stop AT the like button bottom, not after
    left = int(av_box['x']) - 3
    top = int(art_box['y']) - 5
    right = int(like_box['x'] + like_box['width']) + 200  # Wide enough for all buttons
    bottom = int(like_box['y'] + like_box['height']) - 5  # STOP 5px before like button ends
    
    print(f"\\nCrop: L={left}, T={top}, R={right}, B={bottom}")
    
    cropped = img.crop((left, top, right, bottom))
    print(f"Cropped: {cropped.width}x{cropped.height}")
    
    # Resize to 560
    target_width = 560
    ratio = target_width / cropped.width
    final = cropped.resize((target_width, int(cropped.height * ratio)), Image.Resampling.LANCZOS)
    
    rand = random.randint(1000, 9999)
    output = f"C:\\Users\\taoli1\\.openclaw\\workspace\\ai-news\\screenshots\\2026-02-12\\final_{rand}.png"
    final.save(output, optimize=True)
    
    print(f"Saved: final_{rand}.png ({final.width}x{final.height})")
    page.close()
