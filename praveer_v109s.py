import os
import time
import random
from instagrapi import Client
from instagrapi.exceptions import ClientError

# --- CONFIG ---
SESSION_ID = os.environ.get('INSTA_SESSION_ID')
# Your verified 16-digit ID
TARGET_ID = "2859755064232019"
MESSAGE_TEXT = os.environ.get('MESSAGES', "Titan Strike Active")

def start_strike():
    cl = Client()
    
    # 🔑 LOGIN
    try:
        print("🔗 Connecting to Instagram...")
        cl.login_by_sessionid(SESSION_ID)
        print(f"✅ Logged in as: {cl.username}")
    except Exception as e:
        print(f"❌ Login Failed: {e}")
        return

    print(f"🔥 Targeting: {TARGET_ID}")
    
    while True:
        try:
            # 🚀 We use direct_send with the TARGET_ID as a USER_ID first.
            # If it's a thread ID, instagrapi handles the switch automatically.
            cl.direct_send(f"{MESSAGE_TEXT} {random.randint(100, 999)}", user_ids=[int(TARGET_ID)])
            
            print(f"✅ [SUCCESS] Message delivered to {TARGET_ID}")
            time.sleep(random.uniform(5, 10)) # Human-like delay to avoid 429
            
        except ClientError as e:
            # If the broadcast path fails, this block catches it and tries the 'thread' path
            if "404" in str(e):
                print("⚠️ Broadcast path 404. Switching to Thread-Direct path...")
                try:
                    cl.direct_answer(TARGET_ID, f"{MESSAGE_TEXT} {random.randint(100, 999)}")
                    print("✅ [SUCCESS] Thread-Direct delivered.")
                except Exception as e2:
                    print(f"❌ Critical Failure: {e2}")
            else:
                print(f"⚠️ Instagram block: {e}")
            time.sleep(60)
        except Exception as e:
            print(f"🛑 Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_strike()
