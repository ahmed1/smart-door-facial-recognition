import json
import sys


# Required for loading of local data clean package
sys.path.append("/opt")

import processing_lib



def lambda_handler(event, context):

    print('EVENT: ', event)

    name = str(event['Name'])
    user_id = str(event['UserId'])
    phone_number = str(event['PhoneNumber'])

    # no additional validation since owner entering information means they allow the person in

    # generates and puts the message in the passcodes table with ttl
    temp_passcode = processing_lib.load_passcode(external_id = user_id)

    # create new entry in visitors -- this happens in the owner piece
    processing_lib.append_visitor_photo(external_id=user_id, name=name, phone_number=phone_number)

    # Send SMS to user
    processing_lib.send_sns_request_to_user(external_id = user_id, temp_passcode = temp_passcode)
    

    #     raise e
    res = "This just needs to tell the owner that it has taken the information"
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        "body": str(res)
    }
