import boto3

def delete_faces_from_collection(collection_id, faces):

    client=boto3.client('rekognition')

    response=client.delete_faces(CollectionId=collection_id,
                               FaceIds=faces)
    
    print(str(len(response['DeletedFaces'])) + ' faces deleted:') 							
    for faceId in response['DeletedFaces']:
         print (faceId)
    return len(response['DeletedFaces'])

def main():

    collection_id='Collection'
    faces=['0b413b5a-50dd-49a3-bea9-6cdda5446135', '9628194b-8333-42d2-ab41-203fa9943941',
    '49acb963-8a92-483e-97ba-575570225d28', 'b3927e49-b003-4b32-a42a-60de491bdf7f', 'be88f40c-dd5f-42e7-b522-43659a5da2dd', 'bf945150-155e-42f0-aae3-d803f28d1bf9']

    faces_count=delete_faces_from_collection(collection_id, faces)
    print("deleted faces count: " + str(faces_count))

if __name__ == "__main__":
    main()
