import json, boto3, os, uuid
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')



def handler(event, context):
    job_id = event['job_id']
    items = event['items']
    
    records_table = dynamodb.Table(os.environ['RECORDS_TABLE'])

    for item in items:
        records_table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'job_id': job_id,
                'item': item,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
        )    

    dynamodb.Table(os.environ['JOB_TABLE']).update_item(
        Key={'job_id': job_id},
        UpdateExpression='SET #s = :v1, #m = :v2',
        ExpressionAttributeNames={'#v1': 'status', '#v2': 'message'},
        ExpressionAttributeValues={
            ':s': 'SUCCEEDED',
            ':m': f'Saved {len(items)} items to table'}
    )
    
    
    print(json.dumps(event))

    return {
        'job_id': job_id,
        'items_saved': len(items)
    }