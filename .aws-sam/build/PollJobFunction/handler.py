import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['JOBS_TABLE_NAME'])

def handler(event, context):
    print(json.dumps(event))
    job_id = event['pathParameters']['jobId']

    response = table.get_item(Key={'jobId': job_id})
    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': f'Job {job_id} not found'}),
            'headers': {'Content-Type': 'application/json'}
        }

    return {
        'statusCode': 200,
        'body': json.dumps(item),
        'headers': {'Content-Type': 'application/json'}
    }
