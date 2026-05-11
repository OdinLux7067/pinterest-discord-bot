import feedparser
import requests
import time
import re

# ================== CONFIGURATION ==================
# 1. Aapka Pinterest Board RSS Link
PINTEREST_RSS_URL = "https://www.pinterest.com/singh5478004/pfps.rss"

# 2. Aapka Discord Webhook Link
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1501251726873989241/ZoY62yp7gBcfBAeYHU163mF-oXN_9u5oeu_tM2P1qXtnWcVrwNoO6WxWZE1EztGqRWT8"
# ===================================================

def post_to_discord():
    print(f"[{time.strftime('%H:%M:%S')}] Checking Pinterest for new pins...")
    
    # RSS feed fetch karna
    feed = feedparser.parse(PINTEREST_RSS_URL)
    
    # GitHub Actions mein har baar script fresh chalti hai
    # Isliye hum sirf latest 3 pics bhejenge jo board par sabse upar hain
    new_pics_count = 0
    
    # Latest pins ko check karna (top to bottom)
    for entry in feed.entries:
        if new_pics_count >= 3: # Ek baar mein sirf 3 latest pics
            break
            
        # Image URL nikalna description se
        description = entry.description
        img_match = re.search(r'src="([^"]+)"', description)
        
        if img_match:
            low_res_url = img_match.group(1)
            # High Resolution (Original) link banana
            high_res_url = low_res_url.replace("236x", "originals").replace("564x", "originals").replace("736x", "originals")

            # Discord ko sirf direct Image URL bhejna
            payload = {"content": high_res_url}
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

            if response.status_code == 204:
                print(f"✅ Sent: {high_res_url}")
                new_pics_count += 1
                time.sleep(2) # Discord rate limit se bachne ke liye
            else:
                print(f"❌ Discord Error: {response.status_code}")

if __name__ == "__main__":
    try:
        post_to_discord()
    except Exception as e:
        print(f"⚠️ Error: {e}")
