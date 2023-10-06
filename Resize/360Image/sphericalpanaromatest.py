import cv2
import cv2 as stritchOperation
import numpy as np
from PIL import Image
from numpy import asarray
import time

def resize_frame(frame, scale_factor):
    width = int(frame.shape[1] * scale_factor)
    height = int(frame.shape[0] * scale_factor)
    return cv2.resize(frame, (width, height))

def create_360_image(frames):
    num_frames = len(frames)
    frame_height, frame_width, _ = frames[0].shape

    # Set the output image dimensions for 360-degree view
    output_height = num_frames * frame_height
    output_width = frame_width

    # Create a blank canvas for the final 360-degree image
    output_image = np.zeros((output_height, output_width, 3), np.uint8)

    # Merge frames into the final 360-degree image
    for i in range(num_frames):
        y_start = i * frame_height
        y_end = y_start + frame_height
        output_image[y_start:y_end, :] = frames[i]

    return output_image

def stitch_images(images):
    stitcher = stritchOperation.Stitcher_create()
    status, panorama = stitcher.stitch(images)

    if status == stritchOperation.Stitcher_OK:
        return panorama
    else:
        print("Image stitching failed",status )
        return None

# Load the video
video_path = "360Image\\360.mp4"  # Update with your video path
cap = cv2.VideoCapture(video_path)

#interval system
#crop the video for every next 2 seconds. extract the frames and create paranoma, when its done then
# Parameters for resizing and merging frames
scale_factor = 1/3  # Resize frames to one third of the resolution
interval = 0.1  # Interval in seconds

frames = []
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
i=0
merged_image=[]
strittchedImages=[]
last_pan_image=None
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame
    resized_frame = resize_frame(frame, scale_factor)
    
    # Append resized frame to the frames list
    frames.append(resized_frame)

    if(len(frames)>5):
        # Create the 360-degree image
        print("merging images "+str(i),len(frames))
        i=i+1
        merged_image = stitch_images(frames)
        frames.clear()
        if(merged_image is not None):
            last_pan_image=merged_image
            cv2.imwrite("360_image.jpg", last_pan_image)
        strittchedImages.append(merged_image)
        time.sleep(5)


    # Skip frames based on the specified interval
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_POS_FRAMES)) + frame_rate * interval)


frames=[]
i=0
for j in strittchedImages:
    frame=resize_frame(j,scale_factor)
    frames.append(frame)
    if(len(frames)>5):
        # Create the 360-degree image
        print("merging images "+str(i),len(frames))
        i=i+1
        merged_image = stitch_images(frames)
        frames.clear()
        if(merged_image is not None):
            last_pan_image=merged_image
            cv2.imwrite("360_image.jpg", last_pan_image)
        strittchedImages.append(merged_image)
        time.sleep(5)
# Save the 360-degree image
#cv2.imwrite("360_image.jpg", merged_image)

# Load and upscale the 360-degree image
original_image = Image.open("360_image.jpg")
upscaled_image = original_image.resize((2 * original_image.width, 2 * original_image.height))

# Save the upscaled image
upscaled_image.save("upscaled_360_image.jpg")



# Release the video capture
cap.release()
cv2.destroyAllWindows()
