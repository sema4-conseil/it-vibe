import json
import uuid

def lambda_handler(event, context):
    # Parse the JSON from the body field
    body = json.loads(event['body'])
    try:
        # Extracting data from the event
        company_data = {
            "id": str(uuid.uuid4()),
            "name": body["name"],
            "location": body["location"],
            "size": body.get("size", 0),
            "revenue": body.get("revenue", 0),
            "industry": body.get("industry", ""),
            "description": body.get("description", "")
        }

        print(event)
        
        # Here you would typically save the company_data to a database
        # For this example, we'll just return the data as a response
        
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Company created successfully",
                "company": company_data
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