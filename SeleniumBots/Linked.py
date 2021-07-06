from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


url='https://in.linkedin.com/jobs/search?location=India&geoId=102713980&f_E=1%2C2%2C3%2C4%2C5&currentJobId=2633606587&position=6&pageNum=1'
driver = webdriver.Firefox(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\geckodriver.exe")
driver.get(url)
time.sleep(3)

for i in range(0,10):
    jobs=driver.find_elements_by_class_name("base-card__full-link")[i]
    jobs.send_keys(Keys.RETURN)
    time.sleep(2)

    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser')

    jobsTitle=soup.find("h2",{"class":"top-card-layout__title topcard__title"}).text
    jobsCompany=soup.find("a",{"class":"topcard__org-name-link topcard__flavor--black-link"}).text
    jobsLocation=soup.find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).text

    seniorily_level=""
    employment_type=""
    job_function=""
    industries=""
    jobsData=soup.find_all("li",{"class":"description__job-criteria-item"})
    print(len(jobsData))
    for j in jobsData:
        da=j.find("h3",{"class":"description__job-criteria-subheader"})
        print(da.text)
        if(da.text=="Seniority level"):
            seniorily_level=j.find("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"}).text
        elif(da.text=="Employment type"):
            employment_type=j.find("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"}).text
        elif(da.text=="Job function"):
            job_function=j.find("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"}).text
        elif(da.text=="Industries"):
            industries=j.find("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"}).text
         
            
    print(jobsTitle,jobsCompany,jobsLocation,seniorily_level,employment_type,job_function,industries)
    print("")
