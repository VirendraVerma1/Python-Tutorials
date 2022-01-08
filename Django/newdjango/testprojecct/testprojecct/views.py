from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from testprojecct import models

def homepage(request):
    face_datas=models.FaceData.objects.all()
    
    res=render(request,'index.html',{'face_datas':face_datas})
    return res

def update_my_data(request):
    face_data=models.FaceData.objects.get(image_username=request.GET['id'])
    face_data.image_path="world"
    face_data.save()
    return face_data.image_path

def create_new_data(request):
    mydata=models.FaceData()
    mydata.image_path="hello"
    mydata.image_username="hello"
    mydata.image_user_base_id=1
    mydata.image_is_downloaded=1
    mydata.save()

def homepagetest(request):
    s="<h1>Hello world</h1>"
    li=[]
    for i in range(0,10):
        li.append(i)
    res=render(request,'homepage.html',{'li':li,'s':s})
    return res

def check_api(request):
    s="hello world"
    return s