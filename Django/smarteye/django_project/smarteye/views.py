from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FaceData
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from .serializers import FaceSerialier

#face recognition
import face_recognition
import numpy as np
import glob
import pickle
from PIL import Image, ImageDraw
import PIL
import time
import requests
import urllib.request
from PIL import Image
import base64
from django.core.files.base import ContentFile
import io
# Create your views here.

def base64_file(data):
    format, imgstr = data.split(';base64,') 
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # You can save this as file instance.
    return data
    # user.image.save(file_name, data, save=True) # image is User's model field

@api_view(['GET','POST'])
def face_data(request):
    if(request.method=='GET'):
        articles=FaceData.objects.all()
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
        article = FaceData.objects.get(pk=pk)

    except FaceData.DoesNotExist:
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
        
@api_view(['POST'])
def compare_faces(request):
    base_url="http://64.227.178.238"
    #load the database data
    image_path_li=[]
    known_face_names=[]
    known_face_id=[]
    image_locations=[]
    known_face_encodings=[]
    face_datas=FaceData.objects.all()
    serializer=FaceSerialier(face_datas,many=True)
    #return Response(serializer.data[0].image_path)
    fdata=serializer.data[:]
    for i in fdata:
        # image_path_li.append(i['image_path'])
        known_face_names.append(i['image_username'])
        known_face_id.append(i['image_user_base_id'])
        # response = urllib.request.urlopen(i['image_path'])
        data=base64_file(i['image_encoded'])
        temp_image=face_recognition.load_image_file(data)
        temp_locations=face_recognition.face_locations(temp_image)
        temp_encode=face_recognition.face_encodings(temp_image)[0]   
        image_locations.append(temp_locations)
        known_face_encodings.append(temp_encode)
    # img_path1="http://64.227.178.238/media/testvirendra.jpeg" #this thing will be come from the server
    # img_path1='http://64.227.178.238/home/django/django_project/media/testsidhant.jpeg' #this thing will be come from the server
    # img_path1='https://image.cnbcfm.com/api/v1/image/106926992-1628885077267-elon.jpg?v=1639409610'
    # img_path1='https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Steve_Jobs.jpg/527px-Steve_Jobs.jpg'
    # img_path1='https://thumbor.forbes.com/thumbor/fit-in/416x416/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5f4ebe0c87612dab4f12a597%2F0x0.jpg' #this thing will be come from the server
    
    # img_path1=request.POST['image_url_path']
    # img_path1=request.POST['image_url_path']
    # img_encoded=request.POST['image_encoded']
    if 'image_url_path' in request.POST:
        response1 = urllib.request.urlopen(request.POST['image_url_path'])
        test_image = face_recognition.load_image_file(response1)
    else:
        data=base64_file(request.POST['image_encoded'])
        test_image = face_recognition.load_image_file(data)

        

    # Find faces in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    # Convert to PIL format
    pil_image = Image.fromarray(test_image)

    # Create a ImageDraw instance
    draw = ImageDraw.Draw(pil_image)
    name = "Unknown Person"
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown Person"
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            new_json={'UserName':known_face_names[best_match_index],'UserID': known_face_id[best_match_index]}
            return Response(new_json)

        #name = "Unknown Person"
        # If match
        # return Response(matches)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            new_json={'UserName':known_face_names[first_match_index],'UserID': known_face_id[first_match_index]}
            return Response(new_json)
        
        # # Draw box
        # draw.rectangle(((left, top), (right, bottom)), outline=(255,255,0))

        # # Draw label
        # text_width, text_height = draw.textsize(name)
        # draw.rectangle(((left,bottom - text_height - 10), (right, bottom)), fill=(255,255,0), outline=(255,255,0))
        # draw.text((left + 6, bottom - text_height - 5), name, fill=(0,0,0))

    new_json={'UserName':'Unknown','UserID': 0}
    return Response(new_json)

    
    
    # name="Unknown Person"
    # newstr=""
    # for(top, right,bottom,left),image_encode in zip(face_locationss,face_encodingss):
    #     matches=face_recognition.compare_faces(image_encodes,image_encode)

    #     name="Unknown Person"
    #     face_distances = face_recognition.face_distance(image_encodes, image_encode)
    #     best_match_index = np.argmin(face_distances)
    #             # matches_faces=matches[0]
    #             # return Response(matches)
    #             # if matches_faces[best_match_index]:
    #             #     name = image_username_li[best_match_index]
    #             #     print(name)
    #             # return Response(matches)
    #     print()
    #     return Response(matches)
    #     if(matches[0]==True):
    #         # first_match_index=matches.index(True)
    #         name=image_username_li[i] 
    #         newstr+=name+"|"+str(best_match_index)+"!"+str(matches[0])+"."+image_path_li[i]+","
                    

    # return Response(newstr)



@api_view(['GET'])
def compare_faces_from_url(request):

    img_path='https://cdn.vox-cdn.com/thumbor/WCH_hpmDktgoM_vsNb4QGWr2s8k=/0x104:438x396/1400x1050/filters:focal(0x104:438x396):format(jpeg)/cdn.vox-cdn.com/imported_assets/846336/steve-jobs.jpeg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    test_image=face_recognition.load_image_file(response)
    face_location=face_recognition.face_locations(test_image)
    face_encodings=face_recognition.face_encodings(test_image,face_location)

    # img_path1='https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Steve_Jobs.jpg/527px-Steve_Jobs.jpg' #this thing will be come from the server
    img_path1='https://thumbor.forbes.com/thumbor/fit-in/416x416/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5f4ebe0c87612dab4f12a597%2F0x0.jpg' #this thing will be come from the server
    response1 = urllib.request.urlopen(img_path1)
    test_image1=face_recognition.load_image_file(response1)
    face_locations1=face_recognition.face_locations(test_image1)
    face_encodings1=face_recognition.face_encodings(test_image1,face_locations1)
    name="Unknown Person"
    for(top, right,bottom,left),face_encoding in zip(face_location,face_encodings):
        matches=face_recognition.compare_faces(face_encodings1,face_encoding)
        face_distances = face_recognition.face_distance(face_encodings1, face_encoding)
        best_match_index = np.argmin(face_distances)
        name="Unknown Person"
        #return Response(best_match_index)
        #return Response(matches)
        if True in matches:
            name="Steve"
            return Response(name)
    return Response(name)


@api_view(['GET'])
def compare_multiple_faces_from_url(request):

    img_path='https://content.fortune.com/wp-content/uploads/2020/09/CNV.10.20.FORTUNE_BILL_AND_MELINDA_GATES_030-vertical.jpg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    image_of_bill = face_recognition.load_image_file(response)
    bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]

    img_path='https://cdn.vox-cdn.com/thumbor/WCH_hpmDktgoM_vsNb4QGWr2s8k=/0x104:438x396/1400x1050/filters:focal(0x104:438x396):format(jpeg)/cdn.vox-cdn.com/imported_assets/846336/steve-jobs.jpeg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    image_of_steve = face_recognition.load_image_file(response)
    steve_face_encoding = face_recognition.face_encodings(image_of_steve)[0]

    img_path='https://upload.wikimedia.org/wikipedia/commons/8/85/Elon_Musk_Royal_Society_%28crop1%29.jpg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    image_of_elon = face_recognition.load_image_file(response)
    elon_face_encoding = face_recognition.face_encodings(image_of_elon)[0]

    #  Create arrays of encodings and names
    # known_face_encodings = [
    # bill_face_encoding,
    # steve_face_encoding,
    # elon_face_encoding
    # ]
    known_face_encodings=[]
    known_face_encodings.append(bill_face_encoding)
    known_face_encodings.append(steve_face_encoding)
    known_face_encodings.append(elon_face_encoding)

    known_face_names = [
    "Bill Gates",
    "Steve Jobs",
    "Elon Musk"
    ]

    # Load test image to find faces in
    img_path1='https://image.cnbcfm.com/api/v1/image/106926992-1628885077267-elon.jpg?v=1639409610'
    # img_path1='https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Steve_Jobs.jpg/527px-Steve_Jobs.jpg'
    # img_path1='https://thumbor.forbes.com/thumbor/fit-in/416x416/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5f4ebe0c87612dab4f12a597%2F0x0.jpg' #this thing will be come from the server
    response1 = urllib.request.urlopen(img_path1)
    test_image = face_recognition.load_image_file(response1)

    # Find faces in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    # Convert to PIL format
    pil_image = Image.fromarray(test_image)

    # Create a ImageDraw instance
    draw = ImageDraw.Draw(pil_image)

    # Loop through faces in test image
    name = "Unknown Person"
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown Person"
        return Response(matches)
        # If match
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        
        # Draw box
        draw.rectangle(((left, top), (right, bottom)), outline=(255,255,0))

        # Draw label
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left,bottom - text_height - 10), (right, bottom)), fill=(255,255,0), outline=(255,255,0))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(0,0,0))



    return Response(name)

    img_path='https://cdn.vox-cdn.com/thumbor/WCH_hpmDktgoM_vsNb4QGWr2s8k=/0x104:438x396/1400x1050/filters:focal(0x104:438x396):format(jpeg)/cdn.vox-cdn.com/imported_assets/846336/steve-jobs.jpeg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    test_image=face_recognition.load_image_file(response)
    face_location=face_recognition.face_locations(test_image)
    face_encodings=face_recognition.face_encodings(test_image,face_location)

    img_path='https://content.fortune.com/wp-content/uploads/2020/09/CNV.10.20.FORTUNE_BILL_AND_MELINDA_GATES_030-vertical.jpg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    test_image=face_recognition.load_image_file(response)
    face_location1=face_recognition.face_locations(test_image)
    face_encodings1=face_recognition.face_encodings(test_image,face_location1)

    img_path='https://upload.wikimedia.org/wikipedia/commons/8/85/Elon_Musk_Royal_Society_%28crop1%29.jpg' #this thing will be come from the server
    response = urllib.request.urlopen(img_path)
    test_image=face_recognition.load_image_file(response)
    face_location2=face_recognition.face_locations(test_image)
    face_encodings2=face_recognition.face_encodings(test_image,face_location2)

    known_image_encoding=[
        face_encodings,
        face_encodings1,
        face_encodings2
    ]

    known_image_names=[
        "Steve",
        "Bill",
        "Elon"
    ]

    img_path1='https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Steve_Jobs.jpg/527px-Steve_Jobs.jpg' #this thing will be come from the server
    #img_path1='https://thumbor.forbes.com/thumbor/fit-in/416x416/filters%3Aformat%28jpg%29/https%3A%2F%2Fspecials-images.forbesimg.com%2Fimageserve%2F5f4ebe0c87612dab4f12a597%2F0x0.jpg' #this thing will be come from the server
    response1 = urllib.request.urlopen(img_path1)
    test_image1=face_recognition.load_image_file(response1)
    face_locations1=face_recognition.face_locations(test_image1)
    face_encodings1=face_recognition.face_encodings(test_image1,face_locations1)
    name="Unknown Person"
    for(top, right,bottom,left),face_encoding in zip(face_location,face_encodings):
        matches=face_recognition.compare_faces(known_image_encoding,face_encoding)
        face_distances = face_recognition.face_distance(known_image_encoding, face_encoding)
        best_match_index = np.argmin(face_distances)
        name="Unknown Person"
        #return Response(best_match_index)
        #return Response(matches)
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
    return Response(name)