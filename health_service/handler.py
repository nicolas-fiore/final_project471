from datetime import datetime, timezone
import json
import os
def handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        "statusCode": 200, 
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }, 
        "body": json.dumps({
            "status": "ok",
            "service": "cmsc471-website",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "region": os.environ.get("AWS_REGION", "us-east-1")
        })
    }