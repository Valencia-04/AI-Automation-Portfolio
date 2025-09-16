import json

def lambda_handler(event, context):
    body = json.loads(event['body'])

    name = body.get('name', 'there')
    business = body.get('business', 'your business')
    needs = body.get('needs', 'your needs')

    response_message = (
        f"Hi {name}, thanks for reaching out! We’re excited to help with your business: {business}.\n\n"
        f"We understand you need help with:\n\"{needs}\"\n\n"
        "Here’s your next step:\n"
        "- 📄 [Download our onboarding guide](URL)\n"
        "- 📞 Book a call with us at [your-calendar-link]\n"
        "- 💬 We’ll follow up within 24 hours!"
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'message': response_message})
    }
