import json
import uuid
import boto3
import os
from get_user_informations import get_user_informations
from datetime import datetime, timezone

from logging import getLogger
logger = getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO').upper())

dynamodb = boto3.resource('dynamodb')
tableName = os.environ.get('COMPANY_REVIEWS_TABLE_NAME') 
if not tableName:
    logger.error("Environment variable 'COMPANY_REVIEWS_TABLE_NAME' is not set.")
    raise ValueError("Environment variable 'COMPANY_REVIEWS_TABLE_NAME' is not set.")

table = dynamodb.Table(tableName) # Get table name from environment variable 

DEFAULT_HEADERS = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }

CONTRACT_TYPES = ["CDI", "CDD", "INTERNSHIP", "CONTRACTOR", "FREELANCE", "OTHER"]

DATE_FORMAT = "%Y-%m-%d"

# get current datetime in UTC
dt = datetime.now(timezone.utc)

def validateReviewData(reviewData):
        if "company_id" not in reviewData or not reviewData["company_id"]:
            raise ValueError("company_id is required")
        
        if "rating" not in reviewData or not reviewData["rating"] or not (isinstance(reviewData["rating"], int) and 1 <= reviewData["rating"] <= 10):
            raise ValueError("rating must be an integer between 1 and 10")
        
        if "comment" not in reviewData or not reviewData["comment"]:
            raise ValueError("comment is required")
        
        if len(reviewData["comment"]) < 100 or len(reviewData["comment"]) > 1000:
            raise ValueError("comment must be between 100 and 1000 characters long")
        
        if "isAnonymous" not in reviewData or not isinstance(reviewData["isAnonymous"], bool):
            raise ValueError("isAnonymous must be a boolean value")
        
        if "contractType" not in reviewData or not reviewData["contractType"]:
            raise ValueError("contractType is required")
        
        if reviewData["contractType"] not in CONTRACT_TYPES:
            raise ValueError(f"contractType must be one of {', '.join(CONTRACT_TYPES)}")
        
        if "startDate" not in reviewData or not reviewData["startDate"]:
            raise ValueError("startDate is required")
        try:
            # Check if startDate is a valid date string
            datetime.strptime(reviewData["startDate"], DATE_FORMAT)
        except ValueError:
            raise ValueError("startDate must be in the format YYYY-MM-DD")
        
        # startDate should not be in the future
        if datetime.strptime(reviewData["startDate"], DATE_FORMAT) > datetime.now():
            raise ValueError("startDate cannot be in the future")
        
        if "endDate" in reviewData and reviewData["endDate"]:
            try:
                # Check if endDate is a valid date string
                datetime.strptime(reviewData["endDate"], DATE_FORMAT)
            except ValueError:
                raise ValueError("endDate must be in the format YYYY-MM-DD")
            
            # Check if endDate is after startDate
            if reviewData["endDate"] < reviewData["startDate"]:
                raise ValueError("endDate must be after startDate")
            
        

def lambda_handler(event, context):
    try:
        # Parse the request body
        if 'body' not in event or not event['body']:
            logger.error("Request body is missing or empty")
            raise ValueError("Request body is missing or empty")
        
        reviewData = json.loads(event['body'])
        # Validate the review data
        validateReviewData(reviewData)
        
        # Get userdetails from lambda context
        user_id, email, groups, username = get_user_informations(event)
        if not user_id or not email or not username:
            logger.error("User information is missing or incomplete")
            raise AuthenticationError("User information is missing or incomplete")
        
        reviewOwner = {
            "user_id": user_id,
            "email": email,
            "username": username,
        }

        reviewToSave = Review(
            company_id=reviewData["company_id"],
            rating=reviewData["rating"],
            comment=reviewData["comment"],
            isAnonymous=reviewData["isAnonymous"],
            contractType=reviewData["contractType"],
            startDate=reviewData["startDate"],
            endDate=reviewData.get("endDate"),
            creationDate=dt.isoformat(),
            owner=reviewOwner
        )

        table.put_item(Item=reviewToSave.to_dict())
        logger.debug(f"Review added successfully for company_id: {reviewData['company_id']} by user_id: {user_id}")
        
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Review added successfully",
                "id": reviewToSave.review_id,
            }),
            "headers": DEFAULT_HEADERS
        }
        
    except ValueError as ve:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(ve)}),
            "headers": DEFAULT_HEADERS
        }
    except AuthenticationError as e:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "user information is missing or incomplete"}),
            "headers": DEFAULT_HEADERS
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": DEFAULT_HEADERS
        }

class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


class Review:
    """Class representing a review."""
    def __init__(self, company_id, rating, comment, isAnonymous, contractType, startDate,owner ,creationDate, endDate=None):
        self.review_id = str(uuid.uuid4())
        self.creationDate = creationDate
        self.owner = owner
        self.company_id = company_id
        self.rating = rating
        self.comment = comment
        self.isAnonymous = isAnonymous
        self.contractType = contractType
        self.startDate = startDate
        self.endDate = endDate if endDate else None

    def to_dict(self):
        return {
            "review_id": self.review_id,
            "creationDate": self.creationDate,
            "owner": self.owner,
            "company_id": self.company_id,
            "rating": self.rating,
            "comment": self.comment,
            "isAnonymous": self.isAnonymous,
            "contractType": self.contractType,
            "startDate": self.startDate,
            "endDate": self.endDate
        }
    
