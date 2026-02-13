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
    
    # DON'T hide sidebar yet
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    # Find "Relevant" or "View quotes"
    relevant = page.locator('text=/Relevant/').first
    view_quotes = page.locator('text=/View quotes/').first
    post_reply = page.locator('[data-testid="tweetTextarea_0"]').first
    
    print(f"Article: y={art_box['y']:.0f} to {art_box['y']+art_box['height']:.0f}")
    print(f"Action bar: y={ab_box['y']:.0f} to {ab_box['y']+ab_box['height']:.0f}")
    
    if relevant.count() > 0:
        r_box = relevant.bounding_box()
        print(f"Relevant text: y={r_box['y']:.0f}")
    
    if view_quotes.count() > 0:
        vq_box = view_quotes.bounding_box()
        print(f"View quotes: y={vq_box['y']:.0f}")
        
    if post_reply.count() > 0:
        pr_box = post_reply.bounding_box()
        print(f"Post reply textarea: y={pr_box['y']:.0f}")
    
    # Now hide sidebar and check again
    page.evaluate('document.querySelector(\"[data-testid=sidebarColumn]\").style.display=\"none\"')
    page.wait_for_timeout(500)
    
    print("\\n--- After hiding sidebar ---")
    art_box2 = article.bounding_box()
    ab_box2 = action_bar.bounding_box()
    print(f"Article: y={art_box2['y']:.0f} to {art_box2['y']+art_box2['height']:.0f}")
    print(f"Action bar: y={ab_box2['y']:.0f} to {ab_box2['y']+ab_box2['height']:.0f}")
    
    page.close()
