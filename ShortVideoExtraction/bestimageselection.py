import os
import random
import numpy as np
from PIL import Image
from collections import defaultdict
from keras.models import Sequential
from keras.layers import Dense

# Set the directory path
directory_path = 'D:\\Programs\\Python-Tutorials\\ShortVideoExtraction\\ExperimentalPics\\'

# Set the image size
image_size = (64, 64)

# Set the model weights file path
model_weights_file_path = 'model_weights.h5'
# Initialize Q-table
Q = defaultdict(int)

# Set learning rate and discount factor
alpha = 0.1
gamma = 0.9

# Build the neural network model
model = Sequential()
model.add(Dense(64, input_shape=(image_size[0] * image_size[1] * 3,), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='adam')

# Load model weights from file if it exists
if os.path.exists(model_weights_file_path):
    model.load_weights(model_weights_file_path)

# Get list of images in the directory
images = [filename for filename in os.listdir(directory_path) if filename.endswith('.jpg') or filename.endswith('.png')]

# Loop through all images in the directory
while images:
    # Select next image based on Q-values predicted by the neural network model
    q_values = []
    for image_name in images:
        # Open the image and resize it
        image = Image.open(os.path.join(directory_path, image_name)).resize(image_size)

        # Convert image to numpy array and normalize pixel values
        image_array = np.asarray(image) / 255.0

        # Predict Q-value of the image using the neural network model
        q_value = model.predict(image_array.reshape(1, -1))[0][0]
        q_values.append(q_value)

    next_image = images[np.argmax(q_values)]
    images.remove(next_image)

    # Open the next image and resize it
    image = Image.open(os.path.join(directory_path, next_image)).resize(image_size)
    image.show()

    # Convert image to numpy array and normalize pixel values
    image_array = np.asarray(image) / 255.0

    # Predict Q-value of the image using the neural network model
    q_value = model.predict(image_array.reshape(1, -1))[0][0]

    # Get user input
    user_input = input('Is this a good picture? (y/n): ')

    # Update Q-value based on user input
    if user_input == 'y':
        reward = 1
    else:
        reward = -1

    # Update Q-value using the neural network model
    if Q:
        target_q_value = reward + gamma * max(Q.values())
    else:
        target_q_value = reward

    model.fit(image_array.reshape(1, -1), np.array([[target_q_value]]), epochs=1, verbose=0)

    # Update Q-value in Q-table
    Q[next_image] += alpha * (target_q_value - q_value)

# Save model weights to file
model.save_weights(model_weights_file_path)

# Sort images by Q-value and print the best images
best_images = sorted(Q.items(), key=lambda x: x[1], reverse=True)
print('Best images:', [image[0] for image in best_images])