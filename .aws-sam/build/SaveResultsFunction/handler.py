import boto3
import os
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['JOBS_TABLE_NAME'])

def handler(event, context):
    print(json.dumps(event))
    job_id = event.get('jobId')
    status = 'FAILED' if 'error' in event else 'COMPLETED'
    lines = event.get('textractResult', {}).get('lines', [])
    now = datetime.utcnow().isoformat()

    table.update_item(
        Key={'jobId': job_id},
        UpdateExpression='SET #s = :s, results = :r, updatedAt = :u',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':s': status, ':r': lines, ':u': now}
    )

    return {'jobId': job_id, 'status': status}
