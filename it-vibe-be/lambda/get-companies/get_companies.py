import json

def lambda_handler(event, context):
    companies = [
        {
            "name": "Capgemeni",
            "location": "Pune",
            "code": "C1",
            "size": "1000"
        },
        {
            "name": "TCS",
            "location": "Mumbai",
            "code": "T1",
            "size": "2000"
        },
        {
            "name": "Infosys",
            "location": "Bangalore",
            "code": "I1",
            "size": "3000"
        },
        {
            "name": "Wipro",
            "location": "Chennai",
            "code": "W1",
            "size": "4000"
        }
    ]
    
    return {
        "statusCode": 200,
        "body": json.dumps(companies),
        "headers": {
            "Content-Type": "application/json"
        }
    }