import json
import boto3
import base64
import requests
import sys
from random import randint
import cv2


def save_face(fname, external_id):

    img_s3_names = []
    img_temp_names = []
    cap = cv2.VideoCapture(fname)
    num_imgs_saved = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            print('Ran out of bytes')
            break
            
        img_s3_name = external_id + '/' + 'image' + str(num_imgs_saved) + '.jpeg'
        img_s3_names.append(img_s3_name)
        
        img_temp_name = '/tmp/image' + str(num_imgs_saved) + '.jpeg'
        img_temp_names.append(img_temp_name)
        cv2.imwrite(img_temp_name, frame)
        num_imgs_saved += 1
    
    return img_s3_names, img_temp_names

def extract_face(fragment_number, external_id):
    stream_arn = 'arn:aws:kinesisvideo:us-east-1:922059106485:stream/test/1603857719943'


    kinesis_client = boto3.client('kinesisvideo',region_name='us-east-1')

    endpoint = kinesis_client.get_data_endpoint(StreamARN=stream_arn, APIName='GET_MEDIA')
    endpoint = endpoint['DataEndpoint']

    client = boto3.client('kinesis-video-media', endpoint_url=endpoint , region_name = 'us-east-1')

    response = client.get_media(
        StreamARN=stream_arn,
        StartSelector={
            'StartSelectorType': 'FRAGMENT_NUMBER',
            'AfterFragmentNumber': fragment_number
        }
    )

    print(response)
    fname = '/tmp/' + external_id + '.webm'
    with open(fname, 'wb+') as f:
        chunk = response['Payload'].read(50000)
        f.write(chunk)
        
    # call function
    img_s3_names, img_temp_names = save_face(fname, external_id)
    # function worked
    print(img_s3_names, img_temp_names)
    print()
    print()


    
    s3 = boto3.client('s3')
    
    for idx, img_name in enumerate(img_s3_names):
        s3.put_object(Bucket = 'b1-vault', Key = img_name, Body = open(img_temp_names[idx], 'rb').read() )

    return img_s3_names, img_temp_names


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
        extract_face(fragment_number = data['InputInformation']['KinesisVideo']['FragmentNumber'], external_id='new_person_2') # still need to see what this will return 

        # generate OTP
        otp = generate_otp()

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
