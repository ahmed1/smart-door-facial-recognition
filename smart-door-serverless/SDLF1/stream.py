import json
import boto3
import base64
import requests
import sys
from random import randint
import cv2
from datetime import datetime, timezone, timedelta

# required for lambda layer
sys.path.append("/opt")
import processing_lib

def lambda_handler(event, context):
    """
    The event contains records given by Kinesis Data Streams Service: 
    https://docs.aws.amazon.com/kinesis/latest/APIReference/API_Record.html

    Message is Base64-encoded binary data object 

    """
    # print(event)
    


    data = processing_lib.extract_event(event)


    # No Face
    if len(data['FaceSearchResponse']) == 0:

        print('No Faces Detected')
        pass


    # Face Not Seen Before
    elif len(data['FaceSearchResponse'][0]['MatchedFaces']) == 0:
    # Need to extract face
        print('Not Seen Face Before')
        
        external_id = processing_lib.generate_rand_uuid()

        img_s3_names, img_temp_names = processing_lib.extract_face(fragment_number = data['InputInformation']['KinesisVideo']['FragmentNumber'], external_id=external_id, num_images = 0) # still need to see what this will return 
        img_s3_names = processing_lib.make_imgs_public(img_s3_names)

        if not img_s3_names:
            print('Was not able to write images to s3')
        print(img_s3_names)

        
        """
        1. Send owner SMS with url and photo (URL) -> they can give back name and phone number
        2. No other concerns here
        """
        processing_lib.send_sns_request_to_owner(external_id=external_id, img_s3_names=img_s3_names)



    # Face Seen Before
    # take match with highest confidence
    # use sns to send push notification to visitor
    # need to extract face
    else:
        # get external-id of person
        matched_faces = [(matched_face['Similarity'], matched_face['Face']['ExternalImageId']) for matched_face in data['FaceSearchResponse'][0]['MatchedFaces']]
        top_match = sorted(matched_faces, key = lambda elem : elem[0])[0]
        external_id = top_match[1]
        print(external_id)

        # Need number of images stored in Dynamo for known person
        face_id = data['FaceSearchResponse'][0]['MatchedFaces'][0]['Face']['FaceId'] # not being used

        num_images = processing_lib.get_num_images_from_visitors(external_id = external_id)


        """
        1. Extract 50k bytes
        2. Write .webm video in /tmp
        3. Write .jpeg files in /tmp
        4. Store in s3 and return the keys
        """
        img_s3_names, img_temp_names = processing_lib.extract_face(fragment_number = data['InputInformation']['KinesisVideo']['FragmentNumber'], external_id=external_id, num_images = num_images+1) # still need to see what this will return 
        if not img_s3_names:
            print('Was not able to write images to s3')
        print(img_s3_names)
        

        """
        1. Generate OTP
        2. Put passcode in visitors table
        3. Return passcode to be sent to user 
        """
        temp_passcode = processing_lib.load_passcode(external_id = external_id)
        print(external_id, temp_passcode)

        """
        1. Generate URLs - not valid url constructed right now
        2. Get the person's phone number from visitors table
        2. Send person notification with form and allow them to enter the passcode 
        """
        processing_lib.send_sns_request_to_user(external_id = external_id, temp_passcode=temp_passcode)
    


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Success",

        }),
    }
