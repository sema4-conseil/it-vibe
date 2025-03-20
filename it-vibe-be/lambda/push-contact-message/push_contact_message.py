import json
import uuid

def lambda_handler(event, context):
    # Parse the JSON from the body field
    # body = json.loads(event)
    try:
        body = json.loads(event['body'])
        # Extracting data from the event
        message_data = {
            "id": str(uuid.uuid4()),
            "email": body["email"],
            "content": body["message"]
        }

      
        # TODO: Save the message_data to a database
        # For this example, we'll just return the data as a
        # response
        
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Message pushed successfully, we will get back to you soon! on the email:" + body["email"]
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }

        }
        
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "errorMessage": f"Missing key: {str(e)}"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "errorMessage": str(e)
            })
        }