from playwright.sync_api import sync_playwright
from PIL import Image

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
    art_box = article.bounding_box()
    
    # Get tweet text to find the real left boundary
    tweet_text = article.locator('[data-testid="tweetText"]').first
    tt_box = tweet_text.bounding_box() if tweet_text.count() > 0 else None
    
    # Get username for left boundary
    username = article.locator('[data-testid="User-Name"]').first
    un_box = username.bounding_box() if username.count() > 0 else None
    
    # Get avatar
    avatar = article.locator('[data-testid="Tweet-User-Avatar"]').first
    av_box = avatar.bounding_box() if avatar.count() > 0 else None
    
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    print(f"Article: x={art_box['x']:.0f}")
    if av_box: print(f"Avatar: x={av_box['x']:.0f}, right={av_box['x']+av_box['width']:.0f}")
    if un_box: print(f"Username: x={un_box['x']:.0f}")
    if tt_box: print(f"Tweet text: x={tt_box['x']:.0f}")
    print(f"Action bar: x={ab_box['x']:.0f}")
    
    # The issue: Reply box avatar is to the LEFT of the article
    # Let's check its position
    reply_avatar = page.locator('[data-testid="tweetTextarea_0"]').locator('..').locator('img').first
    if reply_avatar.count() > 0:
        ra_box = reply_avatar.bounding_box()
        print(f"\\nReply box avatar: x={ra_box['x']:.0f}, y={ra_box['y']:.0f}")
    
    # Screenshot with sidebar hidden
    page.screenshot(path="temp.png")
    img = Image.open("temp.png")
    
    # NEW STRATEGY: Use avatar's LEFT edge as the left boundary
    # This should exclude the reply box avatar which is in a different vertical position
    if av_box:
        left = int(av_box['x']) - 3  # Small margin before avatar
    else:
        left = int(art_box['x'])
    
    top = int(art_box['y']) - 5
    right = int(ab_box['x'] + ab_box['width']) + 3
    bottom = int(ab_box['y'] + ab_box['height']) - 5  # Stop just before action bar ends
    
    print(f"\\nCrop: L={left}, T={top}, R={right}, B={bottom}")
    
    cropped = img.crop((left, top, right, bottom))
    print(f"Cropped: {cropped.width}x{cropped.height}")
    
    # Verify no purple pixels at bottom-left
    bl_pixel = cropped.getpixel((5, cropped.height - 5))
    print(f"Bottom-left pixel: {bl_pixel}")
    
    # Resize
    target_width = 560
    ratio = target_width / cropped.width
    final = cropped.resize((target_width, int(cropped.height * ratio)), Image.Resampling.LANCZOS)
    
    output = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\fixed_left.png"
    final.save(output, optimize=True)
    
    print(f"Saved: {final.width}x{final.height}")
    page.close()
