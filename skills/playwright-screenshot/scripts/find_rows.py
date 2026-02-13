from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

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
    
    # Find the engagement row with numbers (1K, 2K, 9.8K, 4.4K)
    # This is different from the action bar with buttons
    
    # Look for elements containing the view count / engagement stats
    # "14.8M Views" row
    views = page.locator('text=/Views|意见/').first
    if views.count() > 0:
        box = views.bounding_box()
        print(f"Views text: y={box['y']:.0f} to {box['y']+box['height']:.0f}")
    
    # The row with "1K reply, 2K retweet, 9.8K like, 4.4K bookmark"
    # These are clickable numbers above the action buttons
    
    # Find by looking at all elements in article and their positions
    print("\\n--- All testid elements in article ---")
    testids = ['reply', 'retweet', 'like', 'bookmark']
    for tid in testids:
        els = article.locator(f'[data-testid="{tid}"]').all()
        for i, el in enumerate(els):
            box = el.bounding_box()
            if box:
                print(f"{tid}[{i}]: y={box['y']:.0f}-{box['y']+box['height']:.0f}, x={box['x']:.0f}")
    
    # The time/date row "3:26 AM · Feb 12, 2026"
    time_el = page.locator('time').first
    if time_el.count() > 0:
        box = time_el.bounding_box()
        print(f"\\nTime element: y={box['y']:.0f} to {box['y']+box['height']:.0f}")
    
    page.close()
