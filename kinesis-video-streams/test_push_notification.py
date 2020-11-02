import boto3
import json

import base64


if __name__ == '__main__':


    url = "https://pz7u792kx7.execute-api.us-east-1.amazonaws.com/dev/annex-owner"
    temp_face_id = "123456"
    test_notification = "Would you like to let: " + temp_face_id + " in?"


#    s3 = boto3.client('s3')
#    s3.put_object(Bucket = 'b1-vault', Key = img_name, Body = open(img_temp_names[idx], 'rb').read() )

    client = boto3.client('sns')
    phone_number = '+14085691957'
    
    img = open('tmp/image10.jpeg', 'rb').read()
    
#    print(type(img))
#    img = base64.b64encode(img)
#    print(type(img)) b"\x02\x03\x04"
    response = client.publish(
        PhoneNumber=phone_number,
        Message = "Would you like to let this person in: https://b1-vault.s3.amazonaws.com/new_person_2/image5.jpeg"
    )
#        MessageAttributes = {
#            'store' : {"DataType": "Binary", "BinaryValue": str(base64.b64encode(img))}
#        }
#    )
    print(response)
