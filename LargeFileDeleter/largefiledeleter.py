
import os
from fnmatch import fnmatch

#ingo
# folder_path="D:\\Programs\\Python-Tutorials\\LargeFileDeleter\\Placement-Prepration\\Placement Prepration"
#folder_path="D:\\Tesseract\\BandookDhari"
folder_path="D:\\Programs\\Unity\\"

for path, subdirs, files in os.walk(folder_path):
    for name in files:
        try:
            #print(os.path.join(path, name))
            fileSize = os.path.getsize(os.path.join(path, name))
            #print(fileSize)
            if(fileSize>104857600): # this is 100 mb in binary
                print(os.path.join(path, name))
                print(fileSize)
                os.remove(os.path.join(path, name))
                print("file removed")
        except:
            print("An exception occurred")
        

#fallcars

"""           
folder_path="D:\\Programs\\Unity"
for path, subdirs, files in os.walk(folder_path):
    for name in files:
        try:
            #print(os.path.join(path, name))
            fileSize = os.path.getsize(os.path.join(path, name))
            #print(fileSize)
            if(fileSize>104857600): # this is 100 mb in binary
                print(os.path.join(path, name))
                print(fileSize)
                #os.remove(os.path.join(path, name))
                print("file removed")
        except:
            print("An exception occurred")
"""
