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
    
    # Find the like button to get exact bottom
    like_btn = article.locator('[data-testid="like"]').first
    like_box = like_btn.bounding_box()
    
    print(f"Action bar: y={ab_box['y']:.0f} to {ab_box['y']+ab_box['height']:.0f}")
    print(f"Like button: y={like_box['y']:.0f} to {like_box['y']+like_box['height']:.0f}")
    
    page.screenshot(path="temp.png")
    img = Image.open("temp.png")
    
    # Use avatar left, and LIKE BUTTON bottom (not action bar)
    left = int(av_box['x']) - 3
    top = int(art_box['y']) - 5
    right = int(ab_box['x'] + ab_box['width']) + 3
    # Try different bottom values to find where "Relevant" starts
    
    # The engagement numbers row is at y=722-725
    # Let's stop right after that - around y=730
    bottom = int(like_box['y'] + like_box['height']) - 10  # Extra margin
    
    print(f"Crop: L={left}, T={top}, R={right}, B={bottom}")
    
    cropped = img.crop((left, top, right, bottom))
    
    # Resize
    target_width = 560
    ratio = target_width / cropped.width
    final = cropped.resize((target_width, int(cropped.height * ratio)), Image.Resampling.LANCZOS)
    
    output = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\tight_bottom.png"
    final.save(output, optimize=True)
    
    print(f"Saved: {final.width}x{final.height}")
    page.close()
