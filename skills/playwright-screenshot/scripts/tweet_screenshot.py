"""
Tweet Screenshot - v22  
Use article bottom minus fixed offset (most reliable)
"""
from playwright.sync_api import sync_playwright
from PIL import Image
import os

CDP_URL = "http://localhost:9222"

TWEET_WIDTH = 520
# Offset from article bottom to exclude "View quotes" and reply box
# Article typically ends at reply box; we want to stop before "View quotes"
BOTTOM_EXCLUDE = 100  # pixels to cut from bottom (keeps action bar, excludes View quotes)

def screenshot_tweet(url, output_path, max_height=1500):
    """
    Screenshot a tweet - reliable crop
    """
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()
        
        page.set_viewport_size({"width": 1400, "height": 2000})
        
        try:
            print(f"Navigating: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_selector('article', timeout=15000)
            page.wait_for_timeout(3500)
            
            article = page.locator('article').first
            art_box = article.bounding_box()
            
            if not art_box:
                print("Could not find tweet")
                return None
            
            print(f"Article: y={art_box['y']:.0f}, h={art_box['height']:.0f}, bottom={art_box['y']+art_box['height']:.0f}")
            
            # Get positions - use article x directly (more reliable than avatar)
            # Article x is the true left boundary of the tweet content
            crop_left = int(art_box['x']) - 35  # larger margin to capture full text
            
            crop_top = max(0, int(art_box['y']) - 8)
            crop_right = crop_left + TWEET_WIDTH
            
            # Use article bottom minus fixed offset
            # This is more reliable than trying to find specific elements
            crop_bottom = int(art_box['y'] + art_box['height']) - BOTTOM_EXCLUDE
            
            print(f"Crop bounds: L={crop_left}, T={crop_top}, R={crop_right}, B={crop_bottom}")
            
            # Take screenshot
            temp_path = output_path + ".temp.png"
            page.screenshot(path=temp_path, full_page=False)
            
            img = Image.open(temp_path)
            
            # Ensure bounds are valid
            crop_left = max(0, crop_left)
            crop_top = max(0, crop_top)
            crop_right = min(crop_right, img.width)
            crop_bottom = min(crop_bottom, img.height)
            
            cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
            print(f"Cropped: {cropped.width}x{cropped.height}")
            
            # Apply max height
            if max_height > 0 and cropped.height > max_height:
                cropped = cropped.crop((0, 0, cropped.width, max_height))
            
            # Resize to target width
            target_width = 560
            if cropped.width != target_width:
                ratio = target_width / cropped.width
                new_height = int(cropped.height * ratio)
                cropped = cropped.resize((target_width, new_height), Image.Resampling.LANCZOS)
            
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            cropped.save(output_path, optimize=True)
            os.remove(temp_path)
            
            print(f"Saved: {output_path} ({cropped.width}x{cropped.height})")
            return output_path
            
        finally:
            page.close()


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://x.com/OpenAI/status/2019474152743223477"
    output = sys.argv[2] if len(sys.argv) > 2 else "tweet.png"
    max_h = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    screenshot_tweet(url, output, max_h)
