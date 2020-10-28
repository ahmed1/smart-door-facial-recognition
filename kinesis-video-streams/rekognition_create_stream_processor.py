import json
import boto3


if __name__ == '__main__':


    client = boto3.client('rekognition')
    
    response = client.create_stream_processor(
        Input={
            'KinesisVideoStream': {
                'Arn': 'arn:aws:kinesisvideo:us-east-1:922059106485:stream/test/1603857719943'
            }
        },
        Output={
            'KinesisDataStream': {
                'Arn': 'arn:aws:kinesis:us-east-1:922059106485:stream/KDS1'
            }
        },
        Name='first-stream',
        Settings={
            'FaceSearch': {
                'CollectionId': 'Collection',
                'FaceMatchThreshold': 80.0
            }
        },
        RoleArn='arn:aws:iam::922059106485:role/Rekognition-Access-Role'
    )
    
    print(response)
    
    
"""
{'StreamProcessorArn': 'arn:aws:rekognition:us-east-1:922059106485:streamprocessor/first-stream', 'ResponseMetadata': {'RequestId': '04f0863a-c83c-4afc-b641-149240d062e1', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Wed, 28 Oct 2020 21:23:16 GMT', 'x-amzn-requestid': '04f0863a-c83c-4afc-b641-149240d062e1', 'content-length': '96', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
"""
