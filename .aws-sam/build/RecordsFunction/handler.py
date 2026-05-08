import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
records_table = dynamodb.Table(os.environ['RECORDS_TABLE_NAME'])

CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET,DELETE,OPTIONS'
}

def handler(event, context):
    print(json.dumps(event))
    method = event['httpMethod']

    if method == 'OPTIONS':
        return {'statusCode': 200, 'body': '', 'headers': CORS}

    if method == 'GET':
        response = records_table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps({'records': response.get('Items', [])}),
            'headers': {'Content-Type': 'application/json', **CORS}
        }

    elif method == 'DELETE':
        record_id = event['pathParameters']['id']
        records_table.delete_item(Key={'recordId': record_id})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'{record_id} deleted'}),
            'headers': {'Content-Type': 'application/json', **CORS}
        }

    return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method not allowed'}),
        'headers': {'Content-Type': 'application/json', **CORS}
    }
