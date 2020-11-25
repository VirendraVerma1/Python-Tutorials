import requests
import threading
from bs4 import BeautifulSoup

r=requests.get("https://store.steampowered.com/search/?term=new")
c=r.content
soup=BeautifulSoup(c,"html.parser")
name=soup.find_all("span",{"class":"title"})[0].text
print(name)
