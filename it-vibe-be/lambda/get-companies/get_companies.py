import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import logging
from company_mapper import map

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('COMPANIES_TABLE_NAME')
if not table_name:
    raise ValueError("Environment variable 'COMPANIES_TABLE_NAME' is not set.")
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        startKey = None
        pageSize = 5  # Default page size
        name_value = None
        siren_value = None
        siret_value = None

        if event and event.get('queryStringParameters'):
            query_params = event['queryStringParameters']
            startKey = query_params.get('startKey')
            pageSize = int(query_params.get('pageSize', 5))
            name_value = query_params.get("name")
            siren_value = query_params.get("siren")
            siret_value = query_params.get("siret")
        
        if not isinstance(pageSize, int) or pageSize <= 0:
            raise ValueError("pageSize must be a positive integer.")

        filter_expression = None
        scan_kwargs = {'Limit': pageSize}

        if startKey:
            try:
                scan_kwargs['ExclusiveStartKey'] = json.loads(startKey)
            except json.JSONDecodeError:
                raise ValueError("Invalid format for startKey.")

        if name_value:
            name_lower = name_value.lower()
            filter_expression = Attr("name_lowercase").contains(name_lower)
        
        if siren_value:
            condition = Attr("siren").eq(siren_value)
            filter_expression = condition if not filter_expression else filter_expression & condition

        if siret_value:
            condition = Attr("siret").eq(siret_value)
            filter_expression = condition if not filter_expression else filter_expression & condition
        
        if filter_expression:
            scan_kwargs['FilterExpression'] = filter_expression
        
        # Perform the scan
        items = []
        while len(items) < pageSize:
            result = table.scan(**scan_kwargs)
            items.extend(result.get('Items', []))
            
            # Capture the LastEvaluatedKey from the result
            last_evaluated_key = result.get('LastEvaluatedKey')

            # Break if no more items to scan
            if not last_evaluated_key:
                break

            # Update for next iteration
            scan_kwargs['ExclusiveStartKey'] = result['LastEvaluatedKey']

        # Limit the items to the requested page size
        response_items = items[:pageSize]
        mapped_items = [map(item) for item in response_items]
        response = {
            "items": mapped_items,
            "LastEvaluatedKey": last_evaluated_key,
            "Count": len(response_items),
        }


        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        }

    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(ve)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
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