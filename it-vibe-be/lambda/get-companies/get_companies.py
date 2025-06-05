import json
import boto3
import os
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO').upper())

DEFAULT_RESPONSE_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('COMPANIES_TABLE_NAME')
if not table_name:
    raise ValueError("Environment variable 'COMPANIES_TABLE_NAME' is not set.")
table = dynamodb.Table(table_name)

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def lambda_handler(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    name = query_params.get('name', '').lower()
    siren = query_params.get('siren', '')
    siret = query_params.get('siret', '')
    country = query_params.get('country', 'FR')
    pageSize = int(query_params.get('pageSize', 5))

    logger.debug(f"Received query parameters: {query_params}")

    try:
        if (siren or siret) and name:
            raise ValueError("Cannot filter by both 'name' and 'siren'/'siret'. Please choose one.")
        count_response = None
        if siren:
            query_args = {
                'TableName': table_name,
                'IndexName': "siren-index",
                'KeyConditionExpression': 'siren = :siren',
                'ExpressionAttributeValues': {
                    ':siren': siren
                },
            }

        elif siret:
            query_args = {
                'TableName': table_name,
                'IndexName': 'siret-index',
                'KeyConditionExpression': 'siret = :siret',
                'ExpressionAttributeValues': {
                    ':siret': siret
                },
            }


        else:

            startKey = query_params.get('startKey')

            # validate pageSize
            if pageSize < 1 or pageSize > 100:
                raise ValueError("pageSize must be between 1 and 100.")

            # validate startKey
            if startKey:
                try:
                    startKey = json.loads(startKey, parse_float=Decimal)
                except json.JSONDecodeError:
                    raise ValueError("Invalid startKey format. It should be a valid JSON string.")

            query_args = {
                'TableName': table_name,
                'IndexName': 'country-index',
                'KeyConditionExpression': 'country = :country',
                'ExpressionAttributeValues': {
                    ':country': country
                },
                'Limit': pageSize,
                'ScanIndexForward': True  # Sort ascending
            }
            if startKey:
                query_args['ExclusiveStartKey'] = startKey

            if name:
                query_args['KeyConditionExpression'] += ' and begins_with(name_lowercase, :name)'
                query_args['ExpressionAttributeValues'][':name'] = name

            count_args = {
                'TableName': query_args['TableName'],
                'IndexName': query_args['IndexName'],
                'KeyConditionExpression': query_args['KeyConditionExpression'],
                'ExpressionAttributeValues': query_args['ExpressionAttributeValues'],
                'Select': 'COUNT',
            }
            # We need to do the count only in search by name.
            logger.debug(f"Count args for dynamo db: {count_args}")
            count_response = table.query(**count_args)

        logger.debug(f"Query args for dynamo db: {query_args}")
        query_response = table.query(**query_args)

        result = {
            "items": query_response.get('Items', []),
            "pageSize": pageSize,
            "startKey": query_response.get('LastEvaluatedKey', None)
        }

        if count_response:
            result["count"] = count_response["Count"]
        else:
            result["count"] = query_response["Count"]

        return {
            "statusCode": 200,
            "body": json.dumps(result, default=decimal_to_float),
            "headers": DEFAULT_RESPONSE_HEADERS
        }

    except ValueError as ve:
        logger.debug(f"Validation error: {str(ve)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(ve)}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An internal server error occurred."}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
