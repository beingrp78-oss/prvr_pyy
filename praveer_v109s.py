import os
import time
import random
from instagrapi import Client
from instagrapi.exceptions import ClientError, LoginRequired

# --- CONFIGURATION ---
# In GitHub Secrets, only paste the VALUE of your sessionid (e.g., 80504360780%3A...)
SESSION_ID = os.environ.get('INSTA_SESSION_ID')
# Your verified 16-digit ID (User ID or Thread ID)
TARGET_ID = "2859755064232019"
MESSAGE_TEXT = os.environ.get('MESSAGES', "Strike Active")

def start_strike():
    cl = Client()
    
    # 🛡️ Step 1: Login using Session ID
    try:
        print("🔗 Attempting Session Login...")
        cl.login_by_sessionid(SESSION_ID)
        print(f"✅ Login Successful! Logged in as: {cl.username}")
    except Exception as e:
        print(f"❌ Login Failed: {e}")
        return

    # 🚀 Step 2: The Strike Loop
    print(f"🔥 Targeting ID: {TARGET_ID} | Starting Engine...")
    
    while True:
        try:
            # instagrapi handles the 404/400 logic internally
            # It will automatically find if this is a User or a Thread
            cl.direct_send(f"{MESSAGE_TEXT} [{random.randint(100, 999)}]", user_ids=[TARGET_ID])
            print(f"✅ Strike Delivered to {TARGET_ID}")
            
            # Random sleep between 3 to 7 seconds to mimic human behavior
            time.sleep(random.uniform(3, 7))
            
        except ClientError as e:
            print(f"⚠️ Instagram blocked the request: {e}")
            time.sleep(60) # Cool down for 1 minute
        except Exception as e:
            print(f"🛑 Unexpected Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_strike()
