import boto3
import os
import json

s3 = boto3.client('s3')
bucket = os.environ['INBOX_BUCKET_NAME']

def handler(event, context):
    print(json.dumps(event))
    key = event.get('key')
    url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=300)
    return {'key': key, 'url': url}
