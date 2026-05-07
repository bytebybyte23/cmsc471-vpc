import boto3
import os
import json
import base64

s3 = boto3.client('s3')
bucket = os.environ['INBOX_BUCKET_NAME']

def handler(event, context):
    print(json.dumps(event))
    method = event['httpMethod']

    if method == 'GET':
        response = s3.list_objects_v2(Bucket=bucket)
        items = [obj['Key'] for obj in response.get('Contents', [])]
        return {
            'statusCode': 200,
            'body': json.dumps({'items': items}),
            'headers': {'Content-Type': 'application/json'}
        }

    elif method == 'POST':
        key = event.get('queryStringParameters', {}).get('key', 'upload')
        is_base64 = event.get('isBase64Encoded', False)
        body = event.get('body', '')
        content = base64.b64decode(body) if is_base64 else body.encode('utf-8')
        content_type = event.get('headers', {}).get('Content-Type', 'application/octet-stream')
        s3.put_object(Bucket=bucket, Key=key, Body=content, ContentType=content_type)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': f'{key} uploaded successfully'}),
            'headers': {'Content-Type': 'application/json'}
        }

    elif method == 'DELETE':
        key = event['pathParameters']['key']
        s3.delete_object(Bucket=bucket, Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'{key} deleted'}),
            'headers': {'Content-Type': 'application/json'}
        }

    return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method not allowed'}),
        'headers': {'Content-Type': 'application/json'}
    }
