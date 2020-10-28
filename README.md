# smart-door-facial-recognition



This application will try to simulate a system that allows a user to be granted access to a location using facial recognition. This applicaiton will be built on AWS. Here is a preliminary baseline architecture. 



![](images/door-architecture.png)




#### Notes to deploy lambda function
1. Created S3 bucket to use with cloudformation: smart-door-cloudformation-template
2. Function names must be alphanumeric.



#### API Gateway
1. Manually add all CORS Headers to ensure proper pre-flight authentication.
2. Added complete definitions for both user / owner apis under wp1 and wp2.


#### S3
1. Created b1-visitor-vault to store unstructured data
2. Could add more security to this bucket and add to IAC
