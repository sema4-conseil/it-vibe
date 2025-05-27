from logging import getLogger
import os
import json
import base64
import uuid
import datetime
from datetime import datetime, timezone
import boto3


from is_user_in_group import is_user_in_group
from get_user_informations import get_user_informations


logger = getLogger(__name__)
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
}

MAX_ITEMS_TO_IMPORT = 10;

companiesTableName = os.environ.get("COMPANIES_TABLE_NAME", None)
if not companiesTableName:
    logger.error("COMPANIES_TABLE_NAME environment variable is not set.")
    raise ValueError("COMPANIES_TABLE_NAME environment variable is not set.")


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(companiesTableName)

def validateCompany(company):
    """
    Validates the company data structure.
    Raises ValueError if validation fails.
    """
    required_fields = ['name', 'size', 'country', 'industry', 'revenue', 'creationDate', 'adress', 'siren', 'siret']
    validation_errors = []

    for field in required_fields:
        if field not in company or company[field] is None:
            logger.debug(f"Missing required field: {field} in company {company.get('name', 'Unknown')}")
            validation_errors.append(f"Missing required field: {field}")
    
    if 'name' in company and not isinstance(company['name'], str):
        logger.debug(f"Invalid name: {company.get('name', 'Unknown')} in company {company.get('name', 'Unknown')}")
        validation_errors.append("Invalid name. It should be a string.")

    if 'creationDate' in company:
        try:
            creation_date = company['creationDate']
            if not isinstance(creation_date, str):
                raise ValueError("Creation date should be a string.")
            # Optionally, you can add more validation for date format here
        except ValueError as e:
            logger.debug(f"Invalid creation date: {company.get('creationDate', 'Unknown')} in company {company.get('name', 'Unknown')}")
            validation_errors.append(f"Invalid creation date: {e}")
    
    if 'adress' in company and not isinstance(company['adress'], str):
        logger.debug(f"Invalid address: {company.get('adress', 'Unknown')} in company {company.get('name', 'Unknown')}")
        validation_errors.append("Invalid address. It should be a string.")


    if len(company.get('country', '')) != 2:
        logger.debug(f"Invalid country code: {company.get('country', 'Unknown')} in company {company.get('name', 'Unknown')}")
        validation_errors.append("Invalid country code. It should be a 2-letter ISO code.")
    
    if len(company.get('siren', '')) != 9:
        logger.debug(f"Invalid SIREN number: {company.get('siren', 'Unknown')} in company {company.get('name', 'Unknown')}")
        validation_errors.append("Invalid SIREN number. It should be 9 digits long.")

    if len(company.get('siret', '')) != 14:
        logger.debug(f"Invalid SIRET number: {company.get('siret', 'Unknown')} in company {company.get('name', 'Unknown')}")
        validation_errors.append("Invalid SIRET number. It should be 14 digits long.")
    
    if not isinstance(company.get('size'), int) or company['size'] < 0:
        logger.debug(f"Invalid size: {company.get('size', 'Unknown')} in company {company.get('name', 'Unknown')}")
        validation_errors.append("Invalid size. It should be a non-negative integer.")

    if not isinstance(company.get('revenue'), (int, float)) or company['revenue'] < 0:
        logger.debug(f"Invalid revenue: {company.get('revenue', 'Unknown')} in company {company.get('name', 'Unknown')}")
        validation_errors.append("Invalid revenue. It should be a non-negative number.")



    return validation_errors if validation_errors else None


def validate_user_rights(event):
    """
    Validate if the user has the right to perform the action.
    """
    # Check if the user is in the "admin" group
    if not is_user_in_group(event, "admin"):
        logger.debug("User is not authorized, only admin can execute this action")
        raise PermissionError("User is not authorized, only admin can execute this action")
    
def lambda_handler(event, context):
    """
    Lambda function to import companies from a file.
    """
    logger.debug("Starting import_companies_from_file")

    try:
        validate_user_rights(event)

        content_type = event.get('headers', {}).get('content-type', '')
        if 'multipart/form-data' not in content_type:
            logger.debug("Invalid content type. Expected multipart/form-data.")
            raise ValueError("Invalid content type. Expected multipart/form-data.")

        body = event.get('body', '')
        if not body:
            logger.debug("No body found in the event.")
            raise ValueError("No body found in the event.")

        body = event.get('body', '')

        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body).decode('utf-8')

        boundary = content_type.split('boundary=')[1]
        parts = body.split('--' + boundary)
        file_content = None
        for part in parts:
            if 'filename="' in part:
                file_content = part.split('\r\n\r\n')[1].rstrip('\r\n--')
                break

        if not file_content:
            logger.debug("No file content found in the multipart data.")
            raise ValueError("No file content found in the multipart data.")

        try:
            data = json.loads(file_content)
        except json.JSONDecodeError as e:
            logger.debug(f"JSON decode error: {e}")
            raise ValueError("Invalid JSON format in the file content.")

        if "companies" not in data or not isinstance(data["companies"], list):
            logger.debug("Invalid data format. Expected a list of companies.")
            raise ValueError("Invalid data format. Expected a list of companies.")
        companies = data["companies"]

        if not companies:
            logger.debug("No companies found in the data.")
            raise ValueError("No companies found in the data.")
        
        if len(companies) > MAX_ITEMS_TO_IMPORT:
            error = f"Too many companies to import: {len(companies)}. Maximum is {MAX_ITEMS_TO_IMPORT}."
            logger.debug(error)
            raise ValueError(error)
        

        validation_errors = {}

        for company in companies:
            errors = validateCompany(company)
            if errors is not None:
                validation_errors[company.get('name', 'Unknown')] = errors

        if validation_errors:
            logger.debug(f"Validation errors found: {validation_errors}")
            return {
                "statusCode": 400,
                "headers": DEFAULT_HEADERS,
                "body": json.dumps({"error": "Validation errors found", "details": validation_errors}),
            }
        
        # Get user details from lambda context
        user_id, email, groups, username = get_user_informations(event)
        createdByInfos = {
            "user_id": user_id,
            "email": email,
            "username": username,
            "dateTime": datetime.now(timezone.utc).isoformat(),
        }
        entities = []
        for company in companies:
            entity = CompanyEntiy(
                name=company['name'],
                size=company['size'],
                country=company['country'],
                industry=company['industry'],
                revenue=company['revenue'],
                creationDate=company['creationDate'],
                adress=company['adress'],
                siren=company['siren'],
                siret=company['siret'],
                createdBy=createdByInfos
            )
            entities.append(entity.to_dict())
        
        # save companies to DynamoDB
        with table.batch_writer() as batch:
            for entity in entities:
                batch.put_item(Item=entity)
                
        logger.debug(f"Successfully imported {len(companies)} companies.")

        return {
            'statusCode': 201,
            'headers': DEFAULT_HEADERS,
            'body': json.dumps({
                'message': f'Successfully imported {len(companies)} companies.',
            })
        }

    except PermissionError as pe:
        logger.error(f"PermissionError: {pe}")
        return {
            "statusCode": 403,
            "headers": DEFAULT_HEADERS,
            "body": json.dumps({"error": str(pe)}),
        }
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return {
            "statusCode": 400,
            "headers": DEFAULT_HEADERS,
            "body": json.dumps({"error": str(ve)}),
        }
    except Exception as e:
        logger.error(f"Unexpected error accured: {e}")
        return {
            'statusCode': 500,
            'body': 'An unexpected error.',
            'headers': DEFAULT_HEADERS,
        }

class CompanyEntiy :
    def __init__(self, name, size, country, industry, revenue, creationDate, adress, siren, siret, createdBy):
        self.name = name
        self.size = size
        self.country = country
        self.industry = industry
        self.revenue = revenue
        self.creationDate = creationDate
        self.adress = adress
        self.siren = siren
        self.siret = siret
        self.id = str(uuid.uuid4())
        self.createdBy = createdBy

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_lowercase': self.name.lower(),
            'size': self.size,
            'country': self.country,
            'industry': self.industry,
            'revenue': self.revenue,
            'creationDate': self.creationDate,
            'adress': self.adress,
            'siren': self.siren,
            'siret': self.siret,
            'createdBy': self.createdBy
        }
