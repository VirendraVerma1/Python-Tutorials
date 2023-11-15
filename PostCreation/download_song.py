import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#Change chrome driver path accordingly
chrome_driver = "D:\\Programs\\Python_private\\SeleniumBots\\Driver\\chromedriver.exe"

# Use the Chrome class instead of the WebDriver class
driver = webdriver.Chrome(options=chrome_options)
 
# opening the CSV file
with open('mobcup.csv', mode ='r')as file:
   
  # reading the CSV file
  csvFile = csv.reader(file)
 
  # displaying the contents of the CSV file
  for lines in csvFile:
    try:
        newurl=lines[1]+"/download/mp3"
        print(newurl)
        driver.get(newurl)
        time.sleep(2)
    except:
       pass