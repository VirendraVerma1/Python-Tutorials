from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

for j in range(1,2):
    url='https://www.flipkart.com/search?q=books&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page='+str(j)
    #driver = webdriver.Firefox(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\geckodriver.exe")
    driver = webdriver.Chrome(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\chromedriver.exe")
    driver.get(url)
    time.sleep(3)
    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser')
    jobs=soup.find_all("div",{"class":"_4ddWXP"})
    print(len(jobs))
    for i in jobs:
        try:
            productname=i.find("a",{"class":"s1Q9rs"}).text
            productprice=i.find("div",{"class":"_30jeq3"}).text
            productrating=i.find("div",{"class":"_3LWZlK"}).text
            print(productname,productprice,productrating)
        except Exception:
            pass
    driver.close()
    driver.quit()


