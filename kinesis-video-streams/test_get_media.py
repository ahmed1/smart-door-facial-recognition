import boto3
import cv2



def save_face_tmp(fname, external_id, num_images):

    img_s3_names = []
    img_temp_names = []
    print('did not get here')
    cap = cv2.VideoCapture(fname) # ERROR
    print('did not get here 1')
    num_imgs_saved = 0
    while (cap.isOpened() and num_imgs_saved < 2):
        ret, frame = cap.read()
        if ret == False:
            print('Ran out of bytes')
            break
            
        img_s3_name = external_id + '/' + 'image' + str(num_images) + '.jpeg'
        img_s3_names.append(img_s3_name)
        
        img_temp_name = 'tmp/image' + str(num_images) + '.jpeg'
        img_temp_names.append(img_temp_name)
        cv2.imwrite(img_temp_name, frame)
        num_imgs_saved += 1
        num_images +=1
    
    return img_s3_names, img_temp_names

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
    print('got here')
    fname = 'tmp/' + external_id + '.webm'
    with open(fname, 'wb+') as f:
        chunk = response['Payload'].read(50000)
        f.write(chunk)
    print('got here 1')
    """
    extract images from video and write them to /tmp/ path
    """
    img_s3_names, img_temp_names = save_face_tmp(fname, external_id, num_images)
    # function worked
    print(img_s3_names, img_temp_names)
    print()
    print()

    return img_s3_names, img_temp_names

def save_face_s3(img_s3_names, img_temp_names):
    s3 = boto3.client('s3')
    
    for idx, img_name in enumerate(img_s3_names):
        s3.put_object(Bucket = 'b1-vault', Key = img_name, Body = open(img_temp_names[idx], 'rb').read() )

    return img_s3_names, img_temp_names
    
    
if __name__ == '__main__':
    fragment_number = '91343852333181551289395195757640299498191282805'
    extract_face(fragment_number, 'new_person_15', 3) # will depend on number of people in dynamo
