#face recognition
import face_recognition
import numpy as np
import urllib.request
import os
from fnmatch import fnmatch

dir_path = os.path.dirname(os.path.realpath(__file__))

#paths
KnownImageFilePath=dir_path + "\img\known\\"
compareImagePath=dir_path + "\img\compare\\"

#variables
allKnownImages=[]
allUnKnownImages=[]


def load_all_known_files():
    for path, subdirs, files in os.walk(KnownImageFilePath):
        for name in files:
            allKnownImages.append(path+name)

def load_all_unknown_files():
    for path, subdirs, files in os.walk(compareImagePath):
        for name in files:
            allUnKnownImages.append(path+name)

def check_files():
    print("Known Images")
    for i in allKnownImages:
        print(i)


    print("UnKnown Images")
    for i in allUnKnownImages:
        print(i)

def compare_faces(tocompareImage):
    image_locations=[]
    known_face_encodings=[]
    for i in allKnownImages:
        temp_image=face_recognition.load_image_file(i)
        temp_locations=face_recognition.face_locations(temp_image)
        temp_encode=face_recognition.face_encodings(temp_image)[0]   
        image_locations.append(temp_locations)
        known_face_encodings.append(temp_encode)

    #check if the URL or from the directory
    if "http" in tocompareImage:
        img_path=tocompareImage
        test_image = urllib.request.urlopen(img_path)
    else:
        img_path=tocompareImage
        
    
    test_image = face_recognition.load_image_file(img_path)
    # Find faces in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    # Create a ImageDraw instance
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            new_json={'UserName':allKnownImages[best_match_index]}
            print(new_json)
            return

        if True in matches:
            first_match_index = matches.index(True)
            new_json={'UserName':allKnownImages[first_match_index]}
            print(new_json)
            return

    new_json={'UserName':'Unknown'}
    print(new_json)
    return 

def compare_all_images_from_URL():
    compare_faces("http://t2.gstatic.com/licensed-image?q=tbn:ANd9GcSStEXQ52SE6txqvnwfAyOZ-dt6fkkBqzcir0RaZkoG54dYK7UByieR90Nb18ON4rdZ6VyDNVuQdk1kXik")

def compare_all_images_from_directory():
    for i in allUnKnownImages:
        compare_faces(i)




#main

load_all_known_files()
load_all_unknown_files()
# check_files()
# compare_all_images_from_URL()
compare_all_images_from_directory()
