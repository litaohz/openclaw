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
    
    page.screenshot(path="raw_viewport.png", full_page=False)
    
    img = Image.open("raw_viewport.png")
    print(f"Viewport size: {img.width}x{img.height}")
    
    # Check what's at y=750-760 in the tweet column area (x ~= 500)
    print("\\nPixels at x=500:")
    for y in range(745, 780, 2):
        pixel = img.getpixel((500, y))
        brightness = sum(pixel) / 3
        char = '#' if brightness < 200 else '.'
        print(f"y={y}: {pixel} {'(dark)' if brightness < 200 else ''}")
    
    page.close()
