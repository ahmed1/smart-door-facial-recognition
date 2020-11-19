# smart-door-facial-recognition

---

This application will try to simulate a system that allows a user to be granted access to a location using facial recognition. This applicaiton will be built on AWS. Here is a preliminary baseline architecture. 

## Architecture Overview

---

![](images/door-architecture.png)



## Individual Components

---

###### All code for serveless application, including lambda functions, lambda layer, test / deploy scripts included.

#### S3

* Used to host static web pages `wp1-owner` and `wp2-user`
* Used to deploy infrastructure templates to Cloudformation (and for version control)
* Used to persist photos of users in the database

#### API Gateway

* API Definitions included in `yaml` files.
* Manually add all CORS Headers to ensure proper pre-flight authentication.
  * Includes `Access-Control-Allow-Headers, Access-Control-Allow-Origin, Access-Control-Allow-Credentials, Access-Control-Allow-Methods` in `Method Response` under `OPTIONS` and `POST`
  * Also added `Content-Type, X-Amz-Date, Authorization, X-APi-Key, X-Amz-Security-Token', '*', 'true', POST'` in `Integration Response` under `OPTIONS` and `POST`. 
* Added complete swagger definitions for both user / owner apis under wp1 and wp2.
* Deployed as static sites using S3. In the future, I could add https with cloudfront and cognito.

#### Kinesis Video Streams

* Used to stream video using GStreamer

#### Rekognition

* sample in `index_faces.py`
* Set up automatic pipeline to train on new authenticated people

#### Kinesis Data Streams

* Using 1 open shard
* Retains data for 24 hours 

#### GStreamer C++ SDK

* Built without using docker version
* `cmake` with `-DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_JNI=TRUE`

```shell
export PATH=/path/to/gcc-4.9.2/bin/:$PATH
export LD_LIBRARY_PATH=/path/to/gcc-4.9.2/lib64/:$LD_LIBRARY_PATH
./configure --prefix=/path/to/  --host=arm
```

* Used `width=640, height=480, framerate=10, bitrate=500` for streaming

* https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp

#### Stream Processor

* Need to create Stream Processor between Kinesis Video / Data Streams and Rekogintion
* Created using `kinesis-video-streams/rekognition_start_stream_processor.py` 
* Can check status using: 

```shell
aws rekognition list-stream-processors
# Status should be "Running"
{
    "StreamProcessors": [
        {
            "Name": "first-stream",
            "Status": "RUNNING"
        }
    ]
}
```



#### SAM CLI

* Used to develop / test application locally
* Used docker 2.4.0.0
* Used this script for deploying to s3 bucket `smart-door-cloudformation-template` , then cloudformation to create stack:

```shell
# this also helped keep different versions of deployment persisted in blob storage
sam build --use-container --template-file template.yaml
sam package --s3-bucket smart-door-cloudformation-template --output-template-file packaged.yaml
sam deploy --template-file ./packaged.yaml --stack-name smart-door-message-handler --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
```



####  Lambda functions

* Created S3 bucket to use with cloudformation: smart-door-cloudformation-template
* Definitions inlcuded in `template.yaml` 
* All code dockerized with `requirements.txt` for additional packages used such as `opencv-contrib-python` for `SDLF1`

```yaml
# Lambda Function setup with Lambda Layer:
Resources:
  SDLF0Function:
    Type: AWS::Serverless::Function 
    Properties:
      FunctionName: SDLF0
      CodeUri: ./SDLF0/
      Handler: owner.lambda_handler
      Runtime: python3.7
      Layers:
      - !Ref ProcessingLayer
```

* Note, must include `sys.path.append("/opt")` in any lambda function using this layer so it looks in this directory for the layer.

* Note, to allow streaming to work properly, I used the following configuration for `SDLF1`: 
  * `Batch size: 100`, `Batch window: 30`, `Concurent batches per shard: 1`



#### Additional Lambda Layer



* Used `sys.opt.append(/opt)` so lambda looks inside this directory for lambda function acting as lambda layer
* Used to give good separation of concerns for the lambda functions.

```python
# used fragment_number to extract image of person
client = boto3.client('kinesis-video-media', endpoint_url=endpoint , region_name = 'us-east-1')

    response = client.get_media(
        StreamARN=stream_arn,
        StartSelector={
            'StartSelectorType': 'FRAGMENT_NUMBER',
            'AfterFragmentNumber': fragment_number
        }
    )

```



```python
# also used open-cv to capture the frame to store in s3 and send to owner or train after authenticated
cap = cv2.VideoCapture(fname)
ret, frame = cap.read()
cv2.imwrite(img_temp_name, frame)
```

#### DynamoDB

##### Visitors

* Visitors table includes `face_id`, `name`, `phoneNumber`, `photos` list

##### Pascodes

* TTL -- passcodes only valid for 5 minutes
  * Note: this may not be instant in dynamodb
* Only valid for user one time, then they are deleted



##### Note: Once a new User is authenticated, the simulator will automatically train on their image so they are authenticated automatically in the future.

