import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
import os
from message_status import MessageStatus
from decimal import Decimal

from is_user_in_group import is_user_in_group


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CONTACT_MESSAGE_TABLE_NAME')
if not table_name:
    raise ValueError("Environment variable 'CONTACT_MESSAGE_TABLE_NAME' is not set.")
table = dynamodb.Table(table_name)

# Constants
DEFAULT_RESPONSE_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}

# Helper function to convert Decimals to int/float
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError



def lambda_handler(event, context):
    """
    Lambda function to get contact messages from DynamoDB.
    result should be ordered by creation date ascending and status ascending.
    result should be paginated with a limit of 10 items per page.
    """
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
    try:
        startKey = None
        pageSize = 5
        status= None

        #Exctract query parameters startKey and pageSize 
        if event and event.get('queryStringParameters'):
            query_params = event['queryStringParameters']
            startKey = query_params.get('startKey')
            pageSize = int(query_params.get('pageSize', 5))
            status = query_params.get('status')

            # Validate pageSize
        if not isinstance(pageSize, int) or pageSize <= 0:
            raise ValueError("pageSize must be a positive integer.")
            
            # Validate status 
        if status and status not in ["NEW", "IN_PROGRESS", "DONE", "ARCHIVED"]:
            raise ValueError("Invalid status value. Allowed values are: NEW, IN_PROGRESS, DONE and ARCHIVED.")
            
        query_params = {
            'Limit': pageSize
        }

        if startKey:
            try:
                query_params['ExclusiveStartKey'] = json.loads(startKey)
            except json.JSONDecodeError:
                raise ValueError("Invalid format for startKey.")
                
        # Create query kwargs
        query_params["IndexName"] = "StatusTimestampIndex"
        query_params["ScanIndexForward"] = True
            
        # if status is present scan with filter expression
        key_condition = Key('status')
        if status:
            key_condition = key_condition.eq(MessageStatus[status].value)
        else:
            # if status is not present, return only NEW messages for performance.
            key_condition =  key_condition.eq(MessageStatus.NEW.value)

        query_params['KeyConditionExpression'] = key_condition
        response = table.query(**query_params)
        items = response.get('Items', [])
        serializable_items = json.loads(json.dumps(items, default=decimal_default))

        # Convert LastEvaluatedKey if it exists
        last_evaluated_key = response.get('LastEvaluatedKey')
        if last_evaluated_key:
            last_evaluated_key = json.loads(json.dumps(last_evaluated_key, default=decimal_default))

        return {
            'statusCode': 200,
            'body': json.dumps({
                'items': serializable_items,
                'lastEvaluatedKey': last_evaluated_key
            }),
            'headers': DEFAULT_RESPONSE_HEADERS
        }
        
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return {
            "statusCode": 400,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({"error": str(ve)}),
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({"error": "An internal server error occurred."}),
        }
