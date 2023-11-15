from PIL import Image

def resize_and_crop_image(input_path, output_path, target_height=1920, target_width=1080):
    # Open the image
    img = Image.open(input_path)

    # Calculate the new width to maintain the aspect ratio
    aspect_ratio = img.width / img.height
    target_width = int(target_height * aspect_ratio)

    # Resize the image while maintaining the aspect ratio
    img_resized = img.resize((target_width, target_height))

    # Crop the image
    img_cropped = img_resized.crop((img_resized.width/2-540, 0, img_resized.width/2+540, 1920))

    # Save the resized and cropped image
    img_cropped.save(output_path)

if __name__ == "__main__":
    # Input and output file paths
    input_image_path = "animal.png"
    output_image_path = "output_image.jpg"

    # Call the resize and crop function
    resize_and_crop_image(input_image_path, output_image_path)
