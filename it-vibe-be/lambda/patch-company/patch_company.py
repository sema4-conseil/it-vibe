import json
import boto3
import os
import logging
import time
from datetime import datetime, timezone
from is_user_in_group import is_user_in_group
from get_user_informations import get_user_informations

logger = logging.getLogger()
logger.setLevel(logging.INFO)


UPDATABLE_FIELDS = ["name", "siren", "siret", "adress", "country", "industry","creationDate","size","revenue"]

DEFAULT_RESPONSE_HEADERS = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }

    
DYNAMO_DB_TABLE_NAME = os.environ['COMPANIES_TABLE_NAME']

if not DYNAMO_DB_TABLE_NAME:
    logger.error("Environment variable 'COMPANIES_TABLE_NAME' is not set")
    raise ValueError("Environment variable 'COMPANIES_TABLE_NAME' is not set")

def validate_user_rights(event):
    """
    Validate if the user has the right to perform the action.
    """
    # Check if the user is in the "admin" group
    if not is_user_in_group(event, "admin"):
        raise PermissionError("User is not authorized, only admin can execute this action")
    


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMO_DB_TABLE_NAME)  # Get table name from environment variable


def lambda_handler(event, context):
    try:
        validate_user_rights(event)

        # Validate the event structure
        if not event.get("pathParameters") or not event.get("body"):
            raise ValueError("Invalid request format")
        
        # Check that the body is a valid JSON
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in request body")
        
                
        # Check that the body contains atleast one field to update
        if not any(field in body for field in UPDATABLE_FIELDS):
            raise ValueError("At least one field to update is required")
        
        # Validate the company_id
        company_id = event["pathParameters"].get("id")
        if not company_id:
            raise ValueError("Company ID is required")
        

        # Get user details from lambda context
        user_id, email, groups, username = get_user_informations(event)

        updateInfos = {
            "user_id": user_id,
            "email": email,
            "username": username,
            "dateTime": datetime.now(timezone.utc).isoformat(),# current dateTime
        }

        # Get the company from the database
        response = table.get_item(
            Key={
                'id': company_id
            }
        )
        company = response.get('Item')
        if not company:
            raise NotFoundError(f"Company with ID {company_id} not found")
        
        # Update the company with the new values
        for field in UPDATABLE_FIELDS:
            if field in body:
                company[field] = body[field]
                if (field == "name"):
                    # If the name is updated, also update the name_lowercase field
                    company["name_lowercase"] = body[field].lower()

                    
        company["updatedBy"] = updateInfos


        # Update the company in the database
        table.put_item(Item=company)
        logger.info(f"Company data updated successfully: {company.get('id')}")
        
        return {
            "statusCode": 200,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({
                "message": "Patch company called with success" , "id" : company_id  })
        }

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {
            "statusCode": 400,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({"error": str(e)})
        }
    
    except PermissionError as e:
        logger.error(f"Permission error: {e}")
        return {
            "statusCode": 403,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({"error": str(e)})
        }
    except NotFoundError as e:
        logger.error(f"Not found error: {e}")
        return {
            "statusCode": 404,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        logger.error(f"Error getting user details: {e}")
        return {
            "statusCode": 500,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({"error": "Internal server error"})
        }

class NotFoundError(Exception):
    """Custom exception for not found errors."""
    pass