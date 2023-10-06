import cv2
import numpy as np
import os

def extract_frames(video_path, frame_interval_ms=100):
    frames = []
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(frame_rate * frame_interval_ms / 1000)

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            frames.append(frame)
        count += 1

    cap.release()
    return frames

def stitch_frames(frames):
    # Create a stitcher object
    stitcher = cv2.Stitcher_create()
    
    # Attempt to stitch the frames
    status, panorama = stitcher.stitch(frames)
    
    if status == cv2.Stitcher_OK:
        return panorama
    else:
        print("Error during stitching:", status)
        return None

def main():
    video_path = "360Image\\360.mp4"
    output_dir = "360Image"
    frame_interval_ms = 100  # Interval for frame extraction in milliseconds
    frames_per_panorama = 10  # Number of frames to include in each panorama

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frames = extract_frames(video_path, frame_interval_ms)

    for i in range(0, len(frames), frames_per_panorama):
        panorama_frames = frames[i:i+frames_per_panorama]
        if len(panorama_frames) >= 2:
            panorama = stitch_frames(panorama_frames)
            if panorama is not None:
                panorama_filename = f"panorama_{i // frames_per_panorama}.jpg"
                panorama_path = os.path.join(output_dir, panorama_filename)
                cv2.imwrite(panorama_path, panorama)
                print("Panorama saved:", panorama_path)

if __name__ == "__main__":
    main()
