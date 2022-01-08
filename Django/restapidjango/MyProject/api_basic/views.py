from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article, Face_data
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from .serializers import ArticleSerializer, FaceSerialier

#face recognition
import face_recognition
import cv2
import numpy as np
import glob
import pickle
from PIL import Image, ImageDraw
from face_recognition.api import face_encodings, face_locations
import PIL
import time
import requests
import urllib.request


@api_view(['GET','POST'])
def face_data(request):
    
    if(request.method=='GET'):
        articles=Face_data.objects.all()
        serializer=FaceSerialier(articles,many=True)
        return Response(serializer.data)

    elif(request.method=='POST'):#add new row
        serializer=FaceSerialier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def face_data_detail(request,pk):
    
    try:
        article = Face_data.objects.get(pk=pk)

    except Face_data.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if(request.method=='GET'):
        serializer=FaceSerialier(article)
        return Response(serializer.data)

    elif(request.method=='PUT'):
        serializer=FaceSerialier(article,data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif(request.method=='DELETE'):
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET'])
def compare_faces(request):

    img_path='https://cdn.vox-cdn.com/thumbor/WCH_hpmDktgoM_vsNb4QGWr2s8k=/0x104:438x396/1400x1050/filters:focal(0x104:438x396):format(jpeg)/cdn.vox-cdn.com/imported_assets/846336/steve-jobs.jpeg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    test_image=face_recognition.load_image_file(response)
    face_locations=face_recognition.face_locations(test_image)
    face_encodings=face_recognition.face_encodings(test_image,face_locations)

    # img_path1='https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Steve_Jobs.jpg/527px-Steve_Jobs.jpg' #this thing will be come from the server
    img_path1='https://thumbor.forbes.com/thumbor/fit-in/416x416/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5f4ebe0c87612dab4f12a597%2F0x0.jpg' #this thing will be come from the server
    response1 = urllib.request.urlopen(img_path1)
    test_image1=face_recognition.load_image_file(response1)
    face_locations1=face_recognition.face_locations(test_image1)
    face_encodings1=face_recognition.face_encodings(test_image1,face_locations1)
    name="Unknown Person"
    for(top, right,bottom,left),face_encoding in zip(face_locations,face_encodings):
        matches=face_recognition.compare_faces(face_encodings1,face_encoding)

        name="Unknown Person"

        if True in matches:
            name="Steve"
            return Response(name)
    return Response(name)
    #load the database data
    image_path_li=[]
    image_username_li=[]
    image_encodes=[]
    face_datas=Face_data.objects.all()
    serializer=FaceSerialier(face_datas,many=True)
    #return Response(serializer.data[0].image_path)
    fdata=serializer.data[:]
    for i in fdata:
        image_path_li.append(i['image_path'])
        image_username_li.append(i['image_username'])
        temp_image=face_recognition.load_image_file(i['image_path'])
        temp_encode=face_recognition.face_encodings(temp_image)[0]    
        image_encodes.append(temp_encode)
        
    

    img_path='https://cdn.vox-cdn.com/thumbor/WCH_hpmDktgoM_vsNb4QGWr2s8k=/0x104:438x396/1400x1050/filters:focal(0x104:438x396):format(jpeg)/cdn.vox-cdn.com/imported_assets/846336/steve-jobs.jpeg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    test_image=face_recognition.load_image_file(response)
    face_locations=face_recognition.face_locations(test_image)
    face_encodings=face_recognition.face_encodings(test_image,face_locations)
    name="Unknown Person"
    for(top, right,bottom,left),face_encoding in zip(face_locations,face_encodings):
        matches=face_recognition.compare_faces(image_encodes,face_encoding)

        name="Unknown Person"

        if True in matches:
            first_match_index=matches.index(True)
            name=image_username_li[first_match_index] 
            return Response(name)

    return Response(name)
# @csrf_exempt
# def my_first_test(request,pk):
#     try:
#         face_data = Face_data.objects.get(pk=pk)

#     except Face_data.DoesNotExist:
#         return HttpResponse(status=404)

#     if(request.method=='POST'):#add new row
#         mydata=models.Face_data()
#         mydata.image_path=request.POST['img_path']
#         mydata.image_username=request.POST['img_username']
#         # mydata.image_user_base_id=request.POST['id']
#         mydata.image_is_downloaded=1
#         mydata.save()
#         return JsonResponse("success",status=400)

#     elif(request.method=='GET'):#add new row
#         face_datas=models.Face_data.objects.all()
#         return JsonResponse(face_datas,status=400)



# elif(request.method=='PUT'):
#         data=JSONParser().parse(request)
#         serializer=FaceSerialier(Face_data,data=data)
#         if(serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data,status=201)
#         return Response(serializer.errors,status=400)

# Create your views here.
# @api_view(['GET','POST'])
# def article_list(request):
    
#     if request.method=='GET':
#         articles=Article.objects.all()
#         serializer=ArticleSerializer(articles,many=True)
#         return Response(serializer.data)

#     elif request.method=='POST':
#         # data=JSONParser().parse(request)
#         serializer=ArticleSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET','PUT','DELETE'])
# def article_detail(request,pk):
#     try:
#         article = Article.objects.get(pk=pk)

#     except Article.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     if(request.method=='GET'):
#         serializer=ArticleSerializer(article)
#         return Response(serializer.data)

#     elif(request.method=='PUT'):
#         serializer=ArticleSerializer(article,data=request.data)
#         if(serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     elif(request.method=='DELETE'):
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET','POST'])
# def test_one(request):
#     if request.method=='GET':
#         return Response("hello")

    

# class FileView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     def post(self, request, *args, **kwargs):
#         file_serializer = FileSerializer(data=request.data)
#         if file_serializer.is_valid():
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)