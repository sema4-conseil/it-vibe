import json
import boto3
import os
from datetime import datetime, timezone
from is_user_in_group import is_user_in_group
from get_user_informations import get_user_informations

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['COMPANIES_TABLE_NAME']) # Get table name from environment variable

# get current datetime in UTC
dt = datetime.now(timezone.utc)


# DELETE /companies/{id}
# This lambda function is used to delete company by id.
def lambda_handler(event, context):
    try:
        # get company from table by id
        company_id = event['pathParameters']['id']

        # Check if companyId exists
        if(not company_id):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Company id is required"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                }
        }

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
        response = table.get_item(Key={'id': company_id})
        item = response.get('Item', None)   
        if item:
            # Get the user id from lambda context
            user_id, email, groups = get_user_informations(event)
            if user_id is None:
                return {
                    "statusCode": 401,
                    "body": json.dumps({"error": "User information is required"}),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    }
                }
            # Delete the item ligically, add field isDeleted to true, deletedAt to current time, deleteBy get the user sid from the lambda context
            table.update_item(
                    Key={'id': company_id},
                    UpdateExpression="SET isDeleted = :isDeleted, deleteDatetime = :deleteDatetime, deletedBy = :deletedBy",
                    ExpressionAttributeValues={
                        ':isDeleted': True,
                        ':deleteDatetime': dt.isoformat(),
                        ':deletedBy': user_id
                    }
            )
            # Return 200 OK response
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Company deleted successfully"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                } 
            }
        else:
            # If the item does not exist, return a 404 error
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Company not found"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                }
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        }