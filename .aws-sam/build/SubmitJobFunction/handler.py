import boto3
import os
import json
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['JOBS_TABLE_NAME'])
sfn = boto3.client('stepfunctions')

def handler(event, context):
    print(json.dumps(event))
    job_id = str(uuid.uuid4())
    body = json.loads(event.get('body', '{}'))

    item = {
        'jobId': job_id,
        'status': 'PENDING',
        'input': body,
        'createdAt': datetime.utcnow().isoformat()
    }
    table.put_item(Item=item)

    sfn.start_execution(
        stateMachineArn=os.environ['STATE_MACHINE_ARN'],
        name=job_id,
        input=json.dumps({**body, 'jobId': job_id})
    )

    return {
        'statusCode': 201,
        'body': json.dumps({'jobId': job_id, 'status': 'PENDING'}),
        'headers': {'Content-Type': 'application/json'}
    }
