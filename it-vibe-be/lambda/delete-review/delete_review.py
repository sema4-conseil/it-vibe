import os
import json
import uuid
import boto3
from datetime import datetime, timezone
from is_user_in_group import is_user_in_group
from get_user_informations import get_user_informations

from logging import getLogger

logger = getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO').upper())
logger.name = "DELETE_REVIEW"

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}

dynamodb = boto3.resource('dynamodb')
tableName = os.environ.get('COMPANY_REVIEWS_TABLE_NAME')

if not tableName:
    logger.error("Environment variable 'COMPANY_REVIEWS_TABLE_NAME' is not set")
    raise ValueError("Environment variable 'COMPANY_REVIEWS_TABLE_NAME' is not set")

table = dynamodb.Table(tableName)

# get current datetime in UTC
dt = datetime.now(timezone.utc)


def validate_uuid(uuid_string):
    """
    Validate that a string is a valid UUID.

    Args:
        uuid_string (str): The string to validate as UUID

    Returns:
        UUID: The parsed UUID object if valid

    Raises:
        ValueError: If the string is not a valid UUID
    """
    try:
        return uuid.UUID(uuid_string)
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"String '{uuid_string}' is not a valid UUID")


def lambda_handler(event, context):
    """
        Lambda function called in reviews/delete
        2 query parameters are mandatory: review_id and company id
    """
    try:
        logger.debug("start delete review")

        company_id = event['queryStringParameters'].get('company_id')
        review_id = event['queryStringParameters'].get('review_id')

        if not company_id:
            raise ValueError("Company ID is required")

        if not review_id:
            raise ValueError("Review ID is required")

        logger.debug(f"received review id: {review_id}, company id: {company_id}")

        validate_uuid(company_id)
        validate_uuid(review_id)

        item_key = {
            'company_id': company_id,
            'review_id': review_id
        }

        response = table.get_item(
            Key=item_key
        )

        if "Item" not in response:
            raise NotFoundError("Review not found")

        logger.debug("Found item in DB")

        review = response["Item"]

        user_id, email, groups, username = get_user_informations(event)

        is_user_review_owner = user_id == review["owner"]["user_id"]
        is_user_admin = is_user_in_group(event, "admin")

        if not (is_user_review_owner or is_user_admin):
            logger.debug(f"Authorization error : user \"{user_id}\" is not admin nor review owner")
            raise PermissionError("User not authorized to perform this action")

        logger.debug("User can delete the review")

        delete_response = table.delete_item(Key=item_key)

        if delete_response:
            logger.debug("DELETE IS OK")
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Review deleted successfully"}),
                "headers": DEFAULT_HEADERS
            }
        else:
            logger.error(f"Error in delete review operation with dynamoDB.")
            raise Exception("Internal server error")

    except NotFoundError as nfe:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": str(nfe)}),
            "headers": DEFAULT_HEADERS
        }
    except ValueError as ve:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": str(ve)}),
            "headers": DEFAULT_HEADERS
        }
    except PermissionError as pe:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": str(pe)}),
            "headers": DEFAULT_HEADERS
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"}),
            "headers": DEFAULT_HEADERS
        }


class NotFoundError(Exception):
    """Custom exception for not found errors."""
    pass
