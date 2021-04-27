import requests
import threading
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

for j in range(2,30):
    print("Page",j,"------------------------------------------------------------")
    r=requests.get("https://4movierulz.es/category/multi-audio-dubbed-movies/page/"+str(j)+"/");
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    
    for i in range(len(soup.find_all("div",{"class":"boxed film"}))-2):
        #---------------------------------get Link--------------
        movieLink=soup.find_all("div",{"class":"boxed film"})[i+2].a.get('href')
        print(movieLink)
        
        #-------------------------------get magnet Link------------
        re=requests.get(movieLink);
        cc=re.content
        soupp=BeautifulSoup(cc,"html.parser")
        movieMagnetLink="No Data"
        movieMagnetLink=soupp.find_all("a",{"class":"mv_button_css"})[0].get('href')
        #print(movieMagnetLink)
        
        #------------------------------get movie size-----------------
        movieSize=soupp.find_all("a",{"class":"mv_button_css"})[0].find_all("small")[0].text
        print(movieSize)
        
        #--------------------------get movie name--------------
        nameMovie=soupp.find_all("h2",{"class":"entry-title"})[0].text
        movieTitle=nameMovie
        nameMovie=nameMovie.split("(")
        le=len(nameMovie)-2
        movieName=""
        for k in range(0,le+1):
            movieName=movieName+nameMovie[k]
        movieName=movieName.replace(")","")
        print(movieName)
        
        #--------------------------get movie year--------------
        movieYear=nameMovie[le+1]
        movieYear=movieYear.split(")")
        print(movieYear[0])
        
        #--------------------------get movie languages-----------
        if(movieTitle.find("[") != -1):
            movietest=movieTitle.split("[")
            movietest2=movietest[1].split("]")
            movietest2[0]=movietest2[0].replace("+","|")
        else:
            movietest2[0]="No Data"
        print(movietest2[0])
        
        #--------------------------get movie poster--------------
        moviePoster=soupp.find_all("img",{"class":"attachment-post-thumbnail size-post-thumbnail wp-post-image"})[0].get('src')
        print(moviePoster)
        
        #--------------------------get movie rating--------------
        newName=movieName.replace(" ","+")
        ratingr=requests.get("https://www.imdb.com/find?q="+newName);
        ratingc=ratingr.content
        ratingsoup=BeautifulSoup(ratingc,"html.parser")
        testCheck=ratingsoup.find_all("h1",{"class":"findHeader"})[0].text
        movieRating=""
        movieGenre=""
        if "No results found for" in testCheck:
            movieRatingLink=""
        else:
            movieRatingLink=ratingsoup.find_all("td",{"class":"result_text"})[0].a.get('href')
            movieRatingLink="https://www.imdb.com"+movieRatingLink
            print(movieRatingLink)
            ratingrr=requests.get(movieRatingLink);
            ratingcc=ratingrr.content
            ratingsoupp=BeautifulSoup(ratingcc,"html.parser")
            if(len(ratingsoupp.find_all("span",{"itemprop":"ratingValue"}))>0):
                movieRating=ratingsoupp.find_all("span",{"itemprop":"ratingValue"})[0].text
                
                #---------------------------------genre--------------------------
            if(len(ratingsoupp.find_all("div",{"class":"see-more inline canwrap"}))>0):
                l=len(ratingsoupp.find_all("div",{"class":"see-more inline canwrap"}))
                ll=len(ratingsoupp.find_all("div",{"class":"see-more inline canwrap"})[l-1].find_all("a"))
                print(ll)
                for k in range(ll):
                    movieGenre=movieGenre+ratingsoupp.find_all("div",{"class":"see-more inline canwrap"})[l-1].find_all("a")[k].text
        
        print(movieRating)
        if(not movieGenre == ""):
            movieGenre=movieGenre.replace(" ","|")
            li= list(movieGenre)
            li[0]=""
            movieGenre="".join(li)
        print(movieGenre)
        #--------------------------get movie poster--------------
        movieTrailer=""
        if(len(ratingsoup.find_all("a",{"class":"video-modal"}))>0):
            movieTrailer=ratingsoupp.find_all("a",{"class":"video-modal"})[0].get('href')
        print(movieTrailer)
        
        movieDiscription=""
        movieSizeComapny=""
        Screenshot1=""
        Screenshot2=""
        Screenshot3=""
        movieTrailer=""
        if(movieRating==""):
            moviefloatrate=""
        else:
            moviefloatrate=float(movieRating)
        if(not movieMagnetLink=="No Data"):
            url = 'http://localhost/Movies/Dubbed/insert.php'
            #url="https://torrentodownloader.000webhostapp.com/Movies/Dubbed/insert.php"
            myobj = {'name': movieName,'year': int(movieYear[0]),'description': movieDiscription,
                     'rating': moviefloatrate,'category': movieGenre,'image': moviePoster,
                     'torrent': movieMagnetLink,'sizecompany': movieSizeComapny,'size': movieSize,
                     'screenshot1': Screenshot1,'screenshot2': Screenshot2,'screenshot3': Screenshot3,
                     'trailer': movieTrailer,'language':movietest2[0]}
            x = requests.post(url, data = myobj)
            print(x.text)
        print("\n\n")
