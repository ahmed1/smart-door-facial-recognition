import json
import boto3



def index_faces(collection_id, bucket, photos, name):

    client = boto3.client('rekognition')
    
    f = open('rekognition_index_faces_output.txt', 'w')
    
    for idx, photo in enumerate(photos):
        response = client.index_faces(
            CollectionId=collection_id,
            Image={'S3Object': {'Bucket': bucket, 'Name': photo} },
            ExternalImageId=name,
            DetectionAttributes=['ALL'],
            QualityFilter="AUTO",
            MaxFaces=1
        )
        
        
        print ('Results for ' + photo)
        print('Faces indexed:')
        for faceRecord in response['FaceRecords']:
             print('  Face ID: ' + faceRecord['Face']['FaceId'])
             print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

        print('Faces not indexed:')
        for unindexedFace in response['UnindexedFaces']:
            print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
            print(' Reasons:')
            for reason in unindexedFace['Reasons']:
                print('   ' + reason)
                
        print("Faces indexed count: " + str(len(response['FaceRecords'])))
    
        f.write(str(idx) + ' ' + repr(response) + '\n')
        
    f.close()
    
    
def main():
    bucket = 'b1-vault'
    photos = ['ahmed-shoukr-photo-1.jpeg'] #, 'ahmed-shoukr-photo-2.jpeg', 'ahmed-shoukr-photo-3.jpeg', 'ahmed-shoukr-photo-4.jpeg']
    collection_id='Collection'
    index_faces(collection_id, bucket, photos, 'ahmed-shoukr')
    
    
    
if __name__ == '__main__':
    main()
