import cv2
import os

# Specify the path of the input video
video_dir = "D:\\Programs\\Python-Tutorials\\ShortVideoExtraction\\ExperimentVideos\\VID_20221028_190355.mp4"
input_path = video_dir

# Specify the directory where the output clips will be saved
video_dirr = "D:\\Programs\\Python-Tutorials\\ShortVideoExtraction\\FromVideo\\"
output_dir = video_dirr

# Open the video file
cap = cv2.VideoCapture(input_path)

# Check if the video file was successfully opened
if not cap.isOpened():
    print('Error opening video file')

# Initialize variables
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set the starting and ending frame numbers for each clip
clip_frames = [(0, 100), (100, 200), (200, frame_count)]

# Iterate over each clip
for i, clip in enumerate(clip_frames):
    # Set the starting and ending frames for this clip
    start_frame, end_frame = clip
    
    # Set the output file name for this clip
    output_file = os.path.join(output_dir, f'clip{i}.mp4')
    
    # Create a new video writer object for this clip
    writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    
    # Set the starting frame for the video capture object
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    # Iterate over each frame in this clip
    for j in range(start_frame, end_frame):
        # Read the next frame from the video file
        ret, frame = cap.read()
        
        # Check if the frame was successfully read
        if not ret:
            print(f'Error reading frame {j} for clip {i}')
            break
        
        # Crop the frame
        # You can adjust the crop parameters as needed
        crop_top = int(frame_height * 0.2)
        crop_bottom = int(frame_height * 0.8)
        crop_left = int(frame_width * 0.2)
        crop_right = int(frame_width * 0.8)
        cropped_frame = frame[crop_top:crop_bottom, crop_left:crop_right]
        
        # Write the cropped frame to the output video file
        writer.write(cropped_frame)
    
    # Release the video writer object
    writer.release()

# Release the video capture object
cap.release()