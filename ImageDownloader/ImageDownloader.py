import pandas as pd
import urllib.request
import time

from PIL import Image
import os

from PIL import Image,ImageFilter

from PyPDF2 import PdfFileMerger

import requests
from bs4 import BeautifulSoup

FilePath="D:/ServerData/Images/Temp/"
FilePathtemp="D:/ServerData/Images/Converted/"
mypath="D:\\Temp\\images\\skins\\cosmetics\\slider"
WebsiteURL="https://big-skins.com/frontend/foxic-html-demo/images/skins/cosmetics/slider/"

def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


#download("https://big-skins.com/frontend/foxic-html-demo/images/skins/fashion/products/product-21-1.webp", dest_folder=FilePath)
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)
for i in onlyfiles:
    s=i.split(".")
    if(s[1]=="png"):
        try:
           download(WebsiteURL+""+s[0]+".webp", dest_folder=FilePath)
           print("downlaoded",WebsiteURL+""+s[0]+".webp")
           im=Image.open(FilePath+"\\"+s[0]+".webp").convert("RGB")
           im.save(FilePathtemp+"\\"+s[0]+".png","png")
        except Exception:
            pass
    if(s[1]=="jpg"):
        try:
           download(WebsiteURL+""+s[0]+".webp", dest_folder=FilePath)
           print("downlaoded",WebsiteURL+""+s[0]+".webp")
           im=Image.open(FilePath+"\\"+s[0]+".webp").convert("RGB")
           im.save(FilePathtemp+"\\"+s[0]+".jpg","jpeg")
        except Exception:
            pass
