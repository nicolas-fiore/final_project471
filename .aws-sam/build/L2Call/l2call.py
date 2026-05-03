import json, boto3, os

textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    job_id = event['job_id']
    filename = event['filename']
    bucket = event['bucket']

    response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': filename
            }
        }
    )

    items = [
        block['Text']
        for block in response['Blocks']
        if block['BlockType'] == 'LINE'
    ]

    dynamodb.Table(os.environ['JOB_TABLE']).update_item(
        Key={'job_id': job_id},
        UpdateExpression='SET #s = :s, #m = :m',
        ExpressionAttributeNames={'#s': 'status', '#m': 'message'},
        ExpressionAttributeValues={
            ':s': 'PROCESSING',
            ':m': f'Textract found {len(items)} items'}
    )

    print(json.dumps(event))

    return {
        'job_id': job_id,
        'items': items  
    }