import json
import boto3


if __name__ == '__main__':
    client = boto3.client('dynamodb')
    
    image_key = client.get_item(TableName = 'visitors', Key = {'faceId' : {'S' : 'ahmed-shoukr'}   }  )
    
    print(image_key['Item']['photos']['L'][-1]['M']['objectKey']['S'])
    print()
    print(image_key.keys())
#    print(photos)
#    print(len(photos['Item']['photos']['L'])) # gives number of photos stored
#
#    print("Bucket: ", photos['Item']['photos']['L'][0]['M']['bucket']['S'])
#    print("Path Key: ", photos['Item']['photos']['L'][0]['M']['objectKey']['S'])
#
