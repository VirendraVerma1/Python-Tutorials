from os import listdir
from os.path import isfile, join    
from numba import jit

orignal_path="D:\\Programs\\Python-Tutorials\\ImageCompression\\Orignal"
compressed_path="D:\\Programs\\Python-Tutorials\\ImageCompression\\Compressed"

compressQualityPercentage=90
reverse=True


# Importing the module
from moviepy.editor import *

def read_and_store_all_the_files(fromfolder):
    onlyfiles = [f for f in listdir(fromfolder) if isfile(join(fromfolder, f))]
    return onlyfiles

@jit
def compressVideo(filePath,tofilePath,quality=compressQualityPercentage,rev=True):
    # uploading the video we want to edit
    video = VideoFileClip(filePath)
    print("Width and Height of "+filePath+" : ", end = " ")
    print(str(video.w) + " x ", str(video.h))
    print("#################################")
    # resizing....
    #video_resized = video.resize(0.7)
    compressedHieght=(video.h/100)*quality
    compressedWidth=(video.w/100)*quality
    #reversing
    if(rev):
        video_resized = video.resize((compressedHieght,compressedWidth))
    else:
        video_resized = video.resize((compressedWidth,compressedHieght))

    print("Width and Height of "+filePath+" video : ", end = " ")
    print(str(video_resized.w) + " x ", str(video_resized.h))

    print("###################################")
    video_resized.write_videofile(tofilePath)

def main():
    all_files=read_and_store_all_the_files(orignal_path)
    counter=0
    for i in all_files:
        full_path=orignal_path+"\\"+i
        output_path=compressed_path+"\\"+i
        compressVideo(full_path,output_path)
        counter+=1
        print("Compressed = "+str(counter))

if __name__ == "__main__":
    print("calling main")
    #main()