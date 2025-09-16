import json
import boto3
import base64
import urllib.parse

# Default HR leave policies
DEFAULT_POLICIES = {
    "general_policy": "All leave requests must be approved by the manager. (Default placeholder)",
    "annual_leave": "Employees are entitled to 21 annual leave days per year.",
    "sick_leave": "Employees are entitled to 30 sick leave days per 3-year cycle. See HR for details.",
    "maternity_leave": "Maternity leave: 16 weeks (company policy).",
    "paternity_leave": "Paternity leave: 10 working days paid.",
    "study_leave": "Up to 10 days per year upon approval.",
    "unpaid_leave": "Unpaid leave: case-by-case approval.",
    "cancellation_policy": "If leave is cancelled with less than 24 hours notice, notify HR."
}

BUCKET_NAME = 'BUCKET-NAME'
FILE_KEY = 'fILE-NAME'

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    policies = DEFAULT_POLICIES.copy()
    
    try:
        print("Event received:", event)

        # Try to read policies from S3
        try:
            response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
            content = response['Body'].read().decode('utf-8')
            s3_data = json.loads(content)
            policies.update(s3_data)
            print("Loaded policies from S3:", s3_data)
        except Exception as e:
            print(f"S3 read failed ({str(e)}) — using default policies.")

        # Extract question
        body = event.get('body', '')
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body).decode('utf-8')
        
        # Try JSON first, then form-encoded
        try:
            parsed = json.loads(body) if body else {}
            question = parsed.get('question', '').strip().lower()
        except Exception:
            parsed_qs = urllib.parse.parse_qs(body)
            question = parsed_qs.get('question', [''])[0].strip().lower()
        
        print("Question extracted:", question)

        # Determine answer
        answer = "Sorry — I couldn't find a direct answer. Try: 'annual leave', 'sick leave', 'maternity'."
        if not question:
            answer = policies.get('general_policy')
        elif "sick" in question:
            answer = policies.get('sick_leave')
        elif "annual" in question or "vacation" in question:
            answer = policies.get('annual_leave')
        elif "maternity" in question:
            answer = policies.get('maternity_leave')
        elif "paternity" in question:
            answer = policies.get('paternity_leave')
        elif "study" in question:
            answer = policies.get('study_leave')
        elif "unpaid" in question:
            answer = policies.get('unpaid_leave')
        elif "cancel" in question or "cancellation" in question:
            answer = policies.get('cancellation_policy')
        elif "policy" in question or "leave" in question:
            answer = (policies.get('general_policy') + " Examples: " +
                      policies.get('annual_leave', '') + " | " +
                      policies.get('sick_leave', ''))

    except Exception as e:
        print("Unexpected error:", str(e))
        answer = "Something went wrong. Please contact HR."

    return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    },
    "body": json.dumps({"answer": answer})
}


