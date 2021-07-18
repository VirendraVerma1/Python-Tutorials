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
    serchItem="motivational video"
    url='https://www.youtube.com'
    driver = webdriver.Chrome(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\chromedriver.exe")
    driver.get(url)
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    time.sleep(2)
    search_field=driver.find_element_by_name("search_query")
    search_field.send_keys(serchItem)
    search_field.send_keys(Keys.RETURN)
    time.sleep(5)
    #viedeo=driver.find_elements_by_id("video-title")[0]
    #viedeo.click()
   
    #WebDriverWait(driver,30).until(EC.title_contains(serchItem))style-scope ytd-video-renderer
    WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.ID,"img"))).click()
    
    time.sleep(60)
    driver.close()
    driver.quit()
