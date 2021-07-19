from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

#----------------------first page------------
#url="https://www.naukri.com/jobs-in-lucknw?l=lucknw&cityTypeGid=216"
#url="https://www.naukri.com/jobs-in-mumbai?l=mumbai"
url='https://www.naukri.com/jobs-in-bangalore-bengaluru?l=bangalore%2Fbengaluru&jobAge=1&cityTypeGid=6&cityTypeGid=17&cityTypeGid=58&cityTypeGid=72&cityTypeGid=73&cityTypeGid=97&cityTypeGid=105&cityTypeGid=134&cityTypeGid=135&cityTypeGid=138&cityTypeGid=139&cityTypeGid=183&cityTypeGid=187&cityTypeGid=213&cityTypeGid=220&cityTypeGid=242&cityTypeGid=323&cityTypeGid=325&cityTypeGid=349&cityTypeGid=350&cityTypeGid=469&cityTypeGid=505&cityTypeGid=546&cityTypeGid=556&cityTypeGid=9508&cityTypeGid=9509&experience=0'
driver = webdriver.Firefox(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\geckodriver.exe")
driver.get(url)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="root"]/div[3]/div[2]/section[2]/div[1]/div/span[2]/p').click()
driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/section[2]/div[1]/div/span[2]/ul/li[2]').click()
time.sleep(5)
page = driver.execute_script('return document.body.innerHTML')
soup = BeautifulSoup(''.join(page), 'html.parser')

jobs=soup.find_all("article",{"class":"jobTuple bgWhite br4 mb-8"})
for i in jobs:
    #try:
        jobname=i.find("a", {"class": "title fw500 ellipsis"}).text
        jobcompany=i.find("a", {"class": "subTitle ellipsis fleft"}).text
        jobexperince=i.find("li", {"class": "fleft grey-text br2 placeHolderLi experience"}).find("span", {"class": "ellipsis fleft fs12 lh16"}).text
        jobpackage=i.find("li", {"class": "fleft grey-text br2 placeHolderLi salary"}).find("span", {"class": "ellipsis fleft fs12 lh16"}).text
        joblocation=i.find("li", {"class": "fleft grey-text br2 placeHolderLi location"}).find("span", {"class": "ellipsis fleft fs12 lh16"}).text
        jobkeyskill=i.find("ul",{"class":"tags has-description"}).find_all("li", {"class": "fleft fs12 grey-text lh16 dot"})
        keySkills=[]
        
        skillString=""
        for j in jobkeyskill:
            keySkills.append(j.text)
            skillString +=j.text+","
            
        joblink=i.find("a", {"class": "title fw500 ellipsis"}).get('href')

        print(joblink,jobname,jobcompany,jobexperince,jobpackage,joblocation,keySkills)
      
        url = 'http://localhost/placement/insertjob.php'
        #url = 'http://kreasaard.atwebpages.com/PlacementPrepration/insertjob.php'
        myobj = {'CompanyPhoto':"",'CompanyName': jobcompany,'Post': jobname,'Package': jobpackage,
                'Experience': jobexperince,'Bond': "",'Location': joblocation,
                'Role': "",'IndustyType': "",'FunctionalArea': "",
                'EmploymentType': "",'RoleCategory': "",'Education': "",
                'KeySkill': skillString,
                'Responsibility': "",
                'Knowledge': "",
                'Benifit': "",
                'AboutCompany': "",
                'TotalEmployee': "",
                'LastApplyDate': "",
                'ApplyLink': joblink,
                'Description': ""}
        print(myobj)
        x = requests.post(url, data = myobj)
        print(x.text)
        
        print("")
    #except Exception:
        #pass


driver.close()
driver.quit()
