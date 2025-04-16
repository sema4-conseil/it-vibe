import json
import uuid
import boto3
import os
from is_user_in_group import is_user_in_group


def lambda_handler(event, context):

      # Check if the user is in the "admin" group
    if not is_user_in_group(event, "admin"):
        return {
            "statusCode": 403,
            "body": json.dumps({
                "errorMessage": "User is not authorized, only admin can execute this action"
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }
        }

    # Parse the JSON from the body field
    companyData = json.loads(event['body'])
    try:
        # Extracting data from the event
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['COMPANIES_TABLE_NAME']) # Get table name from environment variable 

        # Check if 'id' exists and is not null; if null or missing, generate a new UUID
        if "id" not in companyData or companyData["id"] is None:
            id = str(uuid.uuid4())
            companyData["id"] = id
            httpStatusCode = 201
        else:
            httpStatusCode = 200

        result = table.put_item(Item=companyData)
        
        return {
            "statusCode": httpStatusCode,
            "body": json.dumps(companyData),
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