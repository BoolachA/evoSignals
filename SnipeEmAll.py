from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

# More flexible XPath that looks for text anywhere within div[2]
XPATH_SIGNAL = "//div[contains(., 'MISTAKE') or contains(., 'TALK')]"
# Reduced number of XPATH options for faster checking
XPATH_TAKE_OPTIONS = [
    "/html/body/div/div/div[3]/div/div/div[2]/div[11]/button",  
    "//div[text()='TAKE']",  
    "//div[contains(text(), 'TAKE')]"
]

last_click_time = 0
CLICK_COOLDOWN = 1.5  # 2 seconds cooldown between clicks

def find_and_click_take():
    global last_click_time
    current_time = time.time()
    
    # Check if enough time has passed since last click
    if current_time - last_click_time < CLICK_COOLDOWN:
        return False
        
    for xpath in XPATH_TAKE_OPTIONS:
        try:
            take_element = WebDriverWait(driver, 0.1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            take_element.click()
            last_click_time = current_time  # Update last click time
            time.sleep(0.5)  # Small delay after click to ensure it registers
            return True
        except:
            continue
    return False

def standBy():
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        try:
            signal_element = WebDriverWait(driver, 0.5, 0.1).until(
                EC.presence_of_element_located((By.XPATH, XPATH_SIGNAL))
            )
            
            if signal_element:
                print("Valid signal found, taking action.")
                if find_and_click_take():
                    print("Signal taken successfully")
                    return True
                else:
                    print("Click skipped (cooldown)")
                    return False
        except TimeoutException:
            return False
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-logging')
    
    URL = input("\nDashboard URL: ")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    print("Browser launched")
    
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception as e:
        print(f"Initial page load error: {str(e)}")
    
    waitForSignal = True
    input("Press any button to go on standBy mode")
    
    print("Unlocked, waiting for signals...")
    while waitForSignal:
        if standBy():
            print("\nSignal taken, program locked")
            input("")
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Unlocked, waiting for signals...")
            last_click_time = time.time()  # Reset cooldown after unlocking
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Not valid signal, still waiting...")