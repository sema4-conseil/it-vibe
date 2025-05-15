import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

import os

VERSION = os.environ.get('VERSION')
if not VERSION:
    raise ValueError("Environment variable 'VERSION' is not set.")

ENV = os.environ.get('ENV')
if not ENV:
    raise ValueError("Environment variable 'ENV' is not set.")

def lambda_handler(event, context):
    """
    Lambda function to check the health of the service.
    and return the version and environment.
    """
    try:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status" : "UP",
                "version" : VERSION,
                "env" : ENV
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "errorMessage": "Internal server error",
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }
        }