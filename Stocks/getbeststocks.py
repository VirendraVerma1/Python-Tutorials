from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import random
import csv

#cd C:\Users\HP\AppData\Local\Google\Chrome\Application
#chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\ChromeProfile"

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#Change chrome driver path accordingly
chrome_driver = "D:\\Programs\\Python_private\\SeleniumBots\\Driver\\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

#find all the links of the stocks
#get all the scores of the link
#base price

company_name=[]
company_links=[]
company_score=[]
company_baseprice=[]

def save_list_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Example nested list
my_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Save nested list to CSV
save_list_to_csv(my_list, 'my_list.csv')

url="https://www.tickertape.in/screener/equity?src=stocks&subindustry=Power+Transmission+%26+Distribution&stock=TTPW&tab=valuation&ref=stock-peers_compare-screener"
driver.get(url)
time.sleep(1)
jobs=driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div[2]/div[1]/div/div[1]/div/div[1]/button")
jobs.send_keys(Keys.RETURN)
time.sleep(1)

jobss=driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div[2]/div[2]/section/div[2]/div/button")
jobss.send_keys(Keys.RETURN)
time.sleep(3)

"""
for i in range(0,113):
    jobs=driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div[2]/div[2]/section/div[2]/div/button")
    jobs.send_keys(Keys.RETURN)
    time.sleep(3)
"""

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

for i in range(1,4559):
    stock=driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div[2]/div[2]/section/div[2]/section[2]/div[3]/span["+str(i)+"]/span[1]")
    stock.send_keys(Keys.RETURN)
    link=soup.find('a',{'class',"jsx-3587258100 btn-link"}).get('href')
    company_links.append(link)
    print(link)


save_list_to_csv(company_links, 'company.csv')

#chatgpt
def chatgpt(message_prompt):
    url="https://chat.openai.com/"
    driver.get(url)
    lol=random.randrange(0, 4)
    time.sleep(lol)
    element_xpath = "/html/body/div[1]/div[1]/div[2]/div/main/div[3]/form/div/div/textarea"
    element = driver.find_element(By.XPATH, element_xpath)
    element.send_keys(message_prompt)
    element.send_keys(Keys.ENTER)
    time.sleep(30)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    ans=soup.find_all('div',{'class',"flex flex-grow flex-col gap-3"})
    
    print(ans)

#google bard
def googlebard(message_prompt):
    url = "https://bard.google.com/"
    driver.get(url)
    lol=random.randrange(0, 4)
    time.sleep(lol)
    element_xpath = "/html/body/chat-app/side-navigation/mat-sidenav-container/mat-sidenav-content/main/chat-window/div[1]/div[2]/input-area/div/mat-form-field/div[1]/div/div[2]/textarea"
    element = driver.find_element(By.XPATH, element_xpath)
    element.send_keys(message_prompt)
    #element.send_keys("Read the web doc from https://docs.tesseract.in/develop/ , https://docs.tesseract.in/develop/troubleshooting/faqs-develop and go through the sub webpages inside the website and  please provide me the solution for : Hello, I'm having some trouble getting the bottom dock panel buttons functionality to work. I tried implementing the IBackHandler and IHomeHandler interfaces, but the OnBackAction() and OnHomeAction() functions don't seem to be called when I press the Back and Home buttons in the dock")
    element.send_keys(Keys.ENTER)
    time.sleep(15)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    ans=soup.find_all('div',{'class',"markdown"})
    custom_list=[]
    for i in ans:
        custom_list.append(i.text)
    print(custom_list)
    #_ngcontent-ng-c4004291087 markdown

