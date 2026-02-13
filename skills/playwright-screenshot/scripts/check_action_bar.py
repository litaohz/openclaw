from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

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
    
    # Get action bar position
    article = page.locator('article').first
    action_bar = article.locator('[role="group"][aria-label*="likes"]').first
    ab_box = action_bar.bounding_box()
    
    action_bar_bottom = ab_box['y'] + ab_box['height']
    print(f"Action bar bottom (reported): {action_bar_bottom:.0f}")
    
    # Take screenshot
    page.screenshot(path="full_viewport.png", full_page=False)
    
    img = Image.open("full_viewport.png")
    
    # Draw a red line at the reported action bar bottom
    draw = ImageDraw.Draw(img)
    draw.line([(0, int(action_bar_bottom)), (1400, int(action_bar_bottom))], fill='red', width=3)
    draw.text((50, int(action_bar_bottom) - 20), f"action_bar_bottom = {int(action_bar_bottom)}", fill='red')
    
    # Save a section around the action bar
    section = img.crop((400, 650, 1050, 850))
    section.save(r"C:\Users\taoli1\.openclaw\workspace\ai-news\screenshots\2026-02-12\action_bar_section.png")
    
    print(f"Saved section around action bar (y=650-850)")
    page.close()
