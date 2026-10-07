# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D8E8E13C5AC3257471DEF50933479C5CAB78E4A1B866DC655F296F353CB51A5658575D819524DC943767AF8050D00A777AD8B08B2C76BECEB5D3D954E683712BB5D04B6D0A77ACEFF0A8710F6CFC914868299F3408274574725BC9D4F9378EF768424D4F038937B1C468DA0A88F248428335E3C160F3DECD2D4EFB5B190DB1448EB22510F0C50CFD2BE4B090294DD830EA0AC616E36B4501A2F90CC5294C1689A51BF13C5F5ABBFC592CE92B946278510D5A09BA3A813E7574D2AA909C3D35C094919CAA28E9B4E8ACA31E9A837D1F95F912C1B0476BBFF24085D06AE0A2E920D545519A7DA9D7423CA5886FBE070034F950694B89C0AA66EBA128A2B1BACC595B49063BF199945C874325D4AC6375B1EC00A98EAD0F4D1F54CF884697FBF4A132D0304B390F602EAFA6DFA8FF024386297DB94C72C2F6965DCCDAF79D6E37A9A285DE7110BC3FAA1B40D80FE6E8CD814A898A10FC95A3641BA1A842C6C6E731E8A46F33EFAF970F150B24501ECB3CCA3F4B13413C8EBBDBB5938AD1350419116179B895A8A15D664D3FE108AB190D708182C152AB531AFD88B529629683EE67"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
