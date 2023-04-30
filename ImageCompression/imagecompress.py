import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join    
from numba import jit

orignal_path="D:\\Programs\\Python-Tutorials\\ImageCompression\\Orignal"
compressed_path="D:\\Programs\\Python-Tutorials\\ImageCompression\\Compressed"

def read_and_store_all_the_files(fromfolder):
    onlyfiles = [f for f in listdir(fromfolder) if isfile(join(fromfolder, f))]
    return onlyfiles

def remove_all_files(directory):
    onlyfiles=read_and_store_all_the_files(directory)
    for i in onlyfiles:
        os.remove(directory+"\\"+i)

@jit
def compressImage(imagePath,path, jpg_quality=None, png_compression=None):
  '''
  persist :image: object to disk. if path is given, load() first.
  jpg_quality: for jpeg only. 0 - 100 (higher means better). Default is 95.
  png_compression: For png only. 0 - 9 (higher means a smaller size and longer compression time).
                  Default is 3.
  '''
  image = cv2.imread(imagePath)

  if jpg_quality:
    cv2.imwrite(path, image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
  elif png_compression:
    cv2.imwrite(path, image, [int(cv2.IMWRITE_PNG_COMPRESSION), png_compression])
  else:
    cv2.imwrite(path, image)



def main():
    

    all_files=read_and_store_all_the_files(orignal_path)
    #remove_all_files(compressed_path)
    for i in all_files:
        full_path=orignal_path+"\\"+i
        output_path=compressed_path+"\\"+i
        print(full_path)

        

        #display the image
        #cv2.imshow('Hanif_Life2Coding', img)

        # save the image in JPEG format with 85% quality
        outpath_jpeg = output_path

        print("hello",outpath_jpeg,full_path)
        compressImage(outpath_jpeg,full_path,jpg_quality=85)

        outpath_png = i

        # save the image in PNG format with 4 Compression
        #save(outpath_png, img,png_compression=4)

        #cv2.waitKey(0)
        #destroy a certain window
        #cv2.destroyWindow('Hanif_Life2Coding')

if __name__ == "__main__":
    print("Calling main")
    #main()