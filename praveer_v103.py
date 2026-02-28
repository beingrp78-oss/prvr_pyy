# -*- coding: utf-8 -*-
import os, time, random, threading, sys, tempfile, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- V100 TURBO CONFIG ---
THREADS = 2 
TOTAL_DURATION = 25000 
BURST_SPEED = (0.05, 0.1) # 🔥 Reduced delay for machine-gun speed

def get_driver(agent_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # 🏎️ CPU Optimization: Desktop mode is actually faster than Mobile Emulation in Headless
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false") # Don't load images
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"v100_turbo_{agent_id}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def turbo_inject(driver, text):
    """Fires messages via the internal React dispatcher (Zero Latency)."""
    try:
        # This JS finds the box, injects text, and triggers the Enter key in 1ms
        driver.execute_script("""
            var box = document.querySelector('div[role="textbox"], textarea');
            if (box) {
                box.focus();
                // Direct text injection
                document.execCommand('insertText', false, arguments[0]);
                
                // Immediate Enter Dispatch
                var enter = new KeyboardEvent('keydown', {
                    key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
                });
                box.dispatchEvent(enter);
            }
        """, text)
        return True
    except:
        return False

def run_life_cycle(agent_id, cookie, target, messages):
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            
            # Inject session
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            
            # Wait for chat load (Staggered)
            time.sleep(12) 
            print(f"✅ Agent {agent_id} Armed", flush=True)

            start_time = time.time()
            # 2-Minute Hyper-Burst
            while (time.time() - start_time) < 120:
                msg = random.choice(messages) + " " + str(random.randint(100,999))
                if turbo_inject(driver, msg):
                    sys.stdout.write("🚀")
                    sys.stdout.flush()
                time.sleep(random.uniform(*BURST_SPEED))
                
        except Exception as e:
            print(f"⚠️ Agent {agent_id} glitch, restarting...", flush=True)
        finally:
            if driver: driver.quit()
            time.sleep(2)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    messages = os.environ.get("MESSAGES", "V100").split("|")
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_life_cycle, i+1, cookie, target, messages)

if __name__ == "__main__":
    main()
