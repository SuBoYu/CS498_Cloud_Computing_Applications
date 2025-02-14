import boto3

# Set the region whre DynamoDB is located
DYNAMODB_REGION = 'us-east-2'

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name=DYNAMODB_REGION)
table = dynamodb.Table('GraphDistance')

def get_distance(source, destination):
    if source == destination:
        return 0

    response = table.get_item(Key={'source': source, 'destination': destination})
    return response.get('Item', {}).get('distance', -1)

def lambda_handler(event, context):
    try:
        intent_name = event['sessionState']['intent']['name']

        slots = event['sessionState']['intent']['slots']
        source = slots['source']['value']['interpretedValue']
        destination = slots['destination']['value']['interpretedValue']

        distance = get_distance(source, destination)

        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent_name,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": f"{distance}"
                }
            ]
        }
        return response

    except Exception as e:
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent_name,
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "An error occurred."
                }
            ]
        }
