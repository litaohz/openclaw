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
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    print(f"Article: y={art_box['y']:.0f} to {art_box['y']+art_box['height']:.0f}")
    
    # Find all groups with aria-label containing numbers (engagement stats)
    groups = article.locator('[role="group"]').all()
    for i, g in enumerate(groups):
        box = g.bounding_box()
        label = g.get_attribute('aria-label') or ''
        if box:
            print(f"Group {i}: y={box['y']:.0f}-{box['y']+box['height']:.0f}, label={label[:50]}")
    
    # Find specific elements
    print("\\n--- Specific elements ---")
    
    # Reply button (in action bar)
    reply = article.locator('[data-testid="reply"]').first
    if reply.count() > 0:
        box = reply.bounding_box()
        print(f"Reply button: y={box['y']:.0f}-{box['y']+box['height']:.0f}")
    
    # Retweet button
    retweet = article.locator('[data-testid="retweet"]').first
    if retweet.count() > 0:
        box = retweet.bounding_box()
        print(f"Retweet button: y={box['y']:.0f}-{box['y']+box['height']:.0f}")
    
    # Like button
    like = article.locator('[data-testid="like"]').first
    if like.count() > 0:
        box = like.bounding_box()
        print(f"Like button: y={box['y']:.0f}-{box['y']+box['height']:.0f}")
    
    # "View quotes" link
    view_quotes = page.locator('text=/View.*quote/i').first
    if view_quotes.count() > 0:
        box = view_quotes.bounding_box()
        print(f"View quotes: y={box['y']:.0f}-{box['y']+box['height']:.0f}")
    
    # "Relevant" 
    relevant = page.locator('text=/Relevant|相关/').first
    if relevant.count() > 0:
        box = relevant.bounding_box()
        print(f"Relevant: y={box['y']:.0f}-{box['y']+box['height']:.0f}")
    
    # Reply box
    reply_box = page.locator('[data-testid="tweetTextarea_0"]').first
    if reply_box.count() > 0:
        box = reply_box.bounding_box()
        print(f"Reply textarea: y={box['y']:.0f}-{box['y']+box['height']:.0f}")
    
    page.close()
