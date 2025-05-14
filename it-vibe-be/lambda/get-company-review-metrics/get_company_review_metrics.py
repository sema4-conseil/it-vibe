# Lambda function to calculate average rating and review count.
import os
import boto3
import json
from decimal import Decimal
import logging

dynamodb = boto3.resource('dynamodb')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


table_name = os.environ.get('COMPANY_REVIEWS_TABLE_NAME')
if not table_name:
    raise ValueError("Environment variable 'COMPANY_REVIEWS_TABLE_NAME' is not set.")
table = dynamodb.Table(table_name) 

DEFAULT_RESPONSE_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}

def lambda_handler(event, context):
    company_id = event['pathParameters']['id']
    
    if not company_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Company ID is required'}),
            'headers': DEFAULT_RESPONSE_HEADERS
        }
    # if company_id is not a valid UUID, return 400
    if not isinstance(company_id, str) or len(company_id) != 36:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid Company ID format'}),
            'headers': DEFAULT_RESPONSE_HEADERS
        }

    try:
        response = table.query(
            KeyConditionExpression='company_id = :company_id',
            ExpressionAttributeValues={
                ':company_id': company_id
            }
        )
    
        items = response['Items']
        if not items:
            return {
                'statusCode': 200,
                'body':  json.dumps({
                    'average_rating': float(0),
                    'review_count': int(0)
                }),
                'headers': DEFAULT_RESPONSE_HEADERS
            }
    
        total_rating = 0
        count = 0
        for item in items:
            total_rating += Decimal(item['rating'])
            count += 1
    
        average_rating = total_rating / count if count > 0 else 0

        # Convert Decimal to float for JSON serialization
        average_rating = float(average_rating)
        count = int(count)
        
        body = {
            'average_rating': average_rating,
            'review_count': count
        }

        return {
            'statusCode': 200,
            'body': json.dumps(body),
            'headers': DEFAULT_RESPONSE_HEADERS
        }
    except KeyError as e:
        logger.error(f"Missing key in request: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"errorMessage": f"Missing required field: {str(e)}"}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    except Exception as e:
        logger.error(f"Error fetching reviews for company {company_id}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }