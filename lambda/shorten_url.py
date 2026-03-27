import json
import os
import random
import string
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        original_url = body.get("url")

        if not original_url:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing 'url' in request body"})
            }

        short_id = generate_short_id()
        created_at = datetime.now(timezone.utc).isoformat()

        item = {
            "short_id": short_id,
            "original_url": original_url,
            "created_at": created_at,
            "click_count": 0
        }

        table.put_item(Item=item)

        base_url = os.environ.get("BASE_URL", "")

        response_body = {
            "short_id": short_id,
            "original_url": original_url,
            "short_url": f"{base_url}/{short_id}" if base_url else short_id
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response_body)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }