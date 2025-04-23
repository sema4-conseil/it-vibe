import json
import uuid
import boto3
import os
import logging
from is_user_in_group import is_user_in_group
from get_user_informations import get_user_informations
from company_mapper import map


logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def lambda_handler(event, context):

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

    # Get user details from lambda context
    user_id, email, groups, username = get_user_informations(event)
    actor = {
        "user_id": user_id,
        "email": email,
        "username": username,
    }

    # Parse the JSON from the body field
    companyData = json.loads(event['body'])

    # Validate company data, mandatory fields are:
    # name, description, siren, siret, president, address, country, industry
    # Do the validation only if creation. 
    if "id" not in companyData or companyData["id"] is None:
        mandatory_fields = ["name", "description", "siren", "siret", "president", "adress", "country", "industry"]
        for field in mandatory_fields:
        # If field not in companyData or field is null
        # Return a 400 error with a message indicating the missing field
            if field not in companyData or companyData[field] is None:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "errorMessage": f"Missing mandatory field: {field}"
                }),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
                }
            }

    try:
        # Fill "name_lowercase" field with the lowercase version of "name" if it exists
        # This is useful for case-insensitive searches
        companyData["name_lowercase"] = companyData["name"].lower() if "name" in companyData else None

        # Extracting data from the event
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['COMPANIES_TABLE_NAME'])  # Get table name from environment variable

        # Check if 'id' exists and is not null; if null or missing, generate a new UUID
        if "id" not in companyData or companyData["id"] is None:
            id = str(uuid.uuid4())
            companyData["id"] = id
            companyData["createdBy"] = actor
            httpStatusCode = 201  # Created

            # Use put_item to create a new item
            table.put_item(Item=companyData)
        else:
            # If the item exists, update it
            companyData["updatedBy"] = actor
            httpStatusCode = 200  # Updated

            # Prepare update expression and attribute values
            update_expression = "SET "
            expression_attribute_values = {}
            expression_attribute_names = {}

            for key, value in companyData.items():
                if key != "id":  # Exclude the primary key from being updated
                    update_expression += f"#{key} = :{key}, "
                    expression_attribute_values[f":{key}"] = value
                    expression_attribute_names[f"#{key}"] = key

            # Remove trailing comma and space
            update_expression = update_expression.rstrip(", ")

            # Perform the update
            table.update_item(
                Key={"id": companyData["id"]},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names
            )

        responseBody = {
            "message": "Item saved successfully",
            "id": companyData["id"],
        }
        return {
            "statusCode": httpStatusCode,
            "body": json.dumps(responseBody),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }
        }

    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "errorMessage": f"Missing key: {str(e)}"
            })
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An internal server error occurred."}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        }