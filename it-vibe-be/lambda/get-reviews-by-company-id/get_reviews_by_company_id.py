# Lambda function to calculate average rating and review count.
import json
import os
from decimal import Decimal

import boto3
from review_mapper import map

from logging import getLogger

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

logger = getLogger("GET_REVIEWS_BY_COMPANY_ID_LAMBDA")
logger.setLevel(LOG_LEVEL)

dynamodb = boto3.resource('dynamodb')
tableName = os.environ.get('COMPANY_REVIEWS_TABLE_NAME')
if not tableName:
    raise ValueError("Environment variable 'COMPANY_REVIEWS_TABLE_NAME' is not set.")
table = dynamodb.Table(tableName)

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}


def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def lambda_handler(event, context):
    try:

            if not event or 'queryStringParameters' not in event:
                 raise ValueError("Invalid event structure: 'queryStringParameters' is missing")
            
            companyId = event['queryStringParameters'].get('companyId')

            if (not companyId):
                raise ValueError("Missing required query parameter: 'companyId'")
            
            response = table.query(
                KeyConditionExpression='company_id = :company_id',
                ExpressionAttributeValues={
                    ':company_id': companyId
                }
            )

            items = response['Items']
            if not items:
                return {
                    'statusCode': 200,
                    'body': json.dumps([]),
                    'headers': DEFAULT_HEADERS
                }

            serializable_items = json.loads(json.dumps(items, default=decimal_to_float))

            mapped_reviews = [map(item) for item in serializable_items]

            return {
                'statusCode': 200,
                'body': json.dumps(mapped_reviews),
                'headers': DEFAULT_HEADERS
            }
    except ValueError as ve:
            logger.error(f"ValueError: {str(ve)}")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": str(ve)}),
                "headers": DEFAULT_HEADERS
            }
    except KeyError as ke:
            logger.error(f"KeyError: Missing key {str(ke)} in the event or response")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Missing key: {str(ke)}"}),
                "headers": DEFAULT_HEADERS
            }
    except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Internal server error"}),
                "headers": DEFAULT_HEADERS
            }
