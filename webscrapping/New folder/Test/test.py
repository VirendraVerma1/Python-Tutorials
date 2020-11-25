import requests
import threading
from bs4 import BeautifulSoup
import subprocess
import webbrowser
import sys


mainlink="https://www.xvideos4.com"
sumblink="https://www.xvideos4.com/tags/xvideos"
r=requests.get(sumblink)
c=r.content
soup=BeautifulSoup(c,"html.parser")
name=soup.find_all("p",{"class":"title"})[0].find_all("a")[0].text
print(name)
link=soup.find_all("p",{"class":"title"})[0].find_all("a")[0].get('href')
print(mainlink+link)

#get video
rr=requests.get(mainlink+link)
cc=rr.content
soupp=BeautifulSoup(cc,"html.parser")
#videolink=soupp.find_all("div",{"id":"html5video"})[0].text
#print(videolink)


url = mainlink+link
if sys.platform == 'darwin':    # in case of OS X
    subprocess.Popen(['open', url])
else:
    webbrowser.open_new_tab(url)
