import json
import boto3
import random
import string

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("url-shortener-links")


def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def lambda_handler(event, context):
    http_method = event.get("requestContext", {}).get("http", {}).get("method")

    # POST: Create short URL
    if http_method == "POST":
        try:
            body = json.loads(event.get("body", "{}"))
            original_url = body.get("url")

            if original_url and not original_url.startswith(("http://", "https://")):
                original_url = "https://" + original_url

            if not original_url:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({"error": "Missing 'url' in request body"})
                }

            short_id = generate_short_id()

            domain = event.get("requestContext", {}).get("domainName")
            short_url = f"https://{domain}/{short_id}"

            table.put_item(
                Item={
                    "short_id": short_id,
                    "original_url": original_url
                }
            )

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "short_id": short_id,
                    "original_url": original_url,
                    "short_url": f"https://go.brandon-tucker.com/{short_id}"
                })
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": str(e)})
            }

    # GET: Redirect short URL
    elif http_method == "GET":
        try:
            short_id = event.get("pathParameters", {}).get("short_id")

            if not short_id:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({"error": "Missing short_id in path"})
                }

            response = table.get_item(Key={"short_id": short_id})
            item = response.get("Item")

            if not item:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({"error": "Short URL not found"})
                }

            original_url = item["original_url"]

            return {
                "statusCode": 302,
                "headers": {
                    "Location": original_url
                },
                "body": ""
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": str(e)})
            }

    else:
        return {
            "statusCode": 405,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Method not allowed"})
        }