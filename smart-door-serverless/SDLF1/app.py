import json
import boto3
import base64
import requests
import sys
from random import randint
import cv2

def extract_face(fragment_number):
    stream_arn = 'arn:aws:kinesisvideo:us-east-1:922059106485:stream/test/1603857719943'


    kinesis_client = boto3.client('kinesisvideo',region_name='us-east-1')

    endpoint = kinesis_client.get_data_endpoint(StreamARN=stream_arn, APIName='GET_MEDIA')
    endpoint = endpoint['DataEndpoint']




    start_selector_type = 'FRAGMENT_NUMBER'

    client = boto3.client('kinesis-video-media', endpoint_url=endpoint , region_name = 'us-east-1')

    response = client.get_media(
        StreamARN=stream_arn,
        StartSelector={
            'StartSelectorType': 'FRAGMENT_NUMBER',
            'AfterFragmentNumber': fragment_number
        }
    )

    print(response)
    print('exiting')
    frame = response['Payload'].read()

    with open('/tmp/stream.avi', 'wb') as f:
        f.write(frame)
        cap = cv2.VideoCapture('file.mvi')




def generate_otp():
    return randint(100000, 999999)

def lambda_handler(event, context):
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
        pass


    # Face Not Seen Before
    elif len(data['FaceSearchResponse'][0]['MatchedFaces']) == 0:
    # Need to extract face
        pass




    # Face Seen Before
    # take match with highest confidence
    # use sns to send push notification to visitor
    # need to extract face
    else: 
        matched_faces = [(matched_face['Similarity'], matched_face['Face']['ExternalImageId']) for matched_face in data['FaceSearchResponse'][0]['MatchedFaces']]
        top_match = sorted(matched_faces, key = lambda elem : elem[0])[0]
        external_id = top_match[1]

        # Extract Face
        extract_face(fragment_number = data['InputInformation']['KinesisVideo']['FragmentNumber']) # still need to see what this will return 

        # generate OTP
        otp = generate_otp()

        # Store OTP in passcodes table with external_id as key (this will automatically occur with the post request?)

        client = boto3.client('sns')
        phone_number = '+14085691957'
        client.publish(PhoneNumber=phone_number, Message = notification)



    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Under Development",

        }),
    }
