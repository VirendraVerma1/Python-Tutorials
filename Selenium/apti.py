from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
driver = webdriver.Chrome(executable_path="D:\\Programs\\Python_private\\SeleniumBots\\Driver\\chromedriver.exe")
for j in range(1,4):
    url='https://www.indiabix.com/aptitude/probability/06600'+str(j)
    #driver = webdriver.Firefox(executable_path="D:\\Programs\\Python-Tutorials\\SeleniumBots\\Driver\\geckodriver.exe")
    
    driver.get(url)
    time.sleep(3)
    page = driver.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(page), 'html.parser')
    quesdiv=soup.find_all("div",{"class":"bix-div-container"})
    for i in quesdiv:
        question=i.find("td",{"class":"bix-td-qtxt"}).text
        options=i.find_all("td",{"class":"bix-td-option"})
        correct_option=i.find("span",{"class":"jq-hdnakqb mx-bold"}).text
        num_correct_option=0
        option1=options[1].text
        option2=options[3].text
        option3=options[5].text
        option4=options[7].text
        print(question)
        print(option1)
        print(option2)
        print(option3)
        print(option4)
        print(correct_option)
        if(correct_option=="A"):
            num_correct_option=1
        elif(correct_option=="B"):
            num_correct_option=2
        elif(correct_option=="C"):
            num_correct_option=3
        else:
            num_correct_option=4
            
        print(num_correct_option)
        url = 'http://localhost/PlacementPrepration/insertques.php'
        myobj = {'Course':"Aptitude",'Subject': "Probability",'Ques': question,
                        'Option1': option1,'Option2': option2,'Option3': option3,
                        'Option4': option4,'Explanation': "",'Correct': correct_option,
                        'Company': "None",'Publisher': 'Bot','YoutubeLink': "",
                        'by_bot': 1}
        x = requests.post(url, data = myobj)
        print(x.text)
driver.close()
driver.quit()


