import json, boto3, os

dynamodb = boto3.resource('dynamodb')
rds = boto3.client('rds-data')


def handler(event, context):
    job_id = event['job_id']
    items = event['items']
    db_arn = os.environ['DB_ARN']
    secret_arn = os.environ['DB_SECRET']
    database = os.environ['DB_NAME']

    for item in items:
        rds.execute_statement(
            resourceArn=db_arn,
            secretArn=secret_arn,
            database=database,
            sql='INSERT INTO shopping_list (job_id, item) VALUES (:job_id, :item)',
            parameters=[
                {'name': 'job_id', 'value': {'stringValue': job_id}},
                {'name': 'item', 'value': {'stringValue': item}}
            ]
        )

    dynamodb.Table(os.environ['JOB_TABLE']).update_item(
        Key={'job_id': job_id},
        UpdateExpression='SET #s = :s, #m = :m',
        ExpressionAttributeNames={'#s': 'status', '#m': 'message'},
        ExpressionAttributeValues={
            ':s': 'SUCCEEDED',
            ':m': f'Saved {len(items)} items to table'}
    )
    
    
    print(json.dumps(event))

    return {
        'job_id': job_id,
        'items_saved': len(items)
    }