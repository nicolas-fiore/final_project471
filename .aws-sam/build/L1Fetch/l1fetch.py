import json, os, boto3

s3 = boto3.client('s3')

def handler(event, context):
    job_id = event['job_id']
    filename = event['filename']
    bucket = os.environ['BUCKET']

    s3.get_object(Bucket=bucket, Key=filename)


    print(json.dumps(event))

    return {
        'job_id': job_id,
        'filename': filename,
        'bucket': bucket
    }