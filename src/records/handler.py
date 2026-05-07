import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['JOBS_TABLE_NAME'])

def handler(event, context):
    print(json.dumps(event))
    method = event['httpMethod']

    if method == 'GET':
        response = table.scan(
            FilterExpression='#s = :completed',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':completed': 'COMPLETED'}
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'records': response.get('Items', [])}),
            'headers': {'Content-Type': 'application/json'}
        }

    elif method == 'DELETE':
        record_id = event['pathParameters']['id']
        table.delete_item(Key={'jobId': record_id})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'{record_id} deleted'}),
            'headers': {'Content-Type': 'application/json'}
        }

    return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method not allowed'}),
        'headers': {'Content-Type': 'application/json'}
    }
