# 🔥 Suppress All Warnings 🔥
import warnings
warnings.simplefilter("ignore")

import time
import random
import requests
import urllib3
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# 🔥 Suppress SSL Warnings 🔥
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 🔥 YOUR SHORTENED LINK 🔥
URL = "https://shrinkme.ink/Kelscrystals"

# ✅ Your Webshare Proxies
PROXIES = [
    "198.23.239.134:6540:bejhiouj:f1pi2mjctcfy",
    "207.244.217.165:6712:bejhiouj:f1pi2mjctcfy",
    "107.172.163.27:6543:bejhiouj:f1pi2mjctcfy",
    "64.137.42.112:5157:bejhiouj:f1pi2mjctcfy",
    "173.211.0.148:6641:bejhiouj:f1pi2mjctcfy",
    "161.123.152.115:6360:bejhiouj:f1pi2mjctcfy",
    "23.94.138.75:6349:bejhiouj:f1pi2mjctcfy",
    "154.36.110.199:6853:bejhiouj:f1pi2mjctcfy",
    "173.0.9.70:5653:bejhiouj:f1pi2mjctcfy",
    "173.0.9.209:5792:bejhiouj:f1pi2mjctcfy"
]

# 🔄 Get a Random Proxy
def get_random_proxy():
    proxy = random.choice(PROXIES)
    ip, port, username, password = proxy.split(":")
    return {
        "http": f"http://{username}:{password}@{ip}:{port}",
        "https": f"http://{username}:{password}@{ip}:{port}",
    }

# 🔄 Get a Random User-Agent
def get_random_user_agent():
    ua = UserAgent()
    return {"User-Agent": ua.random}

# 🏴‍☠️ Infinite Click Bot Logic
def click_farm():
    click_count = 0
    while True:  # Infinite loop
        try:
            proxy = get_random_proxy()
            headers = {
                "User-Agent": get_random_user_agent()["User-Agent"],
                "Referer": "https://google.com",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Connection": "keep-alive",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            print(f"[{click_count+1}] Using proxy: {proxy['http']}")

            # Send a fake "click"
            response = requests.get(URL, headers=headers, proxies=proxy, timeout=10, verify=False, allow_redirects=True)

            if response.status_code == 200:
                print(f"[SUCCESS] Click {click_count+1} sent - Status Code: {response.status_code}")
                click_count += 1

                # Mimic human wait time
                time.sleep(random.uniform(2, 5))
            else:
                print(f"[ERROR] Failed to click {click_count+1} - Status Code: {response.status_code}")

        except Exception as e:
            print(f"[ERROR] {e}")
            continue

if __name__ == "__main__":
    click_farm()

