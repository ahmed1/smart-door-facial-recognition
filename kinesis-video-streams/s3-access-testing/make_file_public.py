import boto3

if __name__ == '__main__':
    
    s3 = boto3.client('s3')
    

    img = open('../tmp/image10.jpeg', 'rb').read()
    response = s3.put_object(Bucket = 'b1-vault', Key = 'test6/img.jpeg', Body = img )
    
    print(response)
    
    
    
    s3 = boto3.resource('s3')
    object_acl = s3.ObjectAcl('b1-vault','test3/img.jpeg')
    response = object_acl.put(ACL='public-read')
    print()
    print(response)
    
