import requests
from bs4 import BeautifulSoup

i=0
count=0
companies_len=0
r=requests.get("https://www.moneycontrol.com/markets/indian-indices/top-nse-500-companies-list/7?classic=true");
c=r.content
soup=BeautifulSoup(c,"html.parser")
sensec=soup.find_all("span",{"id":"indcur"})[0].text #getting sensec
print("nifty: "+sensec)
companies=soup.find_all("table",{"class":"responsive"})
companies_len=len(companies);
for j in range(0,1):
    other_len=len(companies[j])
    
    #print(companies[j])
    for i in range(0,500-1):
        print("Name: "+companies[j].find_all("td")[count].find("p").find("a").text)
        count+=1
        print("LTP: "+companies[j].find_all("td")[count].text) #getting ltp
        count+=1
        print("Change: "+companies[j].find_all("td")[count].text) #getting change
        count+=1
        print("Volume: "+ companies[j].find_all("td")[count].text) #getting volume
        count+=1
        print("Buy Price: "+ companies[j].find_all("td")[count].text) #getting volume
        count+=1
        print("Sell Price: "+ companies[j].find_all("td")[count].text) #getting volume
        count+=1
        print("Buy Qty: "+ companies[j].find_all("td")[count].text) #getting volume
        count+=1
        print("Sell Qty: "+ companies[j].find_all("td")[count].text) #getting volume
        count+=1
        print("\n")
