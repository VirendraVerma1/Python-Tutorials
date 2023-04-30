#  "D:\\Programs\\Python-Tutorials\\ShortVideoExtraction\\FromVideo\\"
from keras.models import Sequential
from keras.layers import Dense
import cv2
import numpy as np
import os

# Set the directory path
dir_path = "D:\\Programs\\Python-Tutorials\\ShortVideoExtraction\\FromVideo\\"

# Get the list of video files in the directory
video_files = [f for f in os.listdir(dir_path) if f.endswith('.mp4')]

# Create a model
model = Sequential()
model.add(Dense(1, input_shape=(224, 224, 3)))
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

# Load the model weights from a file if it exists
weights_file = 'weights.h5'
if os.path.exists(weights_file):
    model.load_weights(weights_file)

# Get user input for training
for video_file in video_files:
    # Load the video file using OpenCV
    cap = cv2.VideoCapture(os.path.join(dir_path, video_file))
    
    # Process the video frames
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Preprocess the frame (resize, normalize, etc.)
        frame = cv2.resize(frame, (224, 224))
        frame = frame.astype('float32') / 255.0
        
        # Add the preprocessed frame to the list of frames
        frames.append(frame)
    
    # Release the video capture
    cap.release()
    
    # Convert the list of frames to a NumPy array and average them
    video = np.array(frames).mean(axis=0)
    
    # Get user input for whether the video is good or bad
    label = input(f'Is {video_file} a good video? (y/n): ')
    label = np.array([1 if label == 'y' else 0])
    
    # Train the model on the video and label
    model.train_on_batch(np.expand_dims(video, axis=0), label)

# Save the model weights to a file
model.save_weights(weights_file)

# Select the best video based on the model's predictions
best_video = None
best_score = 0
for video_file in video_files:
    # Load the video file using OpenCV
    cap = cv2.VideoCapture(os.path.join(dir_path, video_file))
    
    # Process the video frames
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Preprocess the frame (resize, normalize, etc.)
        frame = cv2.resize(frame, (224, 224))
        frame = frame.astype('float32') / 255.0
        
        # Add the preprocessed frame to the list of frames
        frames.append(frame)
    
    # Release the video capture
    cap.release()
    
    # Convert the list of frames to a NumPy array and average them
    video = np.array(frames).mean(axis=0)
    
    # Get the model's prediction for the video
    score = model.predict(np.expand_dims(video, axis=0))[0][0]
    
    # Update the best video and score if necessary
    if score > best_score:
        best_video = video_file
        best_score = score

# Output the best video in mp4 format
print(f'The best video is: {best_video}')