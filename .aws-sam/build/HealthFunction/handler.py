import json
from datetime import datetime

def handler(event, context):
    print(json.dumps(event))

    return {
        'statusCode': 200,
        'body': json.dumps({
            'status': 'healthy',
            'date': datetime.utcnow().strftime('%Y-%m-%d'),
            'time': datetime.utcnow().strftime('%H:%M:%S')
        }),
        'headers': {
            'Content-Type': 'application/json'
        },
    }
