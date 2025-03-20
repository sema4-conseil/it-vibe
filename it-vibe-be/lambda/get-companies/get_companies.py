import json
import random
import uuid


def lambda_handler(event, context):
    companies = []
    
    for i in range(100):
        company = {
            "id": str(uuid.uuid4()),
            "name": f"Company_{i}",
            "location": f"Location_{i}",
            "size": str(random.randint(1, 2000)),
            "revenue": str(random.randint(100000, 1000000000)),
            "industry": f"Industry_{i}",
            "description": f"Some description _{i}",
        }
        companies.append(company)

    return {
        "statusCode": 200,
        "body": json.dumps(companies),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # Required for CORS support to work    
        }
    }
