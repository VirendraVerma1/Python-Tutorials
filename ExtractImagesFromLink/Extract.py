import re
import urllib.request
import os

pathDir="D://Programs//Python-Tutorials//ExtractImagesFromLink//"
text_file = open("D:\\Programs\\Python-Tutorials\\ExtractImagesFromLink\\App Store - Creatives.txt", "r")
data = text_file.read()
text_file.close()
myString=data
#myString = "SCREENSHOTS, https://blobstoragepreprod.blob.core.windows.net/graphics/7b8788a2-1046-49ae-9b95-ef04c02a2cb6/preview-2.png SCREENSHOTS, https://blobstoragepreprod.blob.core.windows.net/graphics/7b8788a2-1046-49ae-9b95-ef04c02a2cb6/preview-3.png SCREENSHOTS, https://blobstoragepreprod.blob.core.windows.net/graphics/7b8788a2-1046-49ae-9b95-ef04c02a2cb6/preview-4.png"

def download_jpg(url, file_path, file_name):
    full_path = file_path + file_name + ".jpg"
    urllib.request.urlretrieve(url, full_path)

li=[]
i=0
applist=myString.split("APP TITLE")
for j in applist:
    try:
        appdata=j
        index=appdata.find('ICON')
        appname=appdata[1:index].strip()
        path = os.path.join(pathDir, appname)
        os.mkdir(path)
        path=path+"//"
        count = appdata.count("https")
        print(appname,appdata,count)
        for i in range(0,count):
            url=re.search("(?P<url>https?://[^\s]+)", appdata).group("url")
            print(url)
            appdata = appdata.replace(url, " ")
            download_jpg(url,path,str(i)+"" )
    except:
        pass
