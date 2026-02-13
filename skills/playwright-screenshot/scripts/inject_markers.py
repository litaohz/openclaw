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
    
    page.evaluate('document.querySelector(\"[data-testid=sidebarColumn]\").style.display=\"none\"')
    
    # Inject a visual marker directly on the page using JavaScript
    # This will paint a red border around the action bar
    page.evaluate('''() => {
        const actionBar = document.querySelector('[role="group"][aria-label*="likes"]');
        if (actionBar) {
            actionBar.style.border = '3px solid red';
            actionBar.style.background = 'rgba(255,0,0,0.1)';
        }
        
        // Also mark the article
        const article = document.querySelector('article');
        if (article) {
            article.style.outline = '2px dashed blue';
        }
    }''')
    
    page.wait_for_timeout(500)
    
    # Now screenshot
    page.screenshot(path="injected_markers.png")
    print("Saved injected_markers.png")
    
    page.close()
