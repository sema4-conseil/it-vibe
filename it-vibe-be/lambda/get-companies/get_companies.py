import json
import boto3
import os


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['COMPANIES_TABLE_NAME']) # Get table name from environment variable



def lambda_handler(event, context):
    try:
        startKey = None
        pageSize = 5  # Default page size

        if event and 'queryStringParameters' in event and event['queryStringParameters']: # check if event exist and if query string parameters exist
            startKey = event['queryStringParameters'].get('startKey')
            pageSize = int(event['queryStringParameters'].get('pageSize', 5))

        query_kwargs = {
            'Limit': pageSize
        }

        # If start key is there, add it to query kwargs. 
        if startKey:
            query_kwargs['ExclusiveStartKey'] = json.loads(startKey)

       
        result = table.scan(**query_kwargs) # Scan the entire table. For large tables, use pagination.
        items = result.get('Items', [])

        response = {
            "items": items,
            "LastEvaluatedKey": result.get('LastEvaluatedKey', None),
            "ScannedCount":  result.get('ScannedCount', None),
            "Count":  result.get('Count', None)
        }

        return {
            "statusCode": 200,
            "body": json.dumps(response),
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