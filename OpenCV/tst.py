from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

# Load video from file
clip = VideoFileClip("input_video.mp4")

# Make subclip from 10s to 40s (30s clip)
subclip = clip.subclip(10, 40)

# Resize subclip to desired resolution
resized_clip = subclip.resize(height=1920)

# Crop the video to 1080x1920 (width x height)
# Here (x_center, y_center) is the position of the center of the cropped region
cropped_clip = subclip.crop(x_center=subclip.w/2-540, y_center=subclip.h, width=1080, height=1920)

# Write the result to a file
cropped_clip.write_videofile("output.mp4", codec='libx264')
