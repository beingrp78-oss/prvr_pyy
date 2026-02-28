import os
import asyncio
import random
from playwright.async_api import async_playwright

# --- CONFIG ---
# Use the FULL cookie string (csrftoken=...; sessionid=...)
COOKIE_STRING = os.environ.get('INSTA_COOKIE')
THREAD_ID = "2859755064232019"
MESSAGE_TEXT = os.environ.get('MESSAGES', "Titan Strike")

async def run_strike():
    async with async_playwright() as p:
        # Launch real browser
        browser = await p.chromium.launch(headless=True)
        # Create a 'context' that mimics a real Windows Chrome user
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        # 🔑 Inject Cookies to bypass Login
        domain = ".instagram.com"
        cookies = []
        for pair in COOKIE_STRING.split(";"):
            if "=" in pair:
                name, value = pair.strip().split("=", 1)
                cookies.append({"name": name, "value": value, "domain": domain, "path": "/"})
        
        await context.add_cookies(cookies)
        page = await context.new_page()
        
        print("🌐 Navigating to Chat...", flush=True)
        await page.goto(f"https://www.instagram.com/direct/t/{THREAD_ID}/")
        
        # Wait for the text box to appear
        try:
            await page.wait_for_selector("div[role='textbox']", timeout=20000)
            print("✅ Chat Loaded. Starting Strike...", flush=True)
        except:
            print("❌ Timeout: Chat didn't load. Cookie might be expired.", flush=True)
            await browser.close()
            return

        while True:
            try:
                # Type the message
                full_msg = f"{MESSAGE_TEXT} {random.randint(100, 999)}"
                await page.fill("div[role='textbox']", full_msg)
                
                # Press Enter
                await page.keyboard.press("Enter")
                print(f"🔥 Strike Delivered: {full_msg}", flush=True)
                
                # Random human-like delay
                await asyncio.sleep(random.uniform(5, 12))
            except Exception as e:
                print(f"⚠️ Error: {e}", flush=True)
                await asyncio.sleep(30)

asyncio.run(run_strike())
