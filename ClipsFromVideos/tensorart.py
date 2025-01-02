import requests
import json
import base64

# Replace with your actual Tensor.art API key
API_KEY = '9uBX3ASjxWvNBAD1xjbVaKA74mWGZys3RGSF7DdeDD3F'

# Tensor.art API endpoint for image generation
API_URL = 'https://api.tensor.art/v1/images/generate'

# The specific model ID you want to use
MODEL_ID = '763947005736342551'  # Flux+Pony Real F1D

def generate_image(prompt, model_id=MODEL_ID, api_key=API_KEY, output_path='output_image.png'):
    """
    Generates an image from a prompt using Tensor.art's API.

    :param prompt: The text prompt to generate the image.
    :param model_id: The ID of the model to use for generation.
    :param api_key: Your Tensor.art API key.
    :param output_path: Path to save the generated image.
    :return: None
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model_id': model_id,
        'prompt': prompt,
        'num_images': 1,           # Number of images to generate
        'resolution': '1024x1024', # Desired resolution
        'response_format': 'base64' # To receive the image in base64
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for bad status codes

        data = response.json()

        # Assuming the API returns the image in base64 format
        if 'images' in data and len(data['images']) > 0:
            image_base64 = data['images'][0]
            image_bytes = base64.b64decode(image_base64)

            with open(output_path, 'wb') as img_file:
                img_file.write(image_bytes)

            print(f"Image successfully saved to {output_path}")
        else:
            print("No image data found in the response.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Example usage
if __name__ == '__main__':
    user_prompt = "A serene landscape with mountains during sunset, in the style of Flux+Pony Real F1D."
    generate_image(prompt=user_prompt)
