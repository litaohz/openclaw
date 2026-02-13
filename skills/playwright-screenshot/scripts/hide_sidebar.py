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
    
    # HIDE the sidebar before screenshot!
    page.evaluate('''() => {
        const sidebar = document.querySelector('[data-testid="sidebarColumn"]');
        if (sidebar) sidebar.style.display = 'none';
        
        // Also hide the "Relevant" section and reply box
        const timeline = document.querySelector('[aria-label="Timeline: Conversation"]');
        if (timeline) {
            // Hide everything after the first article
            const articles = timeline.querySelectorAll('article');
            for (let i = 1; i < articles.length; i++) {
                articles[i].style.display = 'none';
            }
        }
        
        // Hide reply box
        const replyBox = document.querySelector('[data-testid="reply"]');
        if (replyBox) replyBox.style.display = 'none';
    }''')
    
    page.wait_for_timeout(500)
    
    # Get article bounds
    article = page.locator('article').first
    art_box = article.bounding_box()
    
    # Get action bar bounds
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    print(f"After hiding sidebar:")
    print(f"Article: x={art_box['x']:.0f}, w={art_box['width']:.0f}")
    print(f"Action bar: x={ab_box['x']:.0f}, right={ab_box['x']+ab_box['width']:.0f}")
    
    # Take screenshot
    temp_path = "test_hidden_sidebar.temp.png"
    page.screenshot(path=temp_path, full_page=False)
    
    # Crop
    img = Image.open(temp_path)
    
    left = int(art_box['x']) - 5
    top = int(art_box['y']) - 5
    right = int(ab_box['x'] + ab_box['width']) + 5
    bottom = int(ab_box['y'] + ab_box['height']) - 2
    
    print(f"Crop: L={left}, T={top}, R={right}, B={bottom}")
    
    cropped = img.crop((left, top, right, bottom))
    
    # Add red border for verification
    draw = ImageDraw.Draw(cropped)
    draw.rectangle([0, 0, cropped.width-1, cropped.height-1], outline='red', width=3)
    draw.text((10, 10), f'{cropped.width}x{cropped.height}', fill='red')
    
    # Resize to 560
    target_width = 560
    ratio = target_width / cropped.width
    new_height = int(cropped.height * ratio)
    cropped = cropped.resize((target_width, new_height), Image.Resampling.LANCZOS)
    
    output_path = r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\hidden_sidebar.png"
    cropped.save(output_path)
    os.remove(temp_path)
    
    print(f"Saved: {output_path} ({cropped.width}x{cropped.height})")
    page.close()
