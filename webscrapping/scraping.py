import requests
from bs4 import BeautifulSoup
r=requests.get("https://www.x-rates.com/calculator/?from=USD&to=INR&amount=1")
c=r.content
soup=BeautifulSoup(c,"html.parser")

all=soup.find_all("span",{"class":"ccOutputRslt"})[0].text
print(all)
