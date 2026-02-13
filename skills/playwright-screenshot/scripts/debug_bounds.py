from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    context = browser.contexts[0]
    page = context.new_page()
    page.set_viewport_size({'width': 1400, 'height': 2000})
    page.goto('https://x.com/xai/status/2021667200885829667', wait_until='domcontentloaded')
    page.wait_for_selector('article', timeout=15000)
    page.wait_for_timeout(2000)
    
    # Check various elements
    elements = [
        '[data-testid="primaryColumn"]',
        '[data-testid="cellInnerDiv"]',
        'article',
        '[data-testid="tweetText"]',
        '[data-testid="User-Name"]',
    ]
    
    for sel in elements:
        el = page.locator(sel).first
        if el.count() > 0:
            box = el.bounding_box()
            print(f'{sel}: x={box["x"]:.0f}, w={box["width"]:.0f}, right={box["x"]+box["width"]:.0f}')
    
    page.close()
