# -*- coding: utf-8 -*-
# 🚀 PHOENIX V100.35 (VOLT-CRUSHER) - STABLE 24/7
# 🛡️ BY PRAVEERFUCKS | 120-PROCESS DISTRIBUTED MATRIX

import os, time, random, sys, string, multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ VOLT-CRUSHER SPECS ---
STRIKE_DELAY = 0.001  # 1ms Hardware Pulse
PROCESS_COUNT = 3     # Total Chrome instances per GitHub Machine

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.page_load_strategy = 'eager'
    
    # 💥 Resource Stripping: Kill everything that slows down the DOM
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--mute-audio")
    options.add_argument("--js-flags='--max-old-space-size=512'")
    
    # iPad Pro for the most lightweight Instagram DOM structure
    mobile_emulation = { "deviceName": "iPad Pro" }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(options=options, service=service)

def volt_strike(cookie, target, msg_list, p_id):
    """Independent Process Strike Engine."""
    driver = get_driver()
    try:
        driver.get(f"https://www.instagram.com/direct/t/{target}/")
        driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
        driver.refresh()
        
        time.sleep(12) # Secure Handshake
        
        strike_count = 0
        while True:
            # ♻️ Memory Recovery: Refresh every 75 strikes to purge heavy DOM history
            if strike_count > 75:
                driver.refresh()
                time.sleep(6)
                strike_count = 0
                
            salt = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
            payload = f"{random.choice(msg_list)} [{random.randint(1000, 9999)}]-{salt}"
            
            # ⚡ Direct Memory Injection
            driver.execute_script("""
                const box = document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
                if (box) {
                    box.focus();
                    document.execCommand('insertText', false, arguments[0]);
                    box.dispatchEvent(new Event('input', { bubbles: true }));
                    const enter = new KeyboardEvent('keydown', { bubbles: true, key: 'Enter', code: 'Enter', keyCode: 13 });
                    box.dispatchEvent(enter);
                    // Instant wipe to stop the 'loading' ghosting
                    setTimeout(() => { box.innerHTML = ""; box.innerText = ""; }, 2);
                }
            """, payload)
            
            sys.stdout.write(f"⚡")
            sys.stdout.flush()
            strike_count += 1
            time.sleep(STRIKE_DELAY)
    except Exception as e:
        print(f"Agent {p_id} Resetting...")
    finally:
        driver.quit()

def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target = os.environ.get("TARGET_THREAD_ID")
    msg_env = os.environ.get("MESSAGES", "Strike|Active")
    msg_list = msg_env.split("|")
    
    # 🛰️ Launching Parallel Processes
    workers = []
    for i in range(PROCESS_COUNT):
        p = multiprocessing.Process(target=volt_strike, args=(cookie, target, msg_list, i))
        p.start()
        workers.append(p)
        time.sleep(4) # Balanced stagger to prevent boot-up crash

    for p in workers:
        p.join()

if __name__ == "__main__":
    main()
