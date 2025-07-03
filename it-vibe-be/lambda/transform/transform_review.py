import json
import boto3
import os

from logging import getLogger

logger = getLogger("TRANSFORM_REVIEW_LAMBDA")
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

DEFAULT_RESPONSE_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
}

client = boto3.client("bedrock-runtime")
system = [{"text": "Your role is to rephrase a review added by a user on it-vibe API"}]
model_id = "arn:aws:bedrock:eu-west-3:327441465709:inference-profile/eu.amazon.nova-lite-v1:0"
prompt_prefix = "Reformule ce commentaire sans ajouter des remarques te ta part: "


def lambda_handler(event, context):
    try:
        if 'body' not in event or not event['body']:
            logger.warning("Request body is missing or empty")
            raise ValueError("Request body is missing or empty")

        transformation_request = json.loads(event['body'])

        if 'content' not in transformation_request or not transformation_request["content"]:
            message = "Content is mandatory"
            logger.warning(message)
            raise ValueError(message)

        content = prompt_prefix + transformation_request["content"]

        logger.debug(f"content passed to the prompt is: \"{content}\"")

        messages = [
            {"role": "user", "content": [{"text": content}]},
        ]
        model_response = client.converse(
            modelId=model_id,
            messages=messages,
            system=system,
        )

        logger.debug("\n[Full Response]")
        logger.debug(json.dumps(model_response, indent=2))

        return {
            "statusCode": 200,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({
                "message": "Review transformed succefully",
                "response_content": model_response["output"]["message"]["content"][0]["text"],
            }),
        }

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return {
            "statusCode": 400,
            "headers": DEFAULT_RESPONSE_HEADERS,
            "body": json.dumps({"error": str(ve)}),
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": DEFAULT_RESPONSE_HEADERS
        }
