import json
import uuid
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['COMPANY_REVIEWS_TABLE_NAME']) # Get table name from environment variable 
defaultResponseHeader = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }

def validateReviewData(reviewData):
        # If company_id is null or empty, return 400
        if "company_id" not in reviewData or not reviewData["company_id"]:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "errorMessage": "company_id is required"
                }),
                "headers": defaultResponseHeader
            }
        # If rating is null, empty, not a number, or not between 1 and 10, return 400
        if "rating" not in reviewData or not reviewData["rating"] or not (isinstance(reviewData["rating"], int) and 1 <= reviewData["rating"] <= 10):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "errorMessage": "rating is required and must be a number between 1 and 10"
                }),
                "headers": defaultResponseHeader
            }
        # If review is null or empty, return 400
        if "comment" not in reviewData or not reviewData["comment"]:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "errorMessage": "comment is required"
                }),
                "headers": defaultResponseHeader
            }
        # if author is null or empty, return 400
        if "author" not in reviewData or not reviewData["author"]:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "errorMessage": "author is required"
                }),
                "headers": defaultResponseHeader
            }
        return None

def lambda_handler(event, context):
    # Parse the JSON from the body field
    reviewData = json.loads(event['body'])
    try:

        # Validate the review data
        validationError = validateReviewData(reviewData)
        if validationError:
            return validationError
        
        id = str(uuid.uuid4())
        reviewData["review_id"] = id
        httpStatusCode = 201
        table.put_item(Item=reviewData)
        
        return {
            "statusCode": httpStatusCode,
            "body": json.dumps(reviewData),
            "headers": defaultResponseHeader
        }
        
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "errorMessage": f"Missing key: {str(e)}"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "errorMessage": str(e)
            })
        }