from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def removeextraspaces(stringg):
    newstr=""
    for i in range(0,len(stringg)-1):
        if((stringg[i]==' ' and stringg[i+1]==' ') or stringg[i]=='\n' or stringg[i]=='\r' or stringg[i]=='\t'):
            pass
        else:
            newstr +=stringg[i]
    return newstr

url='https://in.linkedin.com/jobs/search?keywords=&location=India&locationId=&geoId=102713980&sortBy=DD&f_TPR=&f_E=1%2C2&position=1&pageNum=0'
#driver = webdriver.Chrome(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\chromedriver.exe")
driver = webdriver.Firefox(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\geckodriver.exe")
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get(url)
time.sleep(3)

for i in range(0,20):
    try:
        print("Job index",i)
        jobs=driver.find_elements_by_class_name("base-card__full-link")[i]
        jobs.send_keys(Keys.RETURN)
        time.sleep(2)

        page = driver.execute_script('return document.body.innerHTML')
        soup = BeautifulSoup(''.join(page), 'html.parser')

        
        jobsLink=soup.find("a",{"data-tracking-control-name":"public_jobs_topcard-title"}).get('href')
        jobsTitle=str(soup.find("h2",{"class":"top-card-layout__title topcard__title"}).text).lstrip()
        jobsCompany=soup.find("a",{"class":"topcard__org-name-link topcard__flavor--black-link"}).text
        jobsLocation=soup.find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).text
        jobsDescription=soup.find("div",{"class":"show-more-less-html__markup"}).text

        seniorily_level=""
        employment_type=""
        job_function=""
        industries=""
        jobsData=soup.find_all("li",{"class":"description__job-criteria-item"})
        for j in jobsData:
            da=j.find("h3",{"class":"description__job-criteria-subheader"})
            
            if(da.text=="Seniority level"):
                seniorily_level=j.find("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"}).text
            elif(da.text=="Employment type"):
                employment_type=j.find("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"}).text
            elif(da.text=="Job function"):
                job_function=j.find("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"}).text
            elif(da.text=="Industries"):
                industries=j.find("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"}).text
             
                
        #print(jobsLink)

        #removing extra spaces
        print(jobsTitle+"|"+jobsCompany+"|"+jobsLocation+"|"+seniorily_level+"|"+employment_type,job_function,industries,jobsDescription,jobsLink)
        
        
        #url = 'http://localhost/placement/insertjob.php'
        url = 'http://kreasaard.atwebpages.com/PlacementPrepration/insertjob.php'
        myobj = {'CompanyPhoto':"",'CompanyName': jobsCompany,'Post': jobsTitle,'Package':'',
                    'Experience': seniorily_level,'Bond': "",'Location': jobsLocation,
                    'Role': "",'IndustyType': industries,'FunctionalArea': job_function,
                    'EmploymentType': employment_type,'RoleCategory': '','Education': "",
                    'KeySkill': '',
                    'Responsibility': "",
                    'Knowledge': "",
                    'Benifit': "",
                    'AboutCompany': "",
                    'TotalEmployee': "",
                    'LastApplyDate': "",
                    'ApplyLink': jobsLink,
                    'Description': jobsDescription}
        #print(myobj)
        x = requests.post(url, data = myobj)
        print(x.text)
        print("test1")
    except Exception:
        pass
driver.close()
driver.quit()
