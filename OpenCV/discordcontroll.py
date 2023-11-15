import pyautogui
from PIL import Image
import pytesseract

# Path to the Tesseract executable (update this with your path)
# pytesseract.pytesseract.tesseract_cmd = r'C:\path\to\tesseract\executable'

# Function to extract text from a region of the screen
def extract_text_from_region(left, top, width, height):
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save('screenshot.png')
    extracted_text = pytesseract.image_to_string(screenshot)
    return extracted_text

# Example coordinates for a region (adjust as needed)
left = 100
top = 100
width = 800
height = 400

# Extract text from the specified region
extracted_text = extract_text_from_region(left, top, width, height)
print("Extracted text:")
print(extracted_text)
