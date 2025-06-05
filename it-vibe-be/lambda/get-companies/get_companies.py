import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
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
    
        query_args = {};

        if siren:
            query_args = {
                'TableName': table_name,
                'IndexName': 'siren-index',
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
        
        logger.debug(f"Query args for dynamo db: {query_args}")

        response = table.query(**query_args)

        result = {
                "items": response.get('Items', []),
                "count": response.get('Count', 0),
                "pageSize": pageSize,
                "startKey": response.get('LastEvaluatedKey', None)
        }

        return {
            "statusCode": 200,
            "body": json.dumps(result, default=decimal_to_float),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
            
    
    
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An internal server error occurred."}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    except ValueError as ve:
        logger.debug(f"Validation error: {str(ve)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(ve)}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }