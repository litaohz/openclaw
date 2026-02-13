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
    
    # HIDE sidebar and extra content
    page.evaluate('''() => {
        // Hide sidebar
        const sidebar = document.querySelector('[data-testid="sidebarColumn"]');
        if (sidebar) sidebar.style.display = 'none';
    }''')
    
    page.wait_for_timeout(300)
    
    # Get article bounds
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    # Get action bar bounds - this is the REAL content boundary
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    # Get avatar for left boundary  
    avatar = article.locator('[data-testid="Tweet-User-Avatar"]').first
    av_box = avatar.bounding_box() if avatar.count() > 0 else None
    
    if av_box:
        left_x = av_box['x'] - 8
        print(f"Avatar: x={av_box['x']:.0f}")
    else:
        left_x = art_box['x'] - 8
        print(f"No avatar, using article x={art_box['x']:.0f}")
    
    print(f"Article: x={art_box['x']:.0f}, y={art_box['y']:.0f}")
    print(f"Action bar: y={ab_box['y']:.0f}, bottom={ab_box['y']+ab_box['height']:.0f}")
    
    # Take full screenshot
    temp_path = "test_v2.temp.png"
    page.screenshot(path=temp_path, full_page=False)
    
    img = Image.open(temp_path)
    
    # Crop boundaries
    left = max(0, int(left_x))
    top = max(0, int(art_box['y']) - 8)
    right = int(ab_box['x'] + ab_box['width']) + 3
    bottom = int(ab_box['y'] + ab_box['height'])  # Exact at action bar
    
    print(f"Crop: L={left}, T={top}, R={right}, B={bottom}")
    
    cropped = img.crop((left, top, right, bottom))
    print(f"Cropped: {cropped.width}x{cropped.height}")
    
    # Resize
    target_width = 560
    ratio = target_width / cropped.width
    new_height = int(cropped.height * ratio)
    final = cropped.resize((target_width, new_height), Image.Resampling.LANCZOS)
    
    output = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\v13_clean.png"
    final.save(output, optimize=True)
    os.remove(temp_path)
    
    print(f"Saved: {output} ({final.width}x{final.height})")
    page.close()
