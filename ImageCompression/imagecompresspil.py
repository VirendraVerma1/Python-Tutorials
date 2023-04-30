
from PIL import Image
import os

def compress_image(image_path, output_path):
    with Image.open(image_path) as img:
        img.save(output_path, optimize=True)

