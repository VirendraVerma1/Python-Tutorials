import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join    
from videocompress import compressVideo
#from imagecompress import compressImage
from imagecompresspil import compress_image
#import tensorflow as tf
from numba import jit

orignal_path="D:\\Programs\\Python-Tutorials\\ImageCompression\\Orignal"
compressed_path="D:\\Programs\\Python-Tutorials\\ImageCompression\\Compressed"

compressQualityPercentage=70
reverse=False

notused=[]

def read_and_store_all_the_files(fromfolder):
    onlyfiles = [f for f in listdir(fromfolder) if isfile(join(fromfolder, f))]
    return onlyfiles

def remove_all_files(directory):
    onlyfiles=read_and_store_all_the_files(directory)
    for i in onlyfiles:
        os.remove(directory+"\\"+i)

@jit
def main():
    remove_all_files(compressed_path)
    all_files=read_and_store_all_the_files(orignal_path)
    #remove_all_files(compressed_path)
    for i in all_files:
        full_path=orignal_path+"\\"+i
        output_path=compressed_path+"\\"+i
            
        if ".mp4" in i:
            compressVideo(full_path,output_path,compressQualityPercentage,reverse)
        elif ".jpg" in i:
            compress_image(full_path,output_path)
        elif ".png" in i:
            compress_image(full_path,output_path)
        else:
            notused.append(i)
    print("############## Final Report ###########")
    print("Not Compressed Files")
    print(notused)

if __name__ == "__main__":
    main()
