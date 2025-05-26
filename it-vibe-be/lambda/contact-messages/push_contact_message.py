import json
import uuid
import logging
import boto3
import os
import re
from datetime import datetime, timezone
from message_status import MessageStatus

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO').upper())

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

MAX_CONTENT_LENGTH = 1000
EMAIL_REGEX = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'

def validate_email(email: str) -> bool:
    """Validate email format using basic regex."""
    return bool(re.match(EMAIL_REGEX, email))

def validate_contact_message_data(message_data: dict) -> dict or None:
    """
    Validate contact message data.
    Returns error response if validation fails, otherwise None.
    """
    if not message_data.get("email", "").strip():
        return {
            "statusCode": 400,
            "body": json.dumps({"errorMessage": "Email is required and cannot be empty"}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    
    if not validate_email(message_data["email"].strip()):
        return {
            "statusCode": 400,
            "body": json.dumps({"errorMessage": "Invalid email format"}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    
    content = message_data.get("content", "").strip()
    if not content:
        return {
            "statusCode": 400,
            "body": json.dumps({"errorMessage": "Message content is required and cannot be empty"}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    
    if len(content) > MAX_CONTENT_LENGTH:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "errorMessage": f"Message content too long. Maximum {MAX_CONTENT_LENGTH} characters allowed"
            }),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    
    return None

def lambda_handler(event, context):
    """Handle incoming contact messages and store them in DynamoDB."""
    try:
        # Parse and validate request
        if not event.get('body'):
            return {
                "statusCode": 400,
                "body": json.dumps({"errorMessage": "Request body is missing"}),
                "headers": DEFAULT_RESPONSE_HEADERS
            }

        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"errorMessage": "Invalid JSON format"}),
                "headers": DEFAULT_RESPONSE_HEADERS
            }

        # Validate the contact message data
        validation_error = validate_contact_message_data(body)
        if validation_error:
            return validation_error

        # Prepare and store the message
        message_data = {
            "id": str(uuid.uuid4()),
            "email": body["email"].strip(),
            "content": body["content"].strip(),
            "timestamp": int(datetime.now(timezone.utc).timestamp()),
            "status": MessageStatus.NEW.value,
        }

        table.put_item(Item=message_data)

        # Return success response
        response_body = {
            "message": "Contact message sent successfully",
            "id": message_data["id"],
        }
        
        return {
            "statusCode": 201,
            "body": json.dumps(response_body),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
        
    except KeyError as e:
        logger.error(f"Missing key in request: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"errorMessage": f"Missing required field: {str(e)}"}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    except Exception as e:
        logger.error(f"Error processing contact message: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"errorMessage": "An internal server error occurred."}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }