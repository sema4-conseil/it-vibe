import json
import uuid
import boto3
import os
import logging
from is_user_in_group import is_user_in_group
from get_user_informations import get_user_informations

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DEFAULT_RESPONSE_HEADERS = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }

    
DYNAMO_DB_TABLE_NAME = os.environ['COMPANIES_TABLE_NAME']

if not DYNAMO_DB_TABLE_NAME:
    logger.error("Environment variable 'COMPANIES_TABLE_NAME' is not set")
    raise ValueError("Environment variable 'COMPANIES_TABLE_NAME' is not set")

def validate_company_data(companyData):
    """
    Validate the company data to ensure all mandatory fields are present.
    """
    mandatory_fields = ["name", "siren", "siret", "adress", "country", "industry","creationDate"]
    for field in mandatory_fields:
        if field not in companyData or companyData[field] is None:
            raise ValueError(f"Missing mandatory field: {field}")

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

        # Get user details from lambda context
        user_id, email, groups, username = get_user_informations(event)
        actor = {
            "user_id": user_id,
            "email": email,
            "username": username,
        }

        # Parse the JSON from the body field
        companyData = json.loads(event['body'])

        # Validate the company data
        validate_company_data(companyData)

    
        # Fill "name_lowercase" field with the lowercase version of "name"
        companyData["name_lowercase"] = companyData["name"].lower()

        # if 'id' is in company data, raise value error, cannot update existing company
        if "id" in companyData:
            raise ValueError("Cannot update existing company, please use the update endpoint")
        
        id = str(uuid.uuid4())
        companyData["id"] = id
        companyData["createdBy"] = actor

            # Use put_item to create a new item
        table.put_item(Item=companyData)
        logger.info(f"Company data saved successfully: {companyData.get('id')}")

        responseBody = {
            "message": "Item saved successfully",
            "id": companyData["id"],
        }

        return {
            "statusCode": 201,
            "body": json.dumps(responseBody),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "errorMessage": f"Missing key: {str(e)}"
            }),
            "headers": DEFAULT_RESPONSE_HEADERS

        }
    except PermissionError as e:
        return {
            "statusCode": 403,
            "body": json.dumps({"error": str(e)}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An internal server error occurred."}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }