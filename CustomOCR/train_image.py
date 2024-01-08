import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from keras.preprocessing import image as keras_image
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from keras.layers import Conv2D, MaxPooling2D, Dropout
from keras.layers import BatchNormalization
from keras.preprocessing.image import ImageDataGenerator

# Get all the fonts under "Fonts" folder
fonts = os.listdir("Fonts")

# Filter for .ttf fonts
ttf_fonts = [font for font in fonts if font.endswith(".ttf")]

print("TTF Fonts:", ttf_fonts)

# Create a directory to save the images
if not os.path.exists("Images"):
    os.makedirs("Images")

# Initialize arrays for storing image data and labels
num_samples = len(ttf_fonts) * 26  # 26 characters for each font
X_train = np.empty((num_samples, 100, 100, 3))
y_train = np.empty((num_samples,), dtype=int)

# Create an image for each alphabet character from each .ttf font
sample_index = 0
for font_name in ttf_fonts:
    font_path = os.path.join("Fonts", font_name)
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        # Create a blank image
        image = Image.new('RGB', (100, 100), color=(73, 109, 137))

        # Get a drawing context
        d = ImageDraw.Draw(image)

        # Define the font
        fnt = ImageFont.truetype(font_path, 40)

        # Draw text
        d.text((10,10), char, font=fnt, fill=(255, 255, 0))

        # Save the image in the "Images" folder
        image_path = os.path.join("Images", f"{font_name}_{char}.png")
        image.save(image_path)

        # Load the image into the training data
        img = keras_image.load_img(image_path, target_size=(100, 100))
        X_train[sample_index, :, :, :] = keras_image.img_to_array(img)
        y_train[sample_index] = ord(char.upper()) - ord('A')  # Convert character to integer label
        sample_index += 1

# Normalize image data
X_train /= 255

# Define a more complex model
model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(100, 100, 3)))
model.add(BatchNormalization())
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(26, activation='softmax'))  # 26 classes for 26 letters

# Compile the model with a smaller learning rate
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=Adam(learning_rate=0.0001),
              metrics=['accuracy'])

# Create an ImageDataGenerator for data augmentation
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    fill_mode='nearest')

# Train the model for more epochs with data augmentation
model.fit(datagen.flow(X_train, y_train, batch_size=32),
          steps_per_epoch=len(X_train) / 32,
          epochs=100)

# Save the trained model
model.save('character_model.h5')
