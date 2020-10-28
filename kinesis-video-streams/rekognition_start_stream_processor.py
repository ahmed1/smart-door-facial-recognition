import json
import boto3


if __name__ == '__main__':

    client = boto3.client('rekognition')
    
    response = client.start_stream_processor(
        Name='first-stream'
    )
    
    print(response)
