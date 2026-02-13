from playwright.sync_api import sync_playwright
from PIL import Image
import os

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
    
    # Check positions
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    # Action bar with reply/retweet/like/share buttons
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    # The row with reply count, retweet count, like count (above the buttons)
    # This is what we actually want to include
    
    # Find the engagement stats row
    reply_count = article.locator('[data-testid="reply"]').first
    if reply_count.count() > 0:
        rc_box = reply_count.bounding_box()
        print(f"Reply button: y={rc_box['y']:.0f}, bottom={rc_box['y']+rc_box['height']:.0f}")
    
    # The actual action buttons row
    print(f"Action bar: y={ab_box['y']:.0f}, h={ab_box['height']:.0f}, bottom={ab_box['y']+ab_box['height']:.0f}")
    
    # Article boundaries
    print(f"Article: x={art_box['x']:.0f}, y={art_box['y']:.0f}, bottom={art_box['y']+art_box['height']:.0f}")
    
    # What's at y=760? (just after action bar)
    # Check for "Relevant" section
    relevant = page.locator('text=/Relevant|相关/').first
    if relevant.count() > 0:
        r_box = relevant.bounding_box()
        print(f"Relevant text: y={r_box['y']:.0f}")
    
    page.close()
