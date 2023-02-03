import requests
from bs4 import BeautifulSoup
r=requests.get("https://store.steampowered.com/vr/#p=0&tab=TopSellers")
c=r.content
soup=BeautifulSoup(c,"html.parser")
topsellerdiv=soup.find("div",{"class":"TopSellersRows"})
print(topsellerdiv)
#all=soup.find_all("span",{"class":"ccOutputRslt"})[0].text
#print(all)
