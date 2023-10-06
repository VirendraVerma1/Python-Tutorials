import cv2
import pytesseract
import easyocr
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# Load the image.
image = cv2.imread('test6.jpg')

# Convert the image to grayscale.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to the image.
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Threshold the image to binarize it.
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find all contours in the image.
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

# Filter the contours to find the license plate.
license_plate = None
for contour in contours:
    (x, y, w, h) = cv2.boundingRect(contour)
    aspect_ratio = w / h

    # Filter out contours that are not the license plate.
    if aspect_ratio > 2.0 and aspect_ratio < 5.0 and w > 100 and h > 20:
        license_plate = contour
        break

# If a license plate was found, crop it from the image and perform OCR.
if license_plate is not None:
    (x, y, w, h) = cv2.boundingRect(license_plate)
    license_plate_image = image[y:y + h, x:x + w]

    # Perform OCR on the license plate image.
    license_plate_number = pytesseract.image_to_string(license_plate_image)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(license_plate_image, detail = 0)
    # Window name in which image is displayed
    window_name = 'image'
    
    # Using cv2.imshow() method
    # Displaying the image
    # cv2.imshow()
    cv2.imwrite("output.jpg", license_plate_image)
    
    # Print the license plate number.
    print("Number=",license_plate_number,result)

else:
    print('No license plate found.')