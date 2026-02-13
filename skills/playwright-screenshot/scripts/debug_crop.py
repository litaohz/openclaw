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
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    print(f"Article: x={art_box['x']:.0f}, y={art_box['y']:.0f}, w={art_box['width']:.0f}")
    print(f"Article right edge: {art_box['x'] + art_box['width']:.0f}")
    
    # Action bar
    action_bar = article.locator('[role=\"group\"][aria-label*=\"likes\"]').first
    ab_box = action_bar.bounding_box()
    print(f"Action bar bottom: {ab_box['y'] + ab_box['height']:.0f}")
    
    # Sidebar
    sidebar = page.locator('[data-testid=\"sidebarColumn\"]').first
    if sidebar.count() > 0:
        sb_box = sidebar.bounding_box()
        print(f"Sidebar starts at x={sb_box['x']:.0f}")
    
    # Take screenshot
    page.screenshot(path="debug_full.png", full_page=False)
    
    # Now crop manually
    img = Image.open("debug_full.png")
    
    # Crop exactly to article bounds
    left = int(art_box['x']) - 5
    top = int(art_box['y']) - 5
    right = int(art_box['x'] + art_box['width']) + 5
    bottom = int(ab_box['y'] + ab_box['height']) - 2
    
    print(f"Crop box: L={left}, T={top}, R={right}, B={bottom}")
    
    cropped = img.crop((left, top, right, bottom))
    cropped.save("debug_cropped.png")
    print(f"Cropped size: {cropped.width}x{cropped.height}")
    
    page.close()
