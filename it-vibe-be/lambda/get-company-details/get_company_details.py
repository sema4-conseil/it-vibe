import json
import boto3
import os
from decimal import Decimal
import uuid
import logging


from logging import getLogger   
logger = getLogger()
logger.setLevel(logging.INFO)


# check if the environment variable COMPANIES_TABLE_NAME is set
if 'COMPANIES_TABLE_NAME' not in os.environ:
    raise ValueError("Environment variable 'COMPANIES_TABLE_NAME' is not set")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['COMPANIES_TABLE_NAME']) # Get table name from environment variable


DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
}


# GET /companies/{id}
# This lambda function is used to get company details by id.
# It takes company id as path parameter and returns company details if found.
def lambda_handler(event, context):
    try:
        # get company from table by id
        company_id = event['pathParameters']['id']

        if(not company_id):
            raise ValueError("Company id is required")
        if not isinstance(company_id, str):
            raise ValueError("Company id must be a string")
        # Validate that the company_id is a valid UUID
        try:
            uuid.UUID(company_id)
        except ValueError:
            raise ValueError("Company id must be a valid UUID")
        


        response = table.get_item(Key={'id': company_id})
        item = response.get('Item', None)   

        if not item:
            raise NotFoundError(f"Company with id {company_id} not found")

        response = json.loads(json.dumps(item, default=lambda x: float(x) if isinstance(x, Decimal) else x))

        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": DEFAULT_HEADERS
        }

    except NotFoundError as nfe:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": str(nfe)}),
            "headers": DEFAULT_HEADERS
        }
    except ValueError as ve:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(ve)}),
            "headers": DEFAULT_HEADERS
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": DEFAULT_HEADERS
        }

class NotFoundError(Exception):
    """Custom exception for not found errors."""
    pass