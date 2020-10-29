import json
import jwt
import base64
import requests


def lambda_handler(event, context):
    """
    The event contains records given by Kinesis Data Streams Service: 
    https://docs.aws.amazon.com/kinesis/latest/APIReference/API_Record.html

    Message is Base64-encoded binary data object 

    """

    base64_img = event['Records'][0]['kinesis']['data']
    base64_img_bytes = base64_img.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    decoded_image_data = decoded_image_data.decode('utf-8')

    data = eval(decoded_image_data)

    print(data)



    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Under Development",

        }),
    }
