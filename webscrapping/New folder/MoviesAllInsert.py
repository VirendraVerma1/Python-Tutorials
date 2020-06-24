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
    for j in range(2,50):
        print("Page ",j)
        #r=requests.get("https://yts.mx/browse-movies/0/all/all/0/rating/0/all");
        r=requests.get("https://yts.mx/browse-movies/0/all/all/0/rating/2018/all?page="+str(j));
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
                #url = 'http://localhost/Movies/insert.php'
                url = 'https://torrentodownloader.000webhostapp.com/Movies/insert.php'
                myobj = {'name': movieName,'year': int(movieYear),'description': movieDiscription,
                         'rating': float(movieRating),'category': movieCategory,'image': movieImage,
                         'torrent': movieTorrent,'sizecompany': movieSizeComapny,'size': movieSize,
                         'screenshot1': Screenshot1,'screenshot2': Screenshot2,'screenshot3': Screenshot3,
                         'trailer': movieTrailer}
                x = requests.post(url, data = myobj)
                print(x.text)
                
   


rangeMax=2
rangeMin=1
rangeCompleted=1
callsa(rangeCompleted)

print("Done!") 
    


import pandas as pd    
from pandas import DataFrame

d = {'MovieName':li_Name,'Year':li_Year,'Category':li_Category,'Rating':li_Rating,'Image':li_Image,'ScreenShot1':li_ScreenShot1,'ScreenShot2':li_ScreenShot2,'ScreenShot3':li_ScreenShot3,'Trailer':li_trailer,'Description':li_description,'MagnetLink':li_MagnetLink,'CompanySize':li_SizeCompany,'Size':li_Size}
df = pd.DataFrame(d)
df.to_csv('Movies.csv', header=False, index=False)
df = DataFrame(d, columns= ['MovieName', 'Year', 'Category', 'Rating', 'Image', 'ScreenShot1', 'ScreenShot2', 'ScreenShot3', 'Trailer', 'Description', 'MagnetLink', 'CompanySize', 'Size'])
df.to_json (r'M.json')
print(df)
