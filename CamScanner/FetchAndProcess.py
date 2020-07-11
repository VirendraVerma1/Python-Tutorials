import pandas as pd
import urllib.request
import time

from PIL import Image
import os

from PIL import Image,ImageFilter

from PyPDF2 import PdfFileMerger

import requests
from bs4 import BeautifulSoup

yy=1
while(yy>0):
    r=requests.get("https://kreasarapps.000webhostapp.com/CamScanner/checkforpdfmaker.php");
    print(r.text)
    try:
        s=r.text.split(";")
        
        imageFilename=[]
        pdfFilename=[]
        mergedFilename=[]
    
        idi=s[len(s)-2]
        groupidi=s[len(s)-3]
        
        filename=""
        FilePath="D:/ServerData/Images/"
        fileNAAM=""
    
        def url_to_jpg(i,url,file_path):
            filename='image-{}.jpg'.format(i)
            full_path='{}{}'.format(file_path,filename)
            urllib.request.urlretrieve(url,full_path)
            print('{} saved.'.format(filename))
            filename
            return filename
    
        def convert_to_pdf(fileName,createName):
            im=Image.open(filename)
            if(im.mode=="RGBA"):
                im=im.convert("RGB")
            new_filename="D:/ServerData/Pdf/"+createName
            if( not os.path.exists(new_filename)):
                im.save(new_filename,"PDF",resolution=100.0)
                print("PDF Created")
    
        for i in range(0,len(s)-3):
            #----------------------------------downloading images
            URL="https://kreasarapps.000webhostapp.com/CamScanner/Images/"+s[i]
            fileNAAM=url_to_jpg(i,URL,FilePath)
            imageFilename.append(fileNAAM)
    
            #------------------------------applying filters
            #image=Image.open(r"D:/ServerData/Images/"+fileNAAM)
            #image = image.convert('1')
            #image=image.filter(ImageFilter.SHARPEN)
            #image=image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            #image.save("D:/ServerData/Images/"+fileNAAM)
            
            #-------------------------------creating pdf
            filename=FilePath+fileNAAM
            pdfname="test"+str(i)+".pdf"
            pdfFilename.append(pdfname)
            convert_to_pdf(filename,pdfname)
    
        # merge two pdf
        path="D:/ServerData/Pdf/"
        pdf_files=pdfFilename
        merger=PdfFileMerger()
        for files in pdf_files:
            merger.append(path+files)
        if( not os.path.exists(path+'MergedPdf/merged.pdf')):
            merger.write(path+'MergedPdf/merged.pdf')
            print("merged")
        merger.close()
        
        #-----------------------------send and change the pdf make values--------------
        print("Group Id",groupidi)
        print("User ID",idi)
        url="https://kreasarapps.000webhostapp.com/CamScanner/uploadpdf.php"
        filess={
            'theFile' : open('D:/ServerData/Pdf/MergedPdf/merged.pdf','rb')
        }
        values = {'id':idi,'groupId':groupidi}
        print("sending pdf")
        r=requests.post(url,files=filess,data=values)
        print(r.status_code)
        print(r.text)
        
        #---------------------------delete files---------------------
        #--remove merged pdf
        
        print("Removing")
        
        filee = 'merged.pdf'
        locationn = "D:/ServerData/Pdf/MergedPdf/"
        path = os.path.join(locationn, filee) 
        
        os.remove(path)
        print("works")
        #remove all images
        for i in range(0,len(imageFilename)):
            os.remove("D:/ServerData/Images/"+imageFilename[i])
        
        #remove all pdf
        for i in range(0,len(pdfFilename)):
            os.remove("D:/ServerData/Pdf/"+pdfFilename[i])
        
        
        print("All the files are removed")
    except Exception:
        pass
    yy=0
    time.sleep(3)
