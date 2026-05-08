import boto3
import os
import json
import base64

s3 = boto3.client('s3')
bucket = os.environ['INBOX_BUCKET_NAME']

CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS'
}

def handler(event, context):
    print(json.dumps(event))
    method = event['httpMethod']

    if method == 'OPTIONS':
        return {'statusCode': 200, 'body': '', 'headers': CORS}

    if method == 'GET':
        response = s3.list_objects_v2(Bucket=bucket)
        items = [obj['Key'] for obj in response.get('Contents', [])]
        return {
            'statusCode': 200,
            'body': json.dumps({'items': items}),
            'headers': {'Content-Type': 'application/json', **CORS}
        }

    elif method == 'POST':
        params = event.get('queryStringParameters') or {}
        key = params.get('key', 'upload')
        is_base64 = event.get('isBase64Encoded', False)
        body = event.get('body', '') or ''
        content = base64.b64decode(body) if is_base64 else body.encode('utf-8')
        headers = event.get('headers') or {}
        content_type = headers.get('Content-Type', headers.get('content-type', 'application/octet-stream'))
        s3.put_object(Bucket=bucket, Key=key, Body=content, ContentType=content_type)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': f'{key} uploaded successfully'}),
            'headers': {'Content-Type': 'application/json', **CORS}
        }

    elif method == 'DELETE':
        key = event['pathParameters']['key']
        s3.delete_object(Bucket=bucket, Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'{key} deleted'}),
            'headers': {'Content-Type': 'application/json', **CORS}
        }

    return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method not allowed'}),
        'headers': {'Content-Type': 'application/json', **CORS}
    }
