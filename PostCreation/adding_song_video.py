import os
import random
from moviepy.editor import *
from PIL import Image
import math

def get_images(image_folder="MyImages"):
    return [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]

def get_random_music(music_folder="Music"):
    music_files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
    return os.path.join(music_folder, random.choice(music_files))

def resize_and_crop_image(input_path, output_path, target_height=1920, target_width=1080):
    img = Image.open(input_path)
    aspect_ratio = img.width / img.height
    target_width = int(target_height * aspect_ratio)
    img_resized = img.resize((target_width, target_height))
    img_cropped = img_resized.crop((img_resized.width/2-540, 0, img_resized.width/2+540, 1920))
    img_cropped.save(output_path)

def create_clip(image, clip_duration):
    temp_image = "temp.jpg"
    resize_and_crop_image(image, temp_image)
    clip = ImageClip(temp_image).resize((1080, 1920)).set_duration(clip_duration)
    start_size = clip.size
    end_size = [dim * 1.2 for dim in start_size]
    clip_zoom = clip.resize(lambda t: start_size if t == 0 else [start_size[i] + (end_size[i] - start_size[i]) * t / clip_duration for i in range(2)])
    return clip_zoom

def create_video(clips, output_video,music_file):
    final_clip = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(music_file)
    audio_duration = audio.duration
    clip_duration = audio_duration / len(clips)
    clips = [create_clip(image, clip_duration) for image in images]
    final_clip = final_clip.set_audio(audio).set_duration(audio_duration)
    final_clip.write_videofile(output_video, codec='libx264', fps=30)

images = get_images()
output_video = "output_video.mp4"
music_file = get_random_music()
audio = AudioFileClip(music_file)
audio_duration = audio.duration
clip_duration = audio_duration / (len(images))
print(math.ceil(clip_duration),audio_duration)
clips = [create_clip(image, math.ceil(clip_duration)) for image in images]
create_video(clips, output_video,music_file)
