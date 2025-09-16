import json
import boto3
import base64
import urllib.parse

def lambda_handler(event, context):
bucket_name = os.environ.get("BUCKET_NAME", "default-bucket")
file_key = os.environ.get("FILE_KEY", "default.json")



    s3 = boto3.client('s3')

    try:
        print("Event received:", event)

        body = event.get('body', '')
        if event.get('isBase64Encoded', False):
            decoded_bytes = base64.b64decode(body)
            body = decoded_bytes.decode('utf-8')

        parsed = urllib.parse.parse_qs(body)
        question = parsed.get('Body', [''])[0].strip().lower()

        print("User question:", question)

        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)

        answer = "Sorry, I didn't understand the question."

        if any(keyword in question for keyword in ["service", "offer", "offering", "services"]):
            service_names = [s['name'] for s in data.get('services', [])]
            answer = f"We offer the following services: {', '.join(service_names)}"
        elif any(keyword in question for keyword in ["hour", "hours", "open", "opening", "time", "schedule"]):
            hours = data.get('business_hours', {})
            answer = "Our working hours are:\n" + "\n".join([f"{day}: {time}" for day, time in hours.items()])
        elif any(keyword in question for keyword in ["location", "address", "where", "located"]):
            answer = f"We are located at: {data.get('location', 'Location not available')}"
        elif "name" in question:
            answer = f"Our business name is: {data.get('business_name', 'Name not found')}"
        elif "contact" in question:
            contact = data.get('Contact', {})
            answer = f"You can reach us at {contact.get('phone', '')} or {contact.get('email', '')}"
        elif "cancel" in question:
            answer = data.get('cancellation_policy', 'No cancellation policy provided.')

        twiml_response = f"<?xml version='1.0' encoding='UTF-8'?><Response><Message>{answer}</Message></Response>"

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/xml'},
            'body': twiml_response
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/xml'},
            'body': "<?xml version='1.0' encoding='UTF-8'?><Response><Message>Something went wrong.</Message></Response>"
        }
