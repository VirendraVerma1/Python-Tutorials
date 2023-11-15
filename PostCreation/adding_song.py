import os
import random
from moviepy.editor import *
from PIL import Image

# Function to get a random music file from the Music folder
def get_random_music():
    music_folder = "Music"
    music_files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    return os.path.join(music_folder, random.choice(music_files))

def resize_and_crop_image(input_path,output_path, target_height=1920, target_width=1080):
    # Open the image
    img = Image.open(input_path)

    # Calculate the new width to maintain the aspect ratio
    aspect_ratio = img.width / img.height
    target_width = int(target_height * aspect_ratio)

    # Resize the image while maintaining the aspect ratio
    img_resized = img.resize((target_width, target_height))

    # Crop the image
    img_cropped = img_resized.crop((img_resized.width/2-540, 0, img_resized.width/2+540, 1920))

    # Save the resized and cropped image
    img_cropped.save(output_path)
    # return img_cropped

# Input image file and output video file
input_image = "animal.png"
temp_image="temp.jpg"
output_video = "output_video.mp4"

resize_and_crop_image(input_image,temp_image)
input_image=temp_image

# Load the image
image_clip = ImageClip(input_image)


# Get a random music file from the Music folder
music_file = get_random_music()

# Set the duration of the video based on the length of the audio
audio = AudioFileClip(music_file)
video_duration = audio.duration

# Set the resolution of the video (1080x1920)
video_resolution = (1080, 1920)

# Resize the image to the desired resolution
image_clip = image_clip.resize(video_resolution)

# Set the video parameters
video_clip = image_clip.set_audio(audio).set_duration(video_duration)

# Write the video to an output file
video_clip.write_videofile(output_video, codec='libx264', fps=30)
