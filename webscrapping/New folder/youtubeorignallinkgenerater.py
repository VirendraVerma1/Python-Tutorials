from pytube import YouTube as yt
import requests
import threading
from bs4 import BeautifulSoup
r=requests.get("http://localhost/Movies/getyoutube.php");
s=r.text.split(";")
d=0
def GetData(asd):
    d=asd
    while(asd+difference>d):
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
            print(newurl)
        except:
            print("Something else went wrong")
            
        if(testt==1):
            urll = 'http://localhost/Movies/youtubelinkinsert.php'
            myobj = {'youtube': s[d],'youtubeorignal': newurl}
            x = requests.post(urll, data = myobj)
            print(x.text)
        d=d+1
rangeCompleted=0
difference=500

# creating thread 
t1 = threading.Thread(target=GetData, args=(rangeCompleted,)) 
t2 = threading.Thread(target=GetData, args=(rangeCompleted+difference*1-1,))
t3 = threading.Thread(target=GetData, args=(rangeCompleted+difference*2-1,))
t4 = threading.Thread(target=GetData, args=(rangeCompleted+difference*3-1,))
t5 = threading.Thread(target=GetData, args=(rangeCompleted+difference*4-1,))
t6 = threading.Thread(target=GetData, args=(rangeCompleted+difference*5-1,))
t7 = threading.Thread(target=GetData, args=(rangeCompleted+difference*6-1,))
t8 = threading.Thread(target=GetData, args=(rangeCompleted+difference*7-1,))
t9 = threading.Thread(target=GetData, args=(rangeCompleted+difference*8-1,))
t10 = threading.Thread(target=GetData, args=(rangeCompleted+difference*9-1,))
t11 = threading.Thread(target=GetData, args=(rangeCompleted+difference*10-1,))
t12 = threading.Thread(target=GetData, args=(rangeCompleted+difference*11-1,))
t13 = threading.Thread(target=GetData, args=(rangeCompleted+difference*12-1,))
t14 = threading.Thread(target=GetData, args=(rangeCompleted+difference*13-1,))
t15 = threading.Thread(target=GetData, args=(rangeCompleted+difference*14-1,))
t16 = threading.Thread(target=GetData, args=(rangeCompleted+difference*15-1,))
t16 = threading.Thread(target=GetData, args=(rangeCompleted+difference*16-1,))
t17 = threading.Thread(target=GetData, args=(rangeCompleted+difference*17-1,))
t18 = threading.Thread(target=GetData, args=(rangeCompleted+difference*18-1,))
t19 = threading.Thread(target=GetData, args=(rangeCompleted+difference*19-1,))
t20 = threading.Thread(target=GetData, args=(rangeCompleted+difference*20-1,))
t21 = threading.Thread(target=GetData, args=(rangeCompleted+difference*21-1,))
t22 = threading.Thread(target=GetData, args=(rangeCompleted+difference*22-1,))
t23 = threading.Thread(target=GetData, args=(rangeCompleted+difference*23-1,))
t24 = threading.Thread(target=GetData, args=(rangeCompleted+difference*24-1,))
t25 = threading.Thread(target=GetData, args=(rangeCompleted+difference*25-1,))
t26 = threading.Thread(target=GetData, args=(rangeCompleted+difference*26-1,))
t27 = threading.Thread(target=GetData, args=(rangeCompleted+difference*27-1,))
t28 = threading.Thread(target=GetData, args=(rangeCompleted+difference*28-1,))
t29 = threading.Thread(target=GetData, args=(rangeCompleted+difference*29-1,))
t30 = threading.Thread(target=GetData, args=(rangeCompleted+difference*30-1,))

# starting thread 1 
t1.start() 
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()
t11.start()
t12.start()
t13.start()
t14.start()
t15.start()
t16.start()
t17.start() 
t18.start()
t19.start()
t20.start()
t21.start()
t22.start()
t23.start()
t24.start()
t25.start()
t26.start()
t27.start()
t28.start()
t29.start()
t30.start()

    
t1.join() 
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
t9.join()
t10.join()
t11.join()
t12.join()
t13.join()
t14.join()
t15.join()
t16.join()
t17.join() 
t18.join()
t19.join()
t20.join()
t21.join()
t22.join()
t23.join()
t24.join()
t25.join()
t26.join()
t27.join()
t28.join()
t29.join()
t30.join()


print("done")
