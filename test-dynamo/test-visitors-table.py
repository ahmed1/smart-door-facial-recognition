import json
import boto3
import datetime



def load_visitor(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
    table = dynamodb.Table('visitors')
    
    
    row = {}
    
    row['faceId'] = '9628194b-8333-42d2-ab41-203fa9943941'
    row['name'] = "Ahmed Shoukr"
    row['phoneNumber'] = "+14085691957"
    row['photos'] = []
    
    photo = {}
    photo['objectKey'] = 'ahmed-shoukr/photo1.jpg'
    photo['bucket'] = 'b1-vault'
    photo['createdTimestamp'] = str(datetime.datetime.now())
    
    row['photos'].append(photo)

    table.put_item(Item=row)
    
if __name__ == '__main__':
    load_visitor()
