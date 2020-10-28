import json
import boto3
import datetime



def load_visitor(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
    table = dynamodb.Table('visitors')
    
    
    row = {}
    
    row['faceId'] = "1234"
    row['name'] = "Jane Doe"
    row['phoneNumber'] = "+12345678901"
    row['photos'] = [
        {
            "objectKey" : "my-photo.jpg",
            "bucket" : "b1-visitor-vault",
            "createdTimestamp" : str(datetime.datetime.now())
        
        
        }
    ]

    table.put_item(Item=row)
    
if __name__ == '__main__':
    load_visitor()
