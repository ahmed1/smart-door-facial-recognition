import json
import boto3

from datetime import datetime, timezone, timedelta
import time
      
if __name__ == '__main__':

    client = boto3.client('dynamodb')
    
    res = client.get_item(TableName='passcodes', Key = {'faceId' : {'S': "125" }} )
    
    
    # need to check if key is still available
    print(res['Item']['passcode']['S'])
