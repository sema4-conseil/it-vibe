import logging

import os
import json

import boto3
from boto3.dynamodb.conditions import Key

from message_status import MessageStatus
from is_user_in_group import is_user_in_group


logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

TRANSITIONS = {
    MessageStatus.NEW: [MessageStatus.IN_PROGRESS, MessageStatus.ARCHIVED],
    MessageStatus.IN_PROGRESS: [MessageStatus.DONE],
    MessageStatus.DONE: [MessageStatus.ARCHIVED],
    MessageStatus.ARCHIVED: [],
}

def validateTransition(from_status:MessageStatus, to_status:MessageStatus):
    """
    Validate if the transition from one status to another is allowed.
    """
    if to_status not in TRANSITIONS.get(from_status, []):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "errorMessage": f"Invalid status transition from {from_status.name} to {to_status.name}"
            }),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    return None

def lambda_handler(event, context):
    """
    Lambda function to update the status of a contact message.
    """
    logger.info("Received event: %s", event)
    
    try:
        # Check if the event is a valid API Gateway event
        if not event.get("pathParameters") or not event.get("body"):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "errorMessage": "Invalid request format"
                }),
                "headers": DEFAULT_RESPONSE_HEADERS
            }
        
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
    
        # Extract parameters from the event
        path_parameters = event.get("pathParameters", {})
        message_id = path_parameters.get("id")
    
        body = json.loads(event['body'])
        toStatus = body.get("status")
    
        # Validate the status
        if not toStatus:
            logger.error("Status is required")
            # Return a 400 response with an error message
            raise ValueError("Status is required")
        
        toStatus = MessageStatus.get_valid_status(toStatus)

        if not toStatus:
            logger.error(f"Invalid status name: {toStatus}")
            # Return a 400 response with an error message
            raise ValueError(f"Invalid status: {toStatus}")
        
        response = table.query(KeyConditionExpression=Key('id').eq(message_id))
        items = response.get('Items', [])
        message = None
        # If items exist, get the first one
        if items:
            # Assuming the first item is the one we want
            message = items[0]
        else:
            # If no items exist, return a 404 response
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "errorMessage": f"Message with ID {message_id} not found"
                }),
                "headers": DEFAULT_RESPONSE_HEADERS
            }
    
        validateTransitionResult = validateTransition(
            MessageStatus(message['status']),
            MessageStatus(toStatus)
        )
        if validateTransitionResult:
            return validateTransitionResult
        
        message['status'] = MessageStatus(toStatus).value
        table.put_item(Item=message)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Message status updated to '{toStatus.name}'",
            }),
            "headers": DEFAULT_RESPONSE_HEADERS
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
