from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


url='https://www.youtube.com/results?search_query=acharya+kaushik+maharaj&sp=EgJAAQ%253D%253D'
driver = webdriver.Chrome(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\chromedriver.exe")
#driver = webdriver.Firefox(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\geckodriver.exe")
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get(url)
time.sleep(3)
driver.find_element_by_xpath('//*[@id="video-title"]').click()
