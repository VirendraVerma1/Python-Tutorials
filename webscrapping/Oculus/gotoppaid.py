from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import pandas as pd



options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
driver = webdriver.Firefox(executable_path=r'D:\\Programs\\Python_private\\SeleniumBots\\Driver\\geckodriver.exe', options=options)
driver.set_window_size(1024, 600)
driver.maximize_window()

data=[]
def extract_data(url):
        try:
                base_data=[]
                driver.get(url)
                time.sleep(7)
                page = driver.execute_script('return document.body.innerHTML')
                soup = BeautifulSoup(''.join(page), 'html.parser')
                title=soup.find("div",{"class":"app-description__title"}).text
                rating=soup.find("div",{"class":"app-description__review-count"}).text.replace("Ratings", "").replace(" ", "").replace(",", "")
                description=soup.find("div",{"class":"clamped-description__content"}).text
                link=url
                price=soup.find("span",{"class":"app-purchase-price"}).text
                category=soup.find_all("div",{"class":"app-details-row__right"})[4].text
                genre=soup.find_all("div",{"class":"app-details-row__right"})[5].text
                platform=soup.find_all("div",{"class":"app-details-row__right"})[3].text
                publisher=soup.find_all("div",{"class":"app-details-row__right"})[9].text
                website=soup.find_all("div",{"class":"app-details-row__right"})[10].text
                fivestar=soup.find("div",{"class":"app-ratings-histogram"}).find_all("span")[1].text.replace("%", "")
                fourstar=soup.find("div",{"class":"app-ratings-histogram"}).find_all("span")[3].text.replace("%", "")
                threestar=soup.find("div",{"class":"app-ratings-histogram"}).find_all("span")[5].text.replace("%", "")
                twostar=soup.find("div",{"class":"app-ratings-histogram"}).find_all("span")[7].text.replace("%", "")
                onestar=soup.find("div",{"class":"app-ratings-histogram"}).find_all("span")[9].text.replace("%", "")
                base_data.append(title)
                base_data.append(description)
                base_data.append(link)
                base_data.append(category)
                base_data.append(genre)
                base_data.append(platform)
                base_data.append(publisher)
                base_data.append(website)
                base_data.append(rating)
                base_data.append(int(fivestar))
                base_data.append(int(fourstar))
                base_data.append(int(threestar))
                base_data.append(int(twostar))
                base_data.append(int(onestar))
                base_data.append(price)
                data.append(base_data)
        except:
                pass
       
extract_data("https://www.oculus.com/experiences/go/967457083325115/")

# opening the CSV file
with open('gotoppaid.csv', mode ='r')as file:
   
  # reading the CSV file
  csvFile = csv.reader(file)
 
  # displaying the contents of the CSV file
  for lines in csvFile:
        extract_data(lines[0])


df = pd.DataFrame(data, columns=['title',  'description', 'link', 'category', 'genre', 'platform',
                                 'publisher', 'website', 'rating', 'fivestar', 'fourstar', 'threestar', 'twostar', 'onestar','price'])
# Save DataFrame to Excel file
df.to_excel('gotoppaid.xlsx', index=False)