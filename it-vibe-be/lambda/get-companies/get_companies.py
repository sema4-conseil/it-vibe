import json
import random
import uuid


def lambda_handler(event, context):
    companies = []
    for i in range(100):
        company = {
            "name": f"Company_{i}",
            "location": f"Location_{i}",
            "code": str(uuid.uuid4()),
            "size": str(random.randint(1, 2000))
        }
        companies.append(company)

    return {
        "statusCode": 200,
        "body": json.dumps(companies),
        "headers": {
            "Content-Type": "application/json"
        }
    }
