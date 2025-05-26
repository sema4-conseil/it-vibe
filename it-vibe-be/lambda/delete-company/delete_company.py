import json
import boto3
import os
import uuid
from datetime import datetime, timezone
from is_user_in_group import is_user_in_group
from get_user_informations import get_user_informations

from logging import getLogger

logger = getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO').upper())

dynamodb = boto3.resource('dynamodb')
tableName = os.environ.get('COMPANIES_TABLE_NAME')

if not tableName:
    logger.error("Environment variable 'COMPANIES_TABLE_NAME' is not set")
    raise ValueError("Environment variable 'COMPANIES_TABLE_NAME' is not set")

table = dynamodb.Table(tableName)  # Get table name from environment variable

# get current datetime in UTC
dt = datetime.now(timezone.utc)

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}


# DELETE /companies/{id}
# This lambda function is used to delete company by id.
def lambda_handler(event, context):
    try:
        # get company from table by id
        company_id = event['pathParameters']['id']

        # Check if companyId exists
        if not company_id:
            raise ValueError("Company ID is required")

        # Check if company_id is a valid UUID
        try:
            uuid.UUID(company_id, version=4)  # Validate that company_id is a valid
        except ValueError:
            raise ValueError("Invalid Company ID format, it should be a valid UUID")

        # Check if the user is in the "admin" group
        if not is_user_in_group(event, "admin"):
            raise PermissionError("User is not authorized, only admin can execute this action")

            # Get the user id from lambda context
        user_id, email, groups, username = get_user_informations(event)
        if not user_id:
            raise AuthenticationError("you should be authenticated to perform this action")

        response = table.get_item(Key={'id': company_id})
        item = response.get('Item', None)
        if not item:
            raise NotFoundError("Company not found")

        if item.get('deletedBy'):
            raise ValueError("Company already deleted")

        deletedBy = {
            "date_time": dt.isoformat(),
            "user_id": user_id,
            "email": email,
            "username": username
        }

        item['deletedBy'] = deletedBy

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Company deleted successfully"}),
            "headers": DEFAULT_HEADERS
        }

    except ValueError as ve:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(ve)}),
            "headers": DEFAULT_HEADERS
        }
    except PermissionError as pe:
        return {
            "statusCode": 403,
            "body": json.dumps({"error": str(pe)}),
            "headers": DEFAULT_HEADERS
        }
    except NotFoundError as nfe:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": str(nfe)}),
            "headers": DEFAULT_HEADERS
        }
    except AuthenticationError as ae:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": str(ae)}),
            "headers": DEFAULT_HEADERS
        }
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": DEFAULT_HEADERS
        }


class NotFoundError(Exception):
    """Custom exception for not found errors."""
    pass


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass
