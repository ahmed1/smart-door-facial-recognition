import json
import boto3
import base64
import requests
import sys
from random import randint
import cv2

sys.path.append("/opt")
import processing_lib

def lambda_handler(event, context):
    print(event)
    """
    The event contains records given by Kinesis Data Streams Service: 
    https://docs.aws.amazon.com/kinesis/latest/APIReference/API_Record.html

    Message is Base64-encoded binary data object 

    """
    # for idx in range(len(event['Records'])):
    # Only taking first Record given
    base64_img = event['Records'][0]['kinesis']['data']
    base64_img_bytes = base64_img.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    decoded_image_data = decoded_image_data.decode('utf-8')

    data = eval(decoded_image_data)

    # print(data)

    # Check for face
    # No Face
    if len(data['FaceSearchResponse']) == 0:
        # sys.exit()
        print('No Faces Detected')
        pass


    # Face Not Seen Before
    elif len(data['FaceSearchResponse'][0]['MatchedFaces']) == 0:
    # Need to extract face
        print('Not Seen Face Before')
        pass




    # Face Seen Before
    # take match with highest confidence
    # use sns to send push notification to visitor
    # need to extract face
    else: 
        matched_faces = [(matched_face['Similarity'], matched_face['Face']['ExternalImageId']) for matched_face in data['FaceSearchResponse'][0]['MatchedFaces']]
        top_match = sorted(matched_faces, key = lambda elem : elem[0])[0]
        external_id = top_match[1]

        # Need number of images stored in Dynamo for known person



        # Extract Face and put in S3
        # img_s3_names contains keys for all images inserted in S3
        img_s3_names, img_temp_names = processing_lib.extract_face(fragment_number = data['InputInformation']['KinesisVideo']['FragmentNumber'], external_id=external_id) # still need to see what this will return 

        
        print(img_s3_names)
        
        # generate OTP
        otp = processing_lib.generate_otp()

        # Store OTP in passcodes table with external_id as key (this will automatically occur with the post request?)

        """
        client = boto3.client('sns')
        phone_number = '+14085691957'
        client.publish(PhoneNumber=phone_number, Message = notification)
        """


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Under Development",

        }),
    }
