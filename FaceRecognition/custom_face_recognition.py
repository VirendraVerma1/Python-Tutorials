import face_recognition
import cv2
import numpy as np
import glob
import pickle
from PIL import Image, ImageDraw
from face_recognition.api import face_encodings, face_locations
import json
import time
import requests
import urllib.request

#paths
KnownImageFilePath='./img/known/'

#variables
total_data=0
image_path_li=[]
image_username_li=[]
image_username_id_li=[]
image_is_local_li=[]

image_encodes=[]

isserveron=True
server_counter=500

def load_all_the_data():
    global image_path_li
    global image_username_li
    global image_username_id_li
    global image_is_local_li
    global image_encodes

    f = open('data.json')
    data = json.load(f)
    for i in data['image_path']:
        image_path_li.append(i)
    for i in data['image_username']:
        image_username_li.append(i)
    for i in data['image_user_id']:
        image_username_id_li.append(i)
    for i in data['image_is_downloaded']:
        image_is_local_li.append(i)

    f.close()

def encode_the_old_data():
    global image_path_li
    global image_username_li
    global image_username_id_li
    global image_is_local_li
    global image_encodes
    for i in range(0,total_data):
        temp_image=face_recognition.load_image_file(image_path_li[i])
        temp_encode=face_recognition.face_encodings(temp_image)[0]    
        image_encodes.append(temp_encode)

def store_new_data():
    global image_path_li
    global image_username_li
    global image_username_id_li
    global image_is_local_li
    global image_encodes


    #download the image with the from the api

    img_path='./img/known/Steve Jobs.jpg'
    img_name="Steve Jobs"
    img_id="1112"
    local_img="1"#0 for not in local 1 for is not in local

    image_path_li.append(img_path)
    image_username_li.append(img_name)
    image_username_id_li.append(img_id)
    image_is_local_li.append(local_img)
    total_data=len(image_path_li)

def compare_the_face():
    global image_path_li
    global image_username_li
    global image_username_id_li
    global image_is_local_li
    global image_encodes

    img_path='./img/known/Steve Jobs.jpg' #this thing will be come from the server
    response = urllib.request.urlopen(url)
    test_image=face_recognition.load_image_file(response)
    face_locations=face_recognition.face_locations(test_image)
    face_encodings=face_recognition.face_encodings(test_image,face_locations)

    for(top, right,bottom,left),face_encoding in zip(face_locations,face_encodings):
        matches=face_recognition.compare_faces(image_encodes,face_encoding)

        name="Unknown Person"

        if True in matches:
            first_match_index=matches.index(True)
            name=image_username_li[first_match_index] 

#write the file
def write_all_data_to_json():
    global image_path_li
    global image_username_li
    global image_username_id_li
    global image_is_local_li
    global image_encodes

    dictionary ={
            "image_path": image_path_li,
            "image_username": image_username_li,
            "image_user_id": image_username_id_li,
            "image_is_downloaded": image_is_local_li
        }

    # Serializing json 
    json_object = json.dumps(dictionary, indent = 4)
    with open('data.json', 'w') as f:
        json.dump(dictionary, f)

def stop_the_program():
    isserveron=False
    write_all_data_to_json()

load_all_the_data()
#store_new_data()
#write_all_data_to_json()

while(True):
    time.sleep(1)
    

    server_counter-=1
    if(server_counter<0):
        server_counter=500
        write_all_data_to_json()