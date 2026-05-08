import boto3
import os
import json
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
jobs_table = dynamodb.Table(os.environ['JOBS_TABLE_NAME'])
records_table = dynamodb.Table(os.environ['RECORDS_TABLE_NAME'])

def handler(event, context):
    print(json.dumps(event))
    job_id = event.get('jobId')
    status = 'FAILED' if 'error' in event else 'COMPLETED'
    lines = event.get('textractResult', {}).get('lines', [])
    now = datetime.utcnow().isoformat()

    # Update job status in JobsTable
    jobs_table.update_item(
        Key={'jobId': job_id},
        UpdateExpression='SET #s = :s, results = :r, updatedAt = :u',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={':s': status, ':r': lines, ':u': now}
    )

    # Save completed result to RecordsTable
    if status == 'COMPLETED':
        records_table.put_item(Item={
            'recordId': str(uuid.uuid4()),
            'jobId': job_id,
            'status': status,
            'results': lines,
            'createdAt': now
        })

    return {'jobId': job_id, 'status': status}
