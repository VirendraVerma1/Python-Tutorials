from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

n=20
while(n>0):
    url='https://www.youtube.com/watch?v=LVONKEliDew&ab_channel=KreaSaarGames'
    driver = webdriver.Chrome(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\chromedriver.exe")
    driver.get(url)
    time.sleep(10)
    print("sar")
    elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "ytp-play-button ytp-button")))
    print("1")
    elements.click()
    print("2")
    time.sleep(60)
    driver.close()
    driver.quit()
