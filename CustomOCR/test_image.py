import numpy as np
from keras.models import load_model
from keras.preprocessing import image as keras_image

# Load the trained model
model = load_model('character_model.h5')

# Load the image
img_path = 'input.png'
img = keras_image.load_img(img_path, target_size=(100, 100))

# Convert the image to a numpy array
x = keras_image.img_to_array(img)

# Normalize the image data
x /= 255

# Expand the dimensions so the model will accept the new image
x = np.expand_dims(x, axis=0)

# Predict the character
predictions = model.predict(x, batch_size=32)

# Get the index of the highest probability
predicted_index = np.argmax(predictions[0])

# Convert the index to a character
if predicted_index < 26:
    predicted_char = chr(predicted_index + ord('A'))  # Uppercase letters
else:
    predicted_char = chr(predicted_index - 26 + ord('a'))  # Lowercase letters

# Print the predicted character
print("The predicted character is:", predicted_char)
