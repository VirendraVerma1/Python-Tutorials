import os
from PIL import Image

# Input and output directories
input_directory = "Screenshots"
output_Iphone67 = "Iphone6.7"
output_Iphone65 = "Iphone6.5"
output_Iphone55 = "Iphone5.5"
output_Iphone129 = "Ipad12.9"

# Create the output directory if it doesn't exist
# Remove previous files in the output folder
for filename in os.listdir(output_Iphone67):
    file_path = os.path.join(output_Iphone67, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

for filename in os.listdir(output_Iphone65):
    file_path = os.path.join(output_Iphone65, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

for filename in os.listdir(output_Iphone55):
    file_path = os.path.join(output_Iphone55, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

for filename in os.listdir(output_Iphone129):
    file_path = os.path.join(output_Iphone129, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

# Desired dimensions for resized images
new_width = 800  # Replace with your desired width
new_height = 600  # Replace with your desired height

def resize_file(img,target_width,target_height,outputfolder):

# Calculate the aspect ratio of the image
            aspect_ratio = img.width / img.height

            # Calculate the new dimensions while maintaining the aspect ratio
            if aspect_ratio > (target_width / target_height):
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
            else:
                new_width = int(target_height * aspect_ratio)
                new_height = target_height

            # Resize the image while maintaining the aspect ratio
            img = img.resize((new_width, new_height))

            # Calculate the coordinates for cropping to the target dimensions
            left = (new_width - target_width) / 2
            top = (new_height - target_height) / 2
            right = (new_width + target_width) / 2
            bottom = (new_height + target_height) / 2

            # Crop the image to the target dimensions
            img = img.crop((left, top, right, bottom))
            # Save the resized image to the output directory
            img.save(os.path.join(outputfolder, filename))


# Loop through all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):  # Add more extensions as needed
        try:
            # Open the image file
            with Image.open(os.path.join(input_directory, filename)) as img:

                resize_file(img,2796,1290,output_Iphone67)
                resize_file(img,2778,1284,output_Iphone65)
                resize_file(img,2208,1242,output_Iphone55)
                resize_file(img,2732,2048,output_Iphone129)
               
                
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    else:
        print(f"Skipping {filename} (not a supported image format)")

print("Done resizing images.")