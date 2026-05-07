import boto3
import os
import json

textract = boto3.client('textract')
bucket = os.environ['INBOX_BUCKET_NAME']

def handler(event, context):
    print(json.dumps(event))
    key = event.get('key')
    response = textract.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': key}}
    )
    blocks = [b['Text'] for b in response['Blocks'] if b['BlockType'] == 'LINE']
    return {'key': key, 'lines': blocks}
