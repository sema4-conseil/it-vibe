import json
import boto3
import os


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['COMPANIES_TABLE_NAME']) # Get table name from environment variable


# GET /companies/{id}
# This lambda function is used to get company details by id.
# It takes company id as path parameter and returns company details if found.
def lambda_handler(event, context):
    try:
        # get company from table by id
        company_id = event['pathParameters']['id']

        if(not company_id):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Company id is required"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                }
            }

        response = table.get_item(Key={'id': company_id})
        item = response.get('Item', None)   


        return {
            "statusCode": item and 200 or 404,  # Return 404 if item not found
            "body": item and json.dumps(item) or json.dumps({"error": "Company not found"}),
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