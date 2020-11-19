import boto3

def delete_passcode(dynamodb=None, external_id=None):
    if not dynamodb:
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('passcodes')
    response = table.delete_item(Key = {'faceId': str(external_id)})
    print(response)
    return response

if __name__ == '__main__':
    delete_passcode(external_id='1234')
