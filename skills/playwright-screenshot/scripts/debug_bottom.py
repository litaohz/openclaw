from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    context = browser.contexts[0]
    page = context.new_page()
    page.set_viewport_size({'width': 1400, 'height': 2000})
    page.goto('https://x.com/xai/status/2021667200885829667', wait_until='domcontentloaded')
    page.wait_for_selector('article', timeout=15000)
    page.wait_for_timeout(2000)
    
    article = page.locator('article').first
    
    # Find action bar (the row with reply/retweet/like/bookmark)
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    if action_bar.count() > 0:
        ab_box = action_bar.bounding_box()
        print(f'Action bar: y={ab_box["y"]:.0f}, h={ab_box["height"]:.0f}, bottom={ab_box["y"]+ab_box["height"]:.0f}')
    
    # Find "View quotes" or similar elements below action bar
    # These are typically links or spans below the engagement stats
    view_quotes = page.locator('text="View quotes"').first
    if view_quotes.count() > 0:
        vq_box = view_quotes.bounding_box()
        print(f'View quotes: y={vq_box["y"]:.0f}')
    
    # Find the reply box
    reply_box = page.locator('[data-testid="tweetTextarea_0"]').first
    if reply_box.count() > 0:
        rb_box = reply_box.bounding_box()
        print(f'Reply box: y={rb_box["y"]:.0f}')
    
    # Check all divs in the article to understand structure
    print("\nArticle children structure:")
    # Get article bottom
    art_box = article.bounding_box()
    print(f'Article: y={art_box["y"]:.0f}, bottom={art_box["y"]+art_box["height"]:.0f}')
    
    page.close()
