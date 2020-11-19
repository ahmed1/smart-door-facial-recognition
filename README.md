# smart-door-facial-recognition



This application will try to simulate a system that allows a user to be granted access to a location using facial recognition. This applicaiton will be built on AWS. Here is a preliminary baseline architecture. 



![](images/door-architecture.png)



###### All code for serveless application, including lambda functions, lambda layer, test / deploy scripts included.



#### Kinesis Video Streams

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

#### Additional Lambda Layer

* Used `sys.opt.append(/opt)` so lambda looks inside this directory for lambda function acting as lambda layer
* Used to give good separation of concerns for the lambda functions.

#### API Gateway
* API Definitions included in `yaml` files.
* Manually add all CORS Headers to ensure proper pre-flight authentication.

* Added complete definitions for both user / owner apis under wp1 and wp2.

* Deployed as static sites using S3 --> could add https with cloudfront and cognito


#### S3
1. Created b1-visitor-vault to store unstructured data
2. Could add as IAC 

#### DynamoDB

##### Visitors

* Visitors table includes `face_id`, `name`, `phoneNumber`, `photos` list

##### Pascodes

* TTL -- passcodes only valid for 5 minutes
  * Note: this may not be instant in dynamodb
* Only valid for user one time, then they are deleted



##### Note: Once a new User is authenticated, the simulator will automatically train on their image so they are authenticated automatically in the future.