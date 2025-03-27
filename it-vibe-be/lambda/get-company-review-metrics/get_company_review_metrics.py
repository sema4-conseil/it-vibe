# Lambda function to calculate average rating and review count.
import os
import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ['COMPANY_REVIEWS_TABLE_NAME']) 

def lambda_handler(event, context):
    company_id = event['company_id']
    response = table.query(
        KeyConditionExpression='company_id = :company_id',
        ExpressionAttributeValues={
            ':company_id': company_id
        }
    )

    items = response['Items']
    if not items:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Company not found or has no reviews'})
        }

    total_rating = 0
    count = 0
    for item in items:
        total_rating += Decimal(item['rating'])
        count += 1

    average_rating = total_rating / count if count > 0 else 0

    return {
        'statusCode': 200,
        'body': json.dumps({
            'average_rating': average_rating,
            'review_count': count
        })
    }