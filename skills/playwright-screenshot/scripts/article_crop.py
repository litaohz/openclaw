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
    
    # Hide sidebar
    page.evaluate('document.querySelector(\"[data-testid=sidebarColumn]\").style.display=\"none\"')
    page.wait_for_timeout(300)
    
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    # Key values
    article_top = art_box['y']
    article_left = art_box['x']
    action_bar_bottom = ab_box['y'] + ab_box['height']
    
    print(f"Article top: {article_top:.0f}")
    print(f"Action bar bottom: {action_bar_bottom:.0f}")
    print(f"Content height should be: {action_bar_bottom - article_top:.0f}")
    
    # Take screenshot of just the article element
    temp = "article_only.png"
    article.screenshot(path=temp)
    
    img = Image.open(temp)
    print(f"Article screenshot: {img.width}x{img.height}")
    
    # The article screenshot includes everything within article boundaries
    # But action bar is at y=708 from page top
    # Article top is at y=53
    # So action bar is at y=708-53=655 from article top
    
    action_bar_in_article = action_bar_bottom - article_top
    print(f"Action bar bottom in article coords: {action_bar_in_article:.0f}")
    
    # Crop the article screenshot to just above action bar bottom
    cropped = img.crop((0, 0, img.width, int(action_bar_in_article)))
    print(f"Cropped to: {cropped.width}x{cropped.height}")
    
    # Resize
    target_width = 560
    ratio = target_width / cropped.width
    final = cropped.resize((target_width, int(cropped.height * ratio)), Image.Resampling.LANCZOS)
    
    output = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\article_cropped.png"
    final.save(output, optimize=True)
    os.remove(temp)
    
    print(f"Saved: {output} ({final.width}x{final.height})")
    page.close()
