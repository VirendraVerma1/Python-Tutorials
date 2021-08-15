from jinja2 import Environment, BaseLoader
import imgkit
import random
import requests
import json
from PIL import Image
import os
from os import listdir
from os.path import isfile, join    

unsortedimage="D:\\Programs\\Python-Tutorials\\MakeImagePost\\UnSortedImage"
imagetocropdirpath="D:\\Programs\\Python-Tutorials\\MakeImagePost\\ImagesToCrop"
croppedimagedirpath="D:\\Programs\\Python-Tutorials\\MakeImagePost\\CropedImage"
completedpostdirpath="D:\\Programs\\Python-Tutorials\\MakeImagePost\\CompletedPost"

path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
html_location='D:\\Programs\\Python-Tutorials\\MakeImagePost\\basichtml.html'

message_list=[
    'Hello world',
    'How are you',
    'I am fine',
    'What are you doing'
]


def read_and_store_all_the_files(fromfolder):
    onlyfiles = [f for f in listdir(fromfolder) if isfile(join(fromfolder, f))]
    return onlyfiles

def remove_all_files(directory):
    onlyfiles=read_and_store_all_the_files(directory)
    for i in onlyfiles:
        os.remove(directory+"\\"+i)

def makeimagecropfromfolder():
    onlyfiles=read_and_store_all_the_files(imagetocropdirpath)
    remove_all_files(croppedimagedirpath)
    counter=1
    for i in onlyfiles:
        try:
            img = Image.open(imagetocropdirpath+"\\"+i)
            width, height = img.size
            size_height=height
            size_width=width

            min_width_size=(width/2.0)-540
            min_height_size=(height/2.0)-540


            #print(size_width-min_size,min_size,size_height)
            img_left_area = (min_width_size,min_height_size, min_width_size+1080, min_height_size+1080)
            img_left = img.crop(img_left_area)

            img_left.save(croppedimagedirpath+"\\"+str(counter)+".jpg")
            counter+=1
        except:
            pass
        
    
def rename_all_the_files():
    onlyfiles=read_and_store_all_the_files(unsortedimage)

    for i in range(0,len(onlyfiles)):
        os.rename(unsortedimage+"\\"+onlyfiles[i],imagetocropdirpath+"\\"+str(i+1)+".jpg") 



def createQuoteImg(msg_body,image_location):
    onlyfiles=read_and_store_all_the_files(croppedimagedirpath)
    content = dict(
        background_img_path=croppedimagedirpath+"\\"+random.choice(onlyfiles),
        description=msg_body,
        )

    HTML="""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="imgkit-format" content="png"/>
        <meta name="imgkit-orientation" content="Landscape"/>
        <style type="text/css">

        .bottom-left{
            position:absolute;
            bottom:250px;
            left:100px;
            width:60%;
            font-size:50px;
            line-height:150%;
            color:#000;
        }

        .top-right{
            position:absolute;
            top:60px;
            right:68px;
            width:100px;
        }
        </style>


        </head>
        <body >
        <div class="container">
            <img src="{{background_img_path}}" style="width:100%;">
            <div class="bottom-left"><p>"{{description}}"</p></div>
        </div>
        </body>
        </html>
        """

    #imgkit.from_string(HTML, image_location, config=config)

    rtemplate = Environment(loader=BaseLoader).from_string(HTML)
    rendered_output = rtemplate.render(**content)
    #rendered_output=Environment().form_string(HTML).from_string(HTML).render(**content)

    with open(html_location,'w', encoding='utf8') as f:
        f.write(rendered_output)

    options={
            'encoding':"UTF-8",
            "enable-local-file-access":None,
            'custom-header':[
                ('Accept-Encoding','gzip')
            ],
        }

    imgkit.from_file(html_location,image_location,options)


def make_themes_from_message():
    remove_all_files(completedpostdirpath)
    counter=1
    for i in message_list:
        createQuoteImg(i,completedpostdirpath+"\\"+str(counter)+".jpg")
        counter+=1

#rename_all_the_files()
#makeimagecropfromfolder()
make_themes_from_message()
