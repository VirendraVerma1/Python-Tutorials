import requests
import time
import json


def publish_image():
    access_token="EAAOznWqhZAMsBO541Oe14MMk4pG7Pj1dNnfmTgiAD6EQxMEq49tls752VaXLA2mZBcE65jV1gzzEGZACUjZCTJNu4jmPtlyakCIbBjptJznBsyQZBuZAV01h2XEZAwrUXWdWU2UMQxMFU8Fhupz5qbE4oGOBKy5IXoeloxKwTHEZAoBNCNBlIjqQLliS4hlqhTvIcpdbK0JY"
    ig_user_id="17841459055279560"
    image_url="http://206.189.128.208/Post/test1.png"

    post_url="https://graph.facebook.com/v18.0/{}/media".format(ig_user_id)
    payload={
        'image_url':image_url,
        'caption':"Instagram Graph API test",
        'access_token':access_token
    }
    r=requests.post(post_url,data=payload)
    print(r.text)

    results=json.loads(r.text)
    if 'id' in results:
        creation_id=results['id']
        second_url="https://graph.facebook.com/v18.0/{}/media_publish".format(ig_user_id)  
        second_payload={
            'creation_id':creation_id,
            'access_token':access_token
        }  
        r=requests.post(second_url,data=second_payload)
        print(r.text)
        print("Image published to instagram")
    else:
        print('image posting is not possible')
publish_image()