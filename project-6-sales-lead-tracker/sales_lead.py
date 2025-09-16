import json
import boto3
import os
import uuid
import urllib.parse
import base64

# DynamoDB & SNS
dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("LEADS_TABLE")
table = dynamodb.Table(table_name)

sns = boto3.client("sns")
sns_topic_arn = os.environ.get("SNS_TOPIC_ARN")

def lambda_handler(event, context):
    try:
        # Get body
        body = event.get("body", "{}")
        if event.get("isBase64Encoded", False):
            body = base64.b64decode(body).decode("utf-8")

        # Try JSON first
        try:
            data = json.loads(body)
            name = data.get("name")
            email = data.get("email")
            company = data.get("company")
        except Exception:
            # If JSON fails, parse as form data
            parsed = urllib.parse.parse_qs(body)
            name = parsed.get("name", [""])[0]
            email = parsed.get("email", [""])[0]
            company = parsed.get("company", [""])[0]

        # Generate unique lead ID
        lead_id = str(uuid.uuid4())

        # Store in DynamoDB
        table.put_item(
            Item={
                "lead_id": lead_id,
                "name": name,
                "email": email,
                "company": company
            }
        )

        # Send SNS notification if configured
        if sns_topic_arn:
            message = f"New lead received:\nName: {name}\nEmail: {email}\nCompany: {company}"
            sns.publish(
                TopicArn=sns_topic_arn,
                Message=message,
                Subject="New Lead Notification"
            )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Lead stored successfully",
                "lead_id": lead_id
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
