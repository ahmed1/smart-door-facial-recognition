import json
import boto3
import base64
import requests
import sys
from random import randint

from datetime import datetime, timezone, timedelta
import uuid

def extract_event(event):
    """
    for idx in range(len(event['Records'])):
    Only taking first Record given
    """
    base64_img = event['Records'][0]['kinesis']['data']
    base64_img_bytes = base64_img.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    decoded_image_data = decoded_image_data.decode('utf-8')
    data = eval(decoded_image_data)
    return data

def get_num_images_from_visitors(external_id):
    client = boto3.client('dynamodb')
    photos = client.get_item(TableName = 'visitors', Key = {'faceId' : {'S' : external_id}   }  )
    
    num_images = len(photos['Item']['photos']['L'])
    return num_images
    
    
def save_face_tmp(fname, external_id, num_images):
    import cv2
    img_s3_names = []
    img_temp_names = []
    
    cap = cv2.VideoCapture(fname) # ERROR
    
    num_imgs_saved = 0
    while (cap.isOpened() and num_imgs_saved < 1):
        ret, frame = cap.read()
        if ret == False:
            print('Ran out of bytes')
            break
            
        img_s3_name = external_id + '/' + 'image' + str(num_images) + '.jpeg'
        img_s3_names.append(img_s3_name)
        
        img_temp_name = '/tmp/image' + str(num_images) + '.jpeg'
        img_temp_names.append(img_temp_name)
        cv2.imwrite(img_temp_name, frame)
        num_imgs_saved += 1
        num_images +=1
    
    return img_s3_names, img_temp_names
    
def save_face_s3(img_s3_names, img_temp_names):
    s3 = boto3.client('s3')
    
    for idx, img_name in enumerate(img_s3_names):
        s3.put_object(Bucket = 'b1-vault', Key = img_name, Body = open(img_temp_names[idx], 'rb').read() )
        # setting public read for link
        
        
     # should verify response here
    return img_s3_names, img_temp_names

# only use for first time visitor to send url in sms
def make_imgs_public(img_s3_names):
    s3_resource = boto3.resource('s3')
    for img_name in img_s3_names: # should just use 1 for now
        object_acl = s3_resource.ObjectAcl('b1-vault', img_name)
        response = object_acl.put(ACL='public-read')

    return img_s3_names
    
def append_photo_visitors(img_s3_names):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('visitors')
    for img_name in img_s3_names:
        photo = {}
        photo['objectKey'] = img_name
        photo['bucket'] = 'b1-vault'
        photo['createdTimestamp'] = str(datetime.datetime.now())
        
        response = table.update_item(
            Key = {
                'faceId' : img_name.split('/')[0]
            },
            UpdateExpression="SET photos = list_append(photos, :i)",
            ExpressionAttributeValues={
                ':i': [photo],
            },
            ReturnValues="UPDATED_NEW"
        )
    return img_s3_names

def extract_face(fragment_number, external_id, num_images):
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

#    print(response)
    """
    Extracting data so far into .webm video file
    """
    
    fname = '/tmp/' + external_id + '.webm'
    with open(fname, 'wb+') as f:
        chunk = response['Payload'].read(50000)
        f.write(chunk)
    
    """
    extract images from video and write them to /tmp/ path
    """
    img_s3_names, img_temp_names = save_face_tmp(fname, external_id, num_images)
    # function worked
    
    img_s3_names, img_temp_names = save_face_s3(img_s3_names, img_temp_names)
    
    
    return img_s3_names, img_temp_names




def generate_otp():
    return randint(100000, 999999)
    
def generate_rand_uuid():
     return uuid.uuid4().hex
    
    
    
def load_passcode(dynamodb = None, external_id = None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
    table = dynamodb.Table('passcodes')
    temp_passcode = generate_otp()
    row = {}
    row['faceId'] = external_id
    row['passcode'] = temp_passcode
    second_offset = 300
    timetolive = round((datetime.now(tz=timezone.utc) - datetime(1970, 1,1, tzinfo=timezone.utc) + timedelta(seconds=second_offset)).total_seconds())
    row['ttl'] = timetolive
    table.put_item(Item=row)
    return temp_passcode

def check_passcode(dynamodb = None, external_id = None, user_passcode):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
    table = dynamodb.Table('passcodes')
    
    passcode = client.get_item(TableName = 'visitors', Key = {'faceId' : {'S' : external_id}   }  )
    if 'Item' in passcode.keys():
        passcode = passcode['Item']['passcode']['S']
        if passcode == user_passcode:
            return True
        else:
            return False
    else:
        return False
    

def get_user_phone_number(external_id):
    client = boto3.client('dynamodb')
    user = client.get_item(TableName = 'visitors', Key = {'faceId' : {'S' : external_id}   }  )
    return user['Item']['phoneNumber']['S']
    
def get_user_name(external_id):
    user = client.get_item(TableName = 'visitors', Key = {'faceId' : {'S' : external_id}   }  )
    return user['Item']['name']['S']
    
def send_sns_request_to_user(external_id, temp_passcode):
    
    client = boto3.client('sns')
    phone_number = get_user_phone_number(external_id)
    url = 'https://s4el8lc5m2.execute-api.us-east-1.amazonaws.com/dev/annex-user'
    notification = "Hello there, welcome to the door simulation. Please enter the passcode and ID provided in this url webpage. URL: {} Passcode: {} ID: {}".format(url, temp_passcode, external_id)
    res = client.publish(PhoneNumber=phone_number, Message = notification)


def construct_url_for_unknown_user_image(img_s3_names):
    return ['https://b1-vault.s3.amazonaws.com/' + img_key for img_key in img_s3_names][0]

def send_sns_request_to_owner(external_id, img_s3_names):
    client = boto3.client('sns')
    
    phone_number = '+14085691957'
    post_url = 'https://pz7u792kx7.execute-api.us-east-1.amazonaws.com/dev/annex-owner'
    img_url = construct_url_for_unknown_user_image(img_s3_names)
    
    
    notification = "Hello owner, there is a user trying to use the door simulation. Please use the url to provide their name and phone number if you would like to give them access. URL: {} Their picture: {} ID: ".format(post_url, img_url, external_id)
    res = client.publish(PhoneNumber=phone_number, Message = notification)


def seen_before(external_id):
    client = boto3.client('dynamodb')
    
    person = client.get_item(TableName = 'visitors', Key = {'faceId' : {'S' : external_id}   }  )
    if 'Item' in person.keys():
        return True
    else:
        return False
        









def append_visitor_photo(external_id, name, phone_number): # not yet used -- this is in the owner section
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('visitors')
    
    
    row = {}
    
    row['faceId'] = external_id
    row['name'] = name
    row['phoneNumber'] = phone_number
    row['photos'] = []
    
    photo = {}
    photo['objectKey'] = external_id + '/image0.jpeg'
    photo['bucket'] = 'b1-vault'
    photo['createdTimestamp'] = str(datetime.datetime.now())
    
    row['photos'].append(photo)

    table.put_item(Item=row)
    
    
def index_faces(external_id):



    client = boto3.client('rekognition')
    
    
    photo = external_id + '/' + 'image0.jpeg'
    bucket = 'b1-vault'
    collection_id = 'Collection'

    response = client.index_faces(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket, 'Name': photo} },
        ExternalImageId=external_id,
        DetectionAttributes=['ALL'],
        QualityFilter="AUTO",
        MaxFaces=1
    )
    
    return str(len(response['FaceRecords'])) # should be 1 indexed face
    
