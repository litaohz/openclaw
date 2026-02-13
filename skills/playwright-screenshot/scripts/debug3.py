from playwright.sync_api import sync_playwright

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
    
    # Get article bounding box
    article = page.locator('article').first
    art_box = article.bounding_box()
    print(f"Article bounding box: x={art_box['x']}, y={art_box['y']}, width={art_box['width']}, height={art_box['height']}")
    print(f"Article right edge: {art_box['x'] + art_box['width']}")
    
    # Get viewport size
    vp = page.viewport_size
    print(f"Viewport: {vp}")
    
    # Take element screenshot and check its size
    article.screenshot(path="test_article_raw.png")
    from PIL import Image
    img = Image.open("test_article_raw.png")
    print(f"Element screenshot size: {img.width}x{img.height}")
    
    page.close()
