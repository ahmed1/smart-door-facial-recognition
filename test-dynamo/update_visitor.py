import boto3
import datetime


def update_visitor(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('visitors')
    
    photo = {}
    photo['objectKey'] = 'ahmed-shoukr/photo2.jpg'
    photo['bucket'] = 'b1-vault'
    photo['createdTimestamp'] = str(datetime.datetime.now())
    
    response = table.update_item(
        Key = {
            'faceId' : '9628194b-8333-42d2-ab41-203fa9943941'
        },
        UpdateExpression="SET photos = list_append(photos, :i)",
        ExpressionAttributeValues={
            ':i': [photo],
        },
        ReturnValues="UPDATED_NEW"
    )
#AttributeUpdates={
#    'photos': {
#        'Value': photo,
#        'Action': 'ADD'|'PUT'|'DELETE'
#    }
#},
#



if __name__ == '__main__':
    update_visitor()
