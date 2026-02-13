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
    
    # Find elements containing numbers like "1K" "2K" "9.8K" "4.4K"
    # These might be in spans
    
    article = page.locator('article').first
    
    # Get all text content positions
    spans = article.locator('span').all()
    
    print("Spans containing engagement numbers:")
    for span in spans:
        text = span.text_content()
        if text and any(x in text for x in ['1K', '2K', '9.8K', '9.9K', '4.4K', '1,0', '2,0']):
            box = span.bounding_box()
            if box and box['y'] > 600:  # Only look in the bottom area
                print(f"'{text[:30]}': y={box['y']:.0f}")
    
    print("\\n--- Looking for the row with reply/retweet/like counts ---")
    # The group that shows "1K replies, 2K reposts, 9.8K likes, 4.4K bookmarks"
    groups = article.locator('[role="group"]').all()
    for g in groups:
        label = g.get_attribute('aria-label')
        box = g.bounding_box()
        if label and box:
            print(f"Group: y={box['y']:.0f}-{box['y']+box['height']:.0f}")
            print(f"  Label: {label}")
    
    page.close()
