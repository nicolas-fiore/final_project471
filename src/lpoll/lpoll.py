import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')



def handler(event, context):
    # GET /api/jobs/abc-123
    job_id = event['pathParameters']['jobId']

    result = dynamodb.Table( os.environ['JOB_TABLE']).get_item(
        Key={ 'jobId': job_id }
    )

    item = result.get('Item', {})


    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin': '*' },      
        'body': json.dumps({
            'jobId': job_id,
            'status': item.get('status', 'UNKNOWN'),
            'message': item.get('message', '...')
        })
    }