import os
import cv2

def extract_frames(video_path, output_dir, frame_interval=1):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save the frame every specified interval
        if frame_number % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{frame_number}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")

        frame_number += 1

        # Jump to the next second
        cap.set(cv2.CAP_PROP_POS_MSEC, frame_number * 1000)

    cap.release()

if __name__ == "__main__":
    video_path = "D:\\Programs\\Python-Tutorials\\FramesFromVideo\\360interior.mp4"  # Replace with your video file's path
    output_dir = "D:\\Programs\\Python-Tutorials\\FramesFromVideo\\Frames\\"  # Replace with the desired output directory
    frame_interval = 2  # Interval in seconds between frames

    extract_frames(video_path, output_dir, frame_interval)