import requests
from bs4 import BeautifulSoup

#----------getting info from i get into pc----------

r=requests.get("https://igetintopc.com");
c=r.content
soup=BeautifulSoup(c,"html.parser")
s=soup.find("a",{"class":"last"}).text
n=int(s)
for j in range(1,2):
    r=requests.get("https://igetintopc.com/page/"+str(j)+"/");
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    a=soup.find_all("a",{"rel":"bookmark"})
    i=0
    for i in range(0,len(a)):
        b=soup.find_all("a",{"rel":"bookmark"})[i].text
        print(b)

#------------getting data from file hippo-------


for k in range(97,121):
    print(str(chr(k)))
    r=requests.get("https://filehippo.com/search?q="+str(chr(k))+"&p=1");
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    a=soup.find_all("a",{"class":"pager-page-link"})[7].text
    l=int(a)

    for j in range(1,l+1):
        r=requests.get("https://filehippo.com/search?q=a&p="+str(j));
        c=r.content
        soup=BeautifulSoup(c,"html.parser")
        t=soup.find_all("span",{"class":"program-title-text"})
        n=len(t)
        print("----------------------------------"+str(n))
        for i in range(0,n):
            s=soup.find_all("span",{"class":"program-title-text"})[i].text
            print(s)
