import requests
import threading
from bs4 import BeautifulSoup

i=0
count=0
companies_len=0
li_Name=[]
li_Year=[]
li_Rating=[]
li_Category=[]
li_Image=[]
li_MagnetLink=[]
li_SizeCompany=[]
li_Size=[]
li_ScreenShot1=[]
li_ScreenShot2=[]
li_ScreenShot3=[]
li_trailer=[]
li_description=[]

def callsa(rangea):
    for j in range(rangea,rangea+difference):
        print("Page ",j)
        r=requests.get("https://yts.mx/browse-movies?page="+str(j));
        c=r.content
        soup=BeautifulSoup(c,"html.parser")
        for i in range(0,19):
            movieName=soup.find_all("a",{"class":"browse-movie-title"})[i].text

            movieYear=soup.find_all("div",{"class":"browse-movie-year"})[i].text


            movieRating=soup.find_all("h4",{"class":"rating"})[i].text


            if(len(soup.find_all("figcaption",{"class":"hidden-xs hidden-sm"})[i].find_all("h4"))>1):
                movieCategory1=soup.find_all("figcaption",{"class":"hidden-xs hidden-sm"})[i].find_all("h4")[1].text
                movieCategory2=""
                if(len(soup.find_all("figcaption",{"class":"hidden-xs hidden-sm"})[i].find_all("h4"))>2):
                    movieCategory2=soup.find_all("figcaption",{"class":"hidden-xs hidden-sm"})[i].find_all("h4")[2].text
                if(not movieCategory2 ==""):
                    movieCategory=movieCategory1+" | "+movieCategory2
                else:
                    movieCategory=movieCategory1
            else:
                movieCategory="No Data"



            movieImage=soup.find_all("img",{"class":"img-responsive"})[i].get('src')


            #getting magnet link ------------------------------
            newURL=soup.find_all("a",{"class":"browse-movie-link"})[i].get('href')
            print(newURL)
            rr=requests.get(newURL);
            cc=rr.content
            soupp=BeautifulSoup(cc,"html.parser")
            movieTorrent="No Data"
            if(len(soupp.find_all("a",{"class":"magnet-download download-torrent magnet"}))>0):
                movieTorrent=soupp.find_all("a",{"class":"magnet-download download-torrent magnet"})[0].get('href')


            movieSizeComapny="No Data"
            if(len(soupp.find_all("p",{"class":"quality-size"}))>0):
                movieSizeComapny=soupp.find_all("p",{"class":"quality-size"})[0].text


            movieSize="No Data"
            if(len(soupp.find_all("p",{"class":"quality-size"}))>0):
                movieSize=soupp.find_all("p",{"class":"quality-size"})[1].text



            #   getting screen shot URL --------------------
            Screenshot1="No data"
            Screenshot2="No data"
            Screenshot3="No data"
            n=len(soupp.find_all("a",{"class":"screenshot-group imghov cboxElement"}))
            if(n>0):
                Screenshot1=soupp.find_all("a",{"class":"screenshot-group imghov cboxElement"})[0].find_all("img")[0].get('src')

            if(n>1):
                Screenshot2=soupp.find_all("a",{"class":"screenshot-group imghov cboxElement"})[1].find_all("img")[0].get('src')

            if(n>2):
                Screenshot3=soupp.find_all("a",{"class":"screenshot-group imghov cboxElement"})[2].find_all("img")[0].get('src')



            #getting youtube trailer URL--------------------------
            movieTrailer="No Data"
            if(len(soupp.find_all("a",{"class":"youtube cboxElement"}))>0):
                movieTrailer=soupp.find_all("a",{"class":"youtube cboxElement"})[0].get('href')


            movieDiscription="No Data"
            if(len(soupp.find_all("p",{"class":"hidden-xs"}))>0):
                movieDiscription=soupp.find_all("p",{"class":"hidden-xs"})[1].text

            movieRating=movieRating.replace(" / 10","")
            movieRating=movieRating.replace(" ","")

            movieName=movieName.replace(",","")
            movieDiscription=movieDiscription.replace("'","")
            movieDiscription=movieDiscription.replace(","," ")
            
            if(not movieTorrent=="No Data"):
                li_Name.append(movieName)
                li_Year.append(int(movieYear))
                li_Rating.append(float(movieRating))
                li_Category.append(movieCategory)
                li_Image.append(movieImage)
                li_ScreenShot3.append(Screenshot1)
                li_ScreenShot2.append(Screenshot2)
                li_ScreenShot1.append(Screenshot3)
                li_trailer.append(movieTrailer)
                li_Size.append(movieSize)
                li_SizeCompany.append(movieSizeComapny)
                li_MagnetLink.append(movieTorrent)
                li_description.append(movieDiscription)
                
                #url = 'https://kreasarapps.000webhostapp.com//Movies/insert.php'
                url = 'http://localhost/Movies/insert.php'
                
                myobj = {'name': movieName,'year': int(movieYear),'description': movieDiscription,
                         'rating': float(movieRating),'category': movieCategory,'image': movieImage,
                         'torrent': movieTorrent,'sizecompany': movieSizeComapny,'size': movieSize,
                         'screenshot1': Screenshot1,'screenshot2': Screenshot2,'screenshot3': Screenshot3,
                         'trailer': movieTrailer}
                x = requests.post(url, data = myobj)
                print(x.text)
                
   


rangeMax=870
rangeMin=1
rangeCompleted=1
#callsa(rangeCompleted)
difference=25
if __name__ == "__main__": 
    # creating thread 
    t1 = threading.Thread(target=callsa, args=(rangeCompleted,)) 
    t2 = threading.Thread(target=callsa, args=(rangeCompleted+difference*1-1,))
    t3 = threading.Thread(target=callsa, args=(rangeCompleted+difference*2-1,))
    t4 = threading.Thread(target=callsa, args=(rangeCompleted+difference*3-1,))
    t5 = threading.Thread(target=callsa, args=(rangeCompleted+difference*4-1,))
    t6 = threading.Thread(target=callsa, args=(rangeCompleted+difference*5-1,))
    t7 = threading.Thread(target=callsa, args=(rangeCompleted+difference*6-1,))
    t8 = threading.Thread(target=callsa, args=(rangeCompleted+difference*7-1,))
    t9 = threading.Thread(target=callsa, args=(rangeCompleted+difference*8-1,))
    t10 = threading.Thread(target=callsa, args=(rangeCompleted+difference*9-1,))
    t11 = threading.Thread(target=callsa, args=(rangeCompleted+difference*10-1,))
    t12 = threading.Thread(target=callsa, args=(rangeCompleted+difference*11-1,))
    t13 = threading.Thread(target=callsa, args=(rangeCompleted+difference*12-1,))
    t14 = threading.Thread(target=callsa, args=(rangeCompleted+difference*13-1,))
    t15 = threading.Thread(target=callsa, args=(rangeCompleted+difference*14-1,))
    t16 = threading.Thread(target=callsa, args=(rangeCompleted+difference*15-1,))
    t16 = threading.Thread(target=callsa, args=(rangeCompleted+difference*16-1,))
    t17 = threading.Thread(target=callsa, args=(rangeCompleted+difference*17-1,))
    t18 = threading.Thread(target=callsa, args=(rangeCompleted+difference*18-1,))
    t19 = threading.Thread(target=callsa, args=(rangeCompleted+difference*19-1,))
    t20 = threading.Thread(target=callsa, args=(rangeCompleted+difference*20-1,))
    t21 = threading.Thread(target=callsa, args=(rangeCompleted+difference*21-1,))
    t22 = threading.Thread(target=callsa, args=(rangeCompleted+difference*22-1,))
    t23 = threading.Thread(target=callsa, args=(rangeCompleted+difference*23-1,))
    t24 = threading.Thread(target=callsa, args=(rangeCompleted+difference*24-1,))
    t25 = threading.Thread(target=callsa, args=(rangeCompleted+difference*25-1,))
    t26 = threading.Thread(target=callsa, args=(rangeCompleted+difference*26-1,))
    t27 = threading.Thread(target=callsa, args=(rangeCompleted+difference*27-1,))
    t28 = threading.Thread(target=callsa, args=(rangeCompleted+difference*28-1,))
    t29 = threading.Thread(target=callsa, args=(rangeCompleted+difference*29-1,))
    t30 = threading.Thread(target=callsa, args=(rangeCompleted+difference*30-1,))
    t31 = threading.Thread(target=callsa, args=(rangeCompleted+difference*31-1,))
    t32 = threading.Thread(target=callsa, args=(rangeCompleted+difference*32-1,))
    t33 = threading.Thread(target=callsa, args=(rangeCompleted+difference*33-1,))
  
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
    t31.start()
    t32.start()
    t33.start()
    
     
  
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
    t31.join()
    t32.join()
    t33.join()
    
    print("Done!") 
    


import pandas as pd    
from pandas import DataFrame

d = {'MovieName':li_Name,'Year':li_Year,'Category':li_Category,'Rating':li_Rating,'Image':li_Image,'ScreenShot1':li_ScreenShot1,'ScreenShot2':li_ScreenShot2,'ScreenShot3':li_ScreenShot3,'Trailer':li_trailer,'Description':li_description,'MagnetLink':li_MagnetLink,'CompanySize':li_SizeCompany,'Size':li_Size}
df = pd.DataFrame(d)
df.to_csv('Movies.csv', header=False, index=False)
df = DataFrame(d, columns= ['MovieName', 'Year', 'Category', 'Rating', 'Image', 'ScreenShot1', 'ScreenShot2', 'ScreenShot3', 'Trailer', 'Description', 'MagnetLink', 'CompanySize', 'Size'])
df.to_json (r'M.json')
print(df)
