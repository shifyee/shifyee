import sys
import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    # Gets the title of the issue that was just opened (e.g. iphone_action:app_spotify)
    issue_title = sys.argv[1] if len(sys.argv) > 1 else "iphone_action:home"
    
    action_map = {
        "iphone_action:power": "powerToggle()",
        "iphone_action:unlock": "unlockPhone()",
        "iphone_action:home": "goHome()",
        "iphone_action:app_commits": "openApp('commits')",
        "iphone_action:app_notes": "openApp('notes')",
        "iphone_action:app_spotify": "openApp('spotify')",
        "iphone_action:app_weather": "openApp('weather')",
        "iphone_action:app_youtube": "openApp('youtube')"
    }
    
    js_command = action_map.get(issue_title, "goHome()")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Sized specifically to fit the iPhone cleanly in the markdown
        page = await browser.new_page(viewport={"width": 450, "height": 850}, device_scale_factor=2)
        
        # Load the HTML file from the GitHub workspace
        workspace = os.getenv("GITHUB_WORKSPACE", os.getcwd())
        file_path = f"file://{workspace}/iphone_dashboard_final.html"
        
        await page.goto(file_path)
        
        # Give APIs (Weather, GitHub, Spotify image) time to load on the phone screen
        await page.wait_for_timeout(3000) 
        
        # Tell the phone to click the app the user chose
        await page.evaluate(js_command)
        
        # Wait for the screen transition animation to finish
        await page.wait_for_timeout(1000) 
        
        phone_element = await page.query_selector("#phoneShell")
        
        # Ensure the assets folder exists
        os.makedirs("assets", exist_ok=True)
        
        # Take screenshot of just the phone with a transparent background
        await phone_element.screenshot(path="assets/iphone_state.png", omit_background=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
