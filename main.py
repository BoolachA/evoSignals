from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

#Change this
XPATH_SIGNAL = "//*[@id='dealerName' and (contains(text(), 'MISTAKE') or contains(text(), 'TALK'))]"
XPATH_TAKE = "/html/body/div/a[3]"
DASHBOARD_URL = "https://evotools.onrender.com/"


def standBy():
    #0.25 Seg to find signal type + 0.25 seg to press TAKE.
    #Worst case scenario script will take 0.5 seg to take a valid signal.
    try:
        signal_element = WebDriverWait(driver, 3, 0.25).until(
            EC.presence_of_element_located((
                By.XPATH, 
                XPATH_SIGNAL
            ))
        )
        if signal_element:
            print("Valid signal found, taking action.")
            take_button = WebDriverWait(driver, 3, 0.25).until(
                EC.element_to_be_clickable((By.XPATH, XPATH_TAKE))
            )
            take_button.click()
            return True
        else:
            print("No valid signal found.")
            return False
    except Exception as e:
        print(f"Error: {e}")


if(__name__=="__main__"):
    driver = webdriver.Firefox() 
    driver.get(DASHBOARD_URL)
    print("\nBrowser launched")

    waitForSignal = True
    input("Press any button to go on standBy mode")
    
    print("Unlocked, waiting for signals...")
    while(waitForSignal):
        if(standBy()):
            print("\nSignal taken, program locked")
            input("")
            os.system("cls")
            print("Unlocked, waiting for signals...")
        else:
            print("Not valid signal, still waiting...")
            continue