from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
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
    
    # HIDE sidebar and extra content
    page.evaluate('''() => {
        // Hide sidebar
        const sidebar = document.querySelector('[data-testid="sidebarColumn"]');
        if (sidebar) sidebar.style.display = 'none';
        
        // Hide everything below the main tweet
        // Find "Relevant" heading and hide it + everything after
        const relevantHeadings = document.querySelectorAll('h2');
        relevantHeadings.forEach(h => {
            if (h.textContent.includes('Relevant') || h.textContent.includes('相关')) {
                let parent = h.closest('div[class]');
                if (parent) parent.style.display = 'none';
            }
        });
        
        // Hide reply box
        const replyBoxes = document.querySelectorAll('[data-testid="tweetTextarea_0"]');
        replyBoxes.forEach(box => {
            let parent = box.closest('div[class]');
            while (parent && parent.tagName !== 'ARTICLE') {
                if (parent.parentElement && parent.parentElement.tagName !== 'ARTICLE') {
                    parent = parent.parentElement;
                } else {
                    break;
                }
            }
            if (parent) parent.style.display = 'none';
        });
        
        // Hide "View quotes" link
        const links = document.querySelectorAll('a');
        links.forEach(link => {
            if (link.textContent.includes('View') && link.textContent.includes('quote')) {
                link.style.display = 'none';
            }
        });
    }''')
    
    page.wait_for_timeout(500)
    
    # Get article bounds
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    # Get action bar bounds
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    # Get avatar position for left boundary
    avatar = article.locator('img[src*="profile_images"]').first
    if avatar.count() > 0:
        av_box = avatar.bounding_box()
        left_x = av_box['x'] - 10  # More margin for avatar
        print(f"Avatar x: {av_box['x']:.0f}")
    else:
        left_x = art_box['x'] - 10
    
    print(f"Article: x={art_box['x']:.0f}, w={art_box['width']:.0f}")
    print(f"Action bar bottom: {ab_box['y']+ab_box['height']:.0f}")
    
    # Take screenshot
    temp_path = "test_clean.temp.png"
    page.screenshot(path=temp_path, full_page=False)
    
    # Crop - use avatar for left, action bar for bottom
    img = Image.open(temp_path)
    
    left = max(0, int(left_x))
    top = max(0, int(art_box['y']) - 8)
    right = int(ab_box['x'] + ab_box['width']) + 5
    bottom = int(ab_box['y'] + ab_box['height'])  # Exact action bar bottom
    
    print(f"Crop: L={left}, T={top}, R={right}, B={bottom}")
    
    cropped = img.crop((left, top, right, bottom))
    print(f"Cropped: {cropped.width}x{cropped.height}")
    
    # Resize to 560
    target_width = 560
    ratio = target_width / cropped.width
    new_height = int(cropped.height * ratio)
    cropped = cropped.resize((target_width, new_height), Image.Resampling.LANCZOS)
    
    output_path = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\clean_final.png"
    cropped.save(output_path)
    os.remove(temp_path)
    
    print(f"Saved: {output_path} ({cropped.width}x{cropped.height})")
    page.close()
