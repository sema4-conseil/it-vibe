# Lambda function to calculate average rating and review count.
import os
import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ['COMPANY_REVIEWS_TABLE_NAME']) 

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def lambda_handler(event, context):

 companyId = None
    
 if event and 'queryStringParameters' in event and event['queryStringParameters']: # check if event exist and if query string parameters exist
    companyId = event['queryStringParameters'].get('companyId')

    if(not companyId):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Company id is required"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        }
    

    response = table.query(
        KeyConditionExpression='company_id = :company_id',
        ExpressionAttributeValues={
            ':company_id': companyId
        }
    )

    items = response['Items']
    if not items:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Company not found or has no reviews'})
        }

    serializable_items = json.loads(json.dumps(items, default=decimal_to_float))
    return {
        'statusCode': 200,
        'body': json.dumps(serializable_items)
    }