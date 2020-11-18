# smart-door-facial-recognition



This application will try to simulate a system that allows a user to be granted access to a location using facial recognition. This applicaiton will be built on AWS. Here is a preliminary baseline architecture. 



![](images/door-architecture.png)



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

####  Lambda functions

* Created S3 bucket to use with cloudformation: smart-door-cloudformation-template
* Definitions inlcuded in `template.yaml` 

#### Additional Lambda Layer

* Used `sys.opt.append(/opt)` so lambda looks inside this directory for lambda layer





#### API Gateway
* API Definitions included in `yaml` files.
* Manually add all CORS Headers to ensure proper pre-flight authentication.

* Added complete definitions for both user / owner apis under wp1 and wp2.

* Deployed as static sites using S3 --> could add https with cloudfront and cognito


#### S3
1. Created b1-visitor-vault to store unstructured data
2. Could add more security to this bucket and add to IAC



#### DynamoDB

##### Visitors

##### Pascodes

* TTL -- passcodes only valid for 5 minutes.

### 

