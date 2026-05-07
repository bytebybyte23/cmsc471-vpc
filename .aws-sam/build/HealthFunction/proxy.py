import boto3
import os
s3 = boto3.client('s3')
import json
def proxy_handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))
    bucket = os.environ['MYBUCKET_BUCKET_NAME']
    response = s3.get_object(Bucket = bucket, Key = 'index.html')
    htmlk_body = response['Body'].read().decode('utf-8')

    return {
        'statusCode': 200,
        'body': htmlk_body,
        'headers': {   
             'Content-Type': 'text/html'
        },
        
     }