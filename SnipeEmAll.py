from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os


XPATH_SIGNAL = "//div[contains(., 'MISTAKE') or contains(., 'TALK')]"
# Multiple strategies for finding the take button cuz im dumb
# WARNING: IF ANOTHER SIGNAL IS TRIGGERED AT THE SAME TIME AS MISTAKE/TALK, THIS SCRIPT WILL TAKE THE FIRST SIGNAL.
XPATH_TAKE_OPTIONS = [
    "/html/body/div/div/div[3]/div/div/div[2]/div[11]/button",  # Original path
    "//button[contains(text(), 'TAKE')]",  # Button with TAKE text
    "//div[text()='TAKE']",  # Div with exact TAKE text
    "//div[contains(text(), 'TAKE')]",  # Div containing TAKE
    "//button[text()='TAKE']"  # Button with exact TAKE text
]

def find_and_click_take():
    for xpath in XPATH_TAKE_OPTIONS:
        try:
            take_element = WebDriverWait(driver, 0.2).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            print(f"Found TAKE element using xpath: {xpath}")
            take_element.click()
            return True
        except:
            continue
    return False

def standBy():
    try:
        WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        try:
            signal_element = WebDriverWait(driver, 0.5, 0.1).until(
                EC.presence_of_element_located((By.XPATH, XPATH_SIGNAL))
            )
            
            if signal_element:
                print("Valid signal found, taking action.")
                print(f"Signal text: {signal_element.text}")  # Debug info
                
                if find_and_click_take():
                    print("Successfully clicked TAKE")
                    return True
                else:
                    print("Failed to find or click TAKE button")
                    return False
        except TimeoutException:
            return False
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print("DOM structure:")
        try:
            print("Current page content:")
            print(driver.page_source)
        except:
            pass
        return False

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    URL = input("\nDashboard URL: ")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    print("Browser launched")
    
    # Wait for initial page load
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
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Not valid signal, still waiting...")