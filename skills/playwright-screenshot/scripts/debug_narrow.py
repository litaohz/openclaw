from playwright.sync_api import sync_playwright

CDP_URL = "http://localhost:9222"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0]
    page = context.new_page()
    page.set_viewport_size({"width": 700, "height": 2000})
    
    url = "https://x.com/xai/status/2021667200885829667"
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_selector('article', timeout=15000)
    page.wait_for_timeout(3500)
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    print(f"Article: y={art_box['y']:.0f}, height={art_box['height']:.0f}, bottom={art_box['y']+art_box['height']:.0f}")
    
    # Action bar
    action_bar = article.locator('[role=\"group\"][aria-label*=\"likes\"]').first
    ab_box = action_bar.bounding_box()
    print(f"Action bar: y={ab_box['y']:.0f}, height={ab_box['height']:.0f}, bottom={ab_box['y']+ab_box['height']:.0f}")
    
    # Find "Relevant" text
    relevant = page.locator('text=\"Relevant\"').first
    if relevant.count() > 0:
        r_box = relevant.bounding_box()
        print(f"Relevant: y={r_box['y']:.0f}")
    else:
        print("Relevant not found")
    
    page.close()
