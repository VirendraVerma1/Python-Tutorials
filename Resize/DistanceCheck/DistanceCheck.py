from PIL import Image, ImageDraw

def extract_center_segment(image, segment_size):
    # Get the dimensions of the image
    width, height = image.size

    # Calculate the coordinates for the center segment
    left = (width - segment_size) // 2
    top = (height - segment_size) // 2
    right = left + segment_size
    bottom = top + segment_size

    # Crop the image to the center segment
    center_segment = image.crop((left, top, right, bottom))
    return center_segment

def extract_left_segment(image, segment_size):
    # Get the dimensions of the image
    width, height = image.size

    # Calculate the coordinates for the center segment
    left = (width - segment_size) // 4
    top = (height - segment_size) // 2
    right = left + segment_size
    bottom = top + segment_size

    # Crop the image to the center segment
    center_segment = image.crop((left, top, right, bottom))
    return center_segment

def extract_up_segment(image, segment_size):
    # Get the dimensions of the image
    width, height = image.size

    # Calculate the coordinates for the center segment
    left = (width - segment_size) // 2
    top = (height - segment_size) // 4
    right = left + segment_size
    bottom = top + segment_size

    # Crop the image to the center segment
    center_segment = image.crop((left, top, right, bottom))
    return center_segment

def calculate_pixel_ratio_difference(segment1, segment2):
    # Convert segments to grayscale for easy pixel comparison
    segment1 = segment1.convert('L')
    segment2 = segment2.convert('L')

    # Get the pixel data for the segments
    pixels1 = list(segment1.getdata())
    pixels2 = list(segment2.getdata())

    # Calculate the mean pixel values for each segment
    mean_pixel1 = sum(pixels1) / len(pixels1)
    mean_pixel2 = sum(pixels2) / len(pixels2)

    # Calculate the pixel ratio difference
    pixel_ratio_difference = (mean_pixel2 - mean_pixel1) / mean_pixel1

    return pixel_ratio_difference

def forward_check(image1, image2):
    # Define the size of the center segment (e.g., 100x100 pixels)
    segment_size = 100

    # Extract the center segment from each image
    center_segment1 = extract_center_segment(image1, segment_size)
    center_segment2 = extract_center_segment(image2, segment_size)

    # Calculate the pixel ratio difference
    pixel_ratio_difference = calculate_pixel_ratio_difference(center_segment1, center_segment2)

    # Determine if the center segment is zoomed in or zoomed out
    zoom_direction = "zoomed in" if pixel_ratio_difference > 0 else "zoomed out"

    # Print the pixel ratio difference and zoom direction
    print(f"Pixel Ratio Difference: {pixel_ratio_difference:.2%}")
    print(f"The center segment is {zoom_direction}.")

def left_check(image1, image2):
    # Define the size of the center segment (e.g., 100x100 pixels)
    segment_size = 100

    # Extract the center segment from each image
    center_segment1 = extract_left_segment(image1, segment_size)
    center_segment2 = extract_left_segment(image2, segment_size)

    # Calculate the pixel ratio difference
    pixel_ratio_difference = calculate_pixel_ratio_difference(center_segment1, center_segment2)

    # Determine if the center segment is zoomed in or zoomed out
    zoom_direction = "zoomed in" if pixel_ratio_difference > 0 else "zoomed out"

    # Print the pixel ratio difference and zoom direction
    print(f"Pixel Left Ratio Difference: {pixel_ratio_difference:.2%}")
    print(f"The Left segment is {zoom_direction}.")

def up_check(image1, image2):
    # Define the size of the center segment (e.g., 100x100 pixels)
    segment_size = 100

    # Extract the center segment from each image
    center_segment1 = extract_up_segment(image1, segment_size)
    center_segment2 = extract_up_segment(image2, segment_size)

    # Calculate the pixel ratio difference
    pixel_ratio_difference = calculate_pixel_ratio_difference(center_segment1, center_segment2)

    # Determine if the center segment is zoomed in or zoomed out
    zoom_direction = "zoomed in" if pixel_ratio_difference > 0 else "zoomed out"

    # Print the pixel ratio difference and zoom direction
    print(f"Pixel Up Ratio Difference: {pixel_ratio_difference:.2%}")
    print(f"The Up segment is {zoom_direction}.")

def main():
    # Load the images
    image1 = Image.open('image1.jpg')  # Replace with your image file path
    image2 = Image.open('image2.jpg')  # Replace with your image file path
    forward_check(image1,image2)
    left_check(image1,image2)
    up_check(image1,image2)

if __name__ == "__main__":
    main()
