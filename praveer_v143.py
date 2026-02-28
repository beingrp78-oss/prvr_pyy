# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V143 AGGRESSIVE-ENTRY)
# 📅 STATUS: 2-3s STAGGER | BURST-PHANTOM | 8-AGENTS

import os, time, sys, base64, threading, random
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ V143 CONFIG ---
THREADS_PER_MACHINE = 4            
BASE_DELAY_MS = 85                 
RECOVERY_RANGE = (1.2, 2.5)        
PURGE_INTERVAL_SEC = 900           
ENTRY_STAGGER = 2.5                # 🔥 Reduced from 40s to 2.5s

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
    ]
    chrome_options.add_argument(f"--user-agent={random.choice(ua_list)}")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def v143_dispatch(driver, b64_text, delay):
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        const rawText = atob(arguments[0]);

        async function fire(msg, ms) {
            const getBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            
            while(window.praveer_active) {
                let burstLimit = 10 + Math.floor(Math.random() * 5); 
                
                for(let i=0; i < burstLimit; i++) {
                    const box = getBox();
                    if (box) {
                        box.focus();
                        const salt = Math.random().toString(36).substring(7);
                        document.execCommand('insertText', false, msg + "\\n" + salt);
                        box.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        let btn = [...document.querySelectorAll('div[role="button"], button')].find(b => b.innerText === 'Send' || b.textContent === 'Send');
                        if (btn) btn.click();
                        else box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}));
                        
                        window.msg_count++;
                        await new Promise(r => setTimeout(r, ms + Math.floor(Math.random() * 15)));
                    }
                }
                await new Promise(r => setTimeout(r, 1000 + Math.random() * 1000));
            }
        }
        fire(rawText, arguments[1]);
    """, b64_text, delay)

def run_agent(agent_id, machine_id, cookie, target, b64_text):
    # 🔥 Fast Entry Logic
    time.sleep(agent_id * ENTRY_STAGGER) 
    while True:
        driver = None
        try:
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            time.sleep(8) # Reduced wait
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(10) # Reduced wait
            
            if "login" in driver.current_url: 
                print(f"❌ [M{machine_id}-A{agent_id}] Account Locked/Blocked.")
                return 

            v143_dispatch(driver, b64_text, BASE_DELAY_MS)

            start = time.time()
            while (time.time() - start) < PURGE_INTERVAL_SEC:
                time.sleep(20)
                try: 
                    c = driver.execute_script("return window.msg_count;")
                    print(f"💓 [M{machine_id}-A{agent_id}] Active: {c}")
                    sys.stdout.flush()
                except: break
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(15)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    raw_messages = os.environ.get("MESSAGES", "").strip()
    b64_messages = base64.b64encode(raw_messages.encode('utf-8')).decode('utf-8')
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, b64_messages)
            time.sleep(1) # Internal pool stagger

if __name__ == "__main__":
    main()
