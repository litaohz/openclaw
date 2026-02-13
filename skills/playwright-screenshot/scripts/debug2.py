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
    
    # Get primary column actual content width
    col = page.locator('[data-testid="primaryColumn"]').first
    col_box = col.bounding_box()
    print(f"Primary Column: x={col_box['x']}, width={col_box['width']}, right={col_box['x']+col_box['width']}")
    
    # Get article bounds
    article = page.locator('article').first
    art_box = article.bounding_box()
    print(f"Article: x={art_box['x']}, width={art_box['width']}, right={art_box['x']+art_box['width']}")
    
    # Get sidebar
    sidebar = page.locator('[data-testid=\"sidebarColumn\"]').first
    if sidebar.count() > 0:
        sb_box = sidebar.bounding_box()
        print(f"Sidebar: x={sb_box['x']}")
    
    # Action bar - this is what we want as bottom boundary  
    action_bar = article.locator('[role=\"group\"][aria-label*=\"likes\"]').first
    ab_box = action_bar.bounding_box()
    print(f"Action bar: y={ab_box['y']}, height={ab_box['height']}, bottom={ab_box['y']+ab_box['height']}")
    
    # Find share button - last item in action bar
    share_btn = article.locator('[aria-label*=\"Share\"]').first
    if share_btn.count() > 0:
        sh_box = share_btn.bounding_box()
        print(f"Share button: x={sh_box['x']}, right={sh_box['x']+sh_box['width']}")
    
    page.close()
