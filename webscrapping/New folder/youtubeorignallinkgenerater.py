from pytube import YouTube as yt
import requests
import threading
from bs4 import BeautifulSoup
r=requests.get("http://localhost/Movies/getyoutube.php");
s=r.text.split(";")
d=8264
while(len(s)>d):
    url=s[d]
    print(d)
    print(url)
    testt=0
    newurl=""
    try:
        vids=yt(url)
        test=vids.streams.all()  # list of all available streams
        newurl=test[0].url
        testt=1
    except:
        print("Something else went wrong")
    
    if(testt==1):
        urll = 'http://localhost/Movies/youtubelinkinsert.php'
        myobj = {'youtube': s[d],'youtubeorignal': newurl}
        x = requests.post(urll, data = myobj)
        print(x.text)
    d=d+1
