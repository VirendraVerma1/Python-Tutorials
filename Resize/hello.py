import cv2
import torch

# Load the YOLOv5 model.
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Load the image.
image = cv2.imread('test1.jpg')

# Convert the image to a PyTorch tensor.
image_tensor = torch.from_numpy(image)

# Run the YOLOv5 model on the image.
results = model(image_tensor)

# Filter the results to only include license plate detections.
license_plate_detections = []
for detection in results:
    if detection['class'] == 0:  # License plate class.
        license_plate_detections.append(detection)

# Draw bounding boxes around the detected license plates.
for detection in license_plate_detections:
    bounding_box = detection['bbox']
    cv2.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]), (0, 255, 0), 2)

# Save the output image.
cv2.imwrite('output.png', image)