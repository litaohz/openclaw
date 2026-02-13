"""
Debug: Check device pixel ratio and actual positions
"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    context = browser.contexts[0]
    page = context.new_page()
    
    page.set_viewport_size({'width': 1400, 'height': 2000})
    page.goto('https://x.com/xai/status/2021667200885829667', wait_until='domcontentloaded')
    page.wait_for_selector('article', timeout=15000)
    page.wait_for_timeout(2000)
    
    # Check device pixel ratio
    dpr = page.evaluate('window.devicePixelRatio')
    print(f"Device Pixel Ratio: {dpr}")
    
    # Check scroll position
    scroll_y = page.evaluate('window.scrollY')
    print(f"Scroll Y: {scroll_y}")
    
    # Check viewport dimensions
    inner_w = page.evaluate('window.innerWidth')
    inner_h = page.evaluate('window.innerHeight')
    print(f"Inner dimensions: {inner_w}x{inner_h}")
    
    # Get actual positions via JS
    article = page.locator('article').first
    art_rect = page.evaluate('''() => {
        const el = document.querySelector('article');
        const rect = el.getBoundingClientRect();
        return {x: rect.x, y: rect.y, width: rect.width, height: rect.height, bottom: rect.bottom};
    }''')
    print(f"Article (JS): y={art_rect['y']:.0f}, h={art_rect['height']:.0f}, bottom={art_rect['bottom']:.0f}")
    
    # Get bookmark button position via JS
    bm_rect = page.evaluate('''() => {
        const el = document.querySelector('[data-testid="bookmark"]');
        if (!el) return null;
        const rect = el.getBoundingClientRect();
        return {y: rect.y, height: rect.height, bottom: rect.bottom};
    }''')
    if bm_rect:
        print(f"Bookmark (JS): y={bm_rect['y']:.0f}, h={bm_rect['height']:.0f}, bottom={bm_rect['bottom']:.0f}")
    
    # Check "View quotes" position
    vq_rect = page.evaluate('''() => {
        const els = document.querySelectorAll('a[href*="quotes"]');
        for (const el of els) {
            if (el.textContent.includes('View')) {
                const rect = el.getBoundingClientRect();
                return {y: rect.y, text: el.textContent};
            }
        }
        return null;
    }''')
    if vq_rect:
        print(f"View quotes (JS): y={vq_rect['y']:.0f}, text='{vq_rect['text']}'")
    
    page.close()
