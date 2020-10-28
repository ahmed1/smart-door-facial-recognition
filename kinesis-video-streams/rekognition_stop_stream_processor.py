import json
import boto3

# should combine this with start_stream_processor

if __name__ == '__main__':

    client = boto3.client('rekognition')

    response = client.stop_stream_processor(
        Name='first-stream'
    )

    print(response)
