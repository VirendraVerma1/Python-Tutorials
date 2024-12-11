import cv2
import os
import glob

def create_video_from_images(image_folder, video_name, fps=20.0, codec='XVID'):
    images = glob.glob(os.path.join(image_folder, 'frame*.png'))
    images.sort()

    if not images:
        print("No images found in the specified directory.")
        return

    # Read the first frame to get the frame size
    frame = cv2.imread(images[0])
    if frame is None:
        print("Error reading the first image.")
        return

    height, width, layers = frame.shape
    frame_size = (width, height)

    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(video_name, fourcc, fps, frame_size)

    for idx, image_path in enumerate(images):
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Error reading image {image_path}, skipping.")
            continue

        # Resize frame if necessary to match the first frame size
        if frame.shape[1::-1] != frame_size:
            frame = cv2.resize(frame, frame_size)

        out.write(frame)
        if idx % 100 == 0:
            print(f"Processed {idx} frames.")

    out.release()
    print(f"Video saved as {video_name}.")

if __name__ == "__main__":
    image_folder = 'CapturedFrames'
    video_name = 'output_video.avi'
    fps = 20.0
    codec = 'XVID'
    create_video_from_images(image_folder, video_name, fps, codec)
