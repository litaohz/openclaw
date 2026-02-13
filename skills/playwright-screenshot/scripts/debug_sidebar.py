from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    context = browser.contexts[0]
    page = context.new_page()
    page.set_viewport_size({'width': 1400, 'height': 2000})
    page.goto('https://x.com/xai/status/2021667200885829667', wait_until='domcontentloaded')
    page.wait_for_selector('article', timeout=15000)
    page.wait_for_timeout(2000)
    
    # Check sidebar elements
    elements = [
        '[data-testid="sidebarColumn"]',
        '[aria-label="Search"]',
        'aside',
        '[data-testid="SearchBox_Search_Input"]',
    ]
    
    for sel in elements:
        el = page.locator(sel).first
        if el.count() > 0:
            box = el.bounding_box()
            print(f'{sel}: x={box["x"]:.0f}, w={box["width"]:.0f}')
        else:
            print(f'{sel}: NOT FOUND')
    
    # Also check where the border/separator is
    # The vertical line between main content and sidebar
    primary = page.locator('[data-testid="primaryColumn"]').first
    if primary.count() > 0:
        pbox = primary.bounding_box()
        print(f'\nPrimary column ends at: {pbox["x"] + pbox["width"]:.0f}')
    
    page.close()
