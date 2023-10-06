import requests
import base64
from io import BytesIO
from PIL import Image
import json
import time

def save_base64_image_to_jpg(base64_data, output_path):
    try:
        # Decode base64 data
        image_data = base64.b64decode(base64_data)
        
        # Create a BytesIO object to work with the image data
        image_stream = BytesIO(image_data)
        
        # Open the image using PIL (Python Imaging Library)
        img = Image.open(image_stream)
        
        # Save the image as a JPEG file
        img.save(output_path, "JPEG")
        
        print(f"Image saved to {output_path} successfully.")
    except Exception as e:
        print("An error occurred:", str(e))

def got_the_response_from_image(response,requirementresponse):
            data = response.json()
            for i in data['images']:
                save_base64_image_to_jpg(i,"D:\\Programs\\Python-Tutorials\\Resize\\Images\\output.png")
                # Replace with the URL of your Laravel endpoint
                url = 'http://206.189.128.208/api/upload_stableDiffusion_file'

                # Replace 'file.jpg' with the path to your JPEG file
                files = {'file': ('file.jpg', open('D:\\Programs\\Python-Tutorials\\Resize\\Images\\output.png', 'rb'), 'image/jpeg'),
                         }
                payload={'id':requirementresponse['id'],'positive_prompt':requirementresponse['positive_prompt']}
                response = requests.post(url, data=payload,files=files)
                if response.status_code == 200:
                    print("File uploaded successfully")
                else:
                    print("File upload failed")

def generate_images():
    requirementresponse=requests.post(url='http://206.189.128.208/api/check_for_image_job')
    if(requirementresponse.text.strip() == "NothingToProceed"):
        print("Nothing to proceed")
        #retry after 30 min
        time.sleep(1000)
        generate_images()
    else:
        #process the data and upload back to the server
        #if having the quantity then random the seed
        # payload = {
        # "prompt": "pretty xeg",
        # "steps": 10,
        # "cfg_scale": 5,
        # "sampler_index": "Euler a",
        # "width": 500,
        # "height": 500
        # }

        print("Requirement="+requirementresponse.text)
        response = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/txt2img', json=requirementresponse.json())  
        print("Output="+response.text)
        got_the_response_from_image(response,requirementresponse.json())
        try:
            #got_the_response_from_image(response,requirementresponse.json())
            time.sleep(1)
        except:
            pass
      
        generate_images()
generate_images()