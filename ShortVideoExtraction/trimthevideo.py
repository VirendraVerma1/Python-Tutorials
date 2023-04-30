from moviepy.video.io.VideoFileClip import VideoFileClip
import os

# Specify the path of the input video
video_dir = "D:\\Programs\\Python-Tutorials\\ShortVideoExtraction\\ExperimentVideos\\VID_20221028_190355.mp4"
input_path = video_dir

# Specify the directory where the output clips will be saved
video_dirr = "D:\\Programs\\Python-Tutorials\\ShortVideoExtraction\\FromVideo\\"
output_dir = video_dirr

# Set the duration of each clip in seconds
clip_duration = 10

# Load the video clip
clip = VideoFileClip(input_path)

# Get the duration of the video clip in seconds
duration = clip.duration

# Calculate the number of clips needed
num_clips = int(duration // clip_duration)

# Iterate over each clip
for i in range(num_clips):
    # Set the start and end times for this clip
    start_time = i * clip_duration
    end_time = min((i+1) * clip_duration, duration)
    
    # Set the output file name for this clip
    output_file = os.path.join(output_dir, f'clip{i}.mp4')
    
    # Select the subclip for this clip
    subclip = clip.subclip(start_time, end_time)
    
    # Write the subclip to the output file
    subclip.write_videofile(output_file, codec='libx264', fps=clip.fps)
    
# Release the video clip
clip.close()