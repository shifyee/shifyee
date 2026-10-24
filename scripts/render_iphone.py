import sys
import asyncio
from playwright.async_api import async_playwright

async def main():
    # Get the action from the issue title (e.g., "iphone_action:app_commits")
    issue_title = sys.argv[1] if len(sys.argv) > 1 else ""
    
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

    # Default to home if unrecognized
    js_command = action_map.get(issue_title, "goHome()")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Set a viewport size that perfectly fits the phone
        page = await browser.new_page(viewport={"width": 600, "height": 900})
        
        # Load your HTML file (make sure it's saved as dashboard.html in your repo root)
        await page.goto("file:///github/workspace/iphone_dashboard_final.html")
        
        # Wait for live data (weather, github stats) to load
        await page.wait_for_timeout(2000) 
        
        # Execute the action the user clicked
        await page.evaluate(js_command)
        
        # Wait for the smooth CSS animations to finish
        await page.wait_for_timeout(1000)
        
        # Take a transparent screenshot of just the phone element
        phone_element = await page.query_selector("#phoneShell")
        await phone_element.screenshot(path="assets/iphone_state.png", omit_background=True)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
