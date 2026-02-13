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
    
    # Get specific elements inside article to find actual content boundary
    article = page.locator('article').first
    
    # The tweet text container
    tweet_text = article.locator('[data-testid="tweetText"]').first
    if tweet_text.count() > 0:
        tt_box = tweet_text.bounding_box()
        print(f"Tweet text: x={tt_box['x']:.0f}, w={tt_box['width']:.0f}, right={tt_box['x']+tt_box['width']:.0f}")
    
    # The media (video/image) container
    media = article.locator('[data-testid="tweetPhoto"], [data-testid="videoPlayer"]').first
    if media.count() > 0:
        m_box = media.bounding_box()
        print(f"Media: x={m_box['x']:.0f}, w={m_box['width']:.0f}, right={m_box['x']+m_box['width']:.0f}")
    
    # Action bar
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    if action_bar.count() > 0:
        ab_box = action_bar.bounding_box()
        print(f"Action bar: x={ab_box['x']:.0f}, w={ab_box['width']:.0f}, right={ab_box['x']+ab_box['width']:.0f}")
    
    # User name/handle row
    username = article.locator('[data-testid="User-Name"]').first
    if username.count() > 0:
        u_box = username.bounding_box()
        print(f"Username: x={u_box['x']:.0f}, w={u_box['width']:.0f}, right={u_box['x']+u_box['width']:.0f}")
    
    # Primary column
    col = page.locator('[data-testid="primaryColumn"]').first
    col_box = col.bounding_box()
    print(f"Primary column: x={col_box['x']:.0f}, w={col_box['width']:.0f}, right={col_box['x']+col_box['width']:.0f}")
    
    page.close()
