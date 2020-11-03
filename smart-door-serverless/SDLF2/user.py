import json
import sys

# import requests
sys.path.append("/opt")

import processing_lib

def lambda_handler(event, context):

    print('EVENT: ', event)


    passcode = str(event['Passcode'])
    user_id = str(event['UserId'])

    # try to query for person in passcodes
    if not processing_lib.check_passcode(external_id = user_id, user_passcode = passcode):
        res = "Permission Denied"
    else:
        user_name = processing_lib.get_user_name(external_id=user_id)
        res = 'Hello, {}. Your authentication is a success. You may enter!'.format(user_name)

        # put the person in visitors table
        # if not processing_lib.seen_before(user_id):
        # create new entry in visitors -- this happens in the owner piece

        # train on new person
        new_faces_appended = processing_lib.index_faces(external_id = user_id)
        assert new_faces_appended == 1, "No Face has been trained error."
            



    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        "body": str(res)
    }
