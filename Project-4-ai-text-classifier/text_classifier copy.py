import json
import urllib.request
import os

HF_API_URL = "URL"

def call_hf(text, token):
    data = json.dumps({"inputs": text}).encode("utf-8")
    req = urllib.request.Request(
        HF_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)

def lambda_handler(event, context):
    # Try to get body as string
    body_str = event.get("body") or "{}"
    
    # If body is already dict, use it, else parse string
    if isinstance(body_str, str):
        try:
            body = json.loads(body_str)
        except:
            body = {}
    else:
        body = body_str

    # Now get 'text'
    text = body.get("text", "").strip()
    if not text:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No 'text' provided"})
        }

    token = os.environ.get("HF_TOKEN")
    if not token:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Missing HF_TOKEN"})
        }

    try:
        result = call_hf(text, token)
    except Exception as e:
        return {
            "statusCode": 502,
            "body": json.dumps({"error": "Failed to call Hugging Face", "details": str(e)})
        }

    return {
    "statusCode": 200,
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type"
    },
    "body": json.dumps({"input": text, "classification": result})
}

