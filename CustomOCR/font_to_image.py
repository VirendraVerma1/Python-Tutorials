import os
from PIL import Image, ImageDraw, ImageFont

# Get all the fonts under "Fonts" folder
fonts = os.listdir("Fonts")

# Filter for .ttf fonts
ttf_fonts = [font for font in fonts if font.endswith(".ttf")]

print("TTF Fonts:", ttf_fonts)

# Create a directory to save the images
if not os.path.exists("Images"):
    os.makedirs("Images")

# Create an image for each alphabet character from each .ttf font
for font_name in ttf_fonts:
    font_path = os.path.join("Fonts", font_name)
    for char in "1":
        # Create a blank image
        image = Image.new('RGB', (100, 100), color=(73, 109, 137))

        # Get a drawing context
        d = ImageDraw.Draw(image)

        # Define the font
        fnt = ImageFont.truetype(font_path, 40)

        # Draw text
        d.text((10,10), char, font=fnt, fill=(255, 255, 0))

        # Save the image in the "Images" folder
        image.save(os.path.join("Images", f"{font_name}_{char}.png"))
