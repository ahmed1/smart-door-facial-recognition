import json
import boto3


if __name__ == '__main__':
    client = boto3.client('dynamodb')
    
    res = client.get_item(TableName = 'visitors', Key = {'faceId' : {'S' : '1234'}   }  )
    
    print("Bucket: ", res['Item']['photos']['L'][0]['M']['bucket']['S'])
    print("Path Key: ", res['Item']['photos']['L'][0]['M']['objectKey']['S'])

