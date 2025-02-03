# 🔥 Import Everything Needed 🔥
import time
import random
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

warnings.simplefilter("ignore")  # Suppress SSL warnings

# 🔥 YOUR LINKTARGET URL 🔥
URL = "https://link-target.net/1286222/keluna"

# 🔥 Setup WebDriver (Headless Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"user-agent={UserAgent().random}")

# Setup driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 🔥 Click Bot Logic 🔥
def click_farm():
    click_count = 0
    while True:  # Infinite loop
        try:
            print(f"[{click_count+1}] Visiting: {URL}")

            # Open the URL
            driver.get(URL)

            # Wait for ads or "Continue" button
            time.sleep(random.uniform(5, 10))

            try:
                # Click "Next" or "Continue" button if found
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
                )
                next_button.click()
                print("[LOG] Clicked 'Continue' button")
                time.sleep(random.uniform(3, 6))

            except:
                print("[LOG] No 'Continue' button found")

            # Final Wait before closing
            time.sleep(random.uniform(2, 5))
            click_count += 1

        except Exception as e:
            print(f"[ERROR] {e}")
            continue

# 🔥 Start Clicking 🔥
if __name__ == "__main__":
    click_farm()
