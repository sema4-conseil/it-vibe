import json
import os
import boto3

from logging import getLogger

logger = getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO').upper())


CONFIG_BUCKET   = os.environ.get('CONFIG_BUCKET', None)  
if not CONFIG_BUCKET:
    raise ValueError("CONFIG_BUCKET environment variable is not set")

CONFIG_KEY      = os.environ.get('CONFIG_KEY', None)
if not CONFIG_KEY:
    raise ValueError("CONFIG_KEY environment variable is not set")

ENV = os.environ.get('ENV', 'dev')


def load_config():
    """Load configuration from S3 bucket"""
    logger.debug("Loading configuration from S3 bucket: %s, key: %s", CONFIG_BUCKET, CONFIG_KEY)
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=CONFIG_BUCKET, Key=CONFIG_KEY)
        config_data = json.loads(response['Body'].read().decode('utf-8'))
        return config_data
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise

def send_email_notification(message_details):
    """
    Send email notification to admin using Amazon SES
    """
    ses_client = boto3.client('ses')
    
    subject = "New contact messages for IT Vibe"
    
    # Format the email body
    body_text = f"""
    New contact message details:
    
    Name: {message_details.get('name', 'Not provided')}
    Email: {message_details.get('email', 'Not provided')}
    Message: {message_details.get('message', 'Not provided')}
    """
    
    body_html = f"""
    <html>
        <head></head>
        <body>
            <h1>New Contact Message Received</h1>
            <h2>Details:</h2>
            <p><strong>Env:</strong> {ENV}</p>
            <p><strong>Email:</strong> {message_details.get('email', 'Not provided')}</p>
            <p><strong>Content:</strong> {message_details.get('content', 'No content')}</p>
        </body>
    </html>
    """
    config_data = load_config()
    sender_email = config_data.get('sender', None)
    admin_email= config_data.get('admin', None)
    if not sender_email or not admin_email:
        logger.error("Sender or admin email not configured in the config file")
        return False
    

    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [admin_email],
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body_text
                    },
                    'Html': {
                        'Data': body_html
                    }
                }
            }
        )
        logger.info("Email sent successfully: %s", response['MessageId'])
        return True
    except Exception as e:
        logger.error("Failed to send email: %s", str(e))
        return False
    
    

def lambda_handler(event, context):
    """
    Lambda function to handle new contact message.
    When contact message is saved into the dynamodb table, an email notification is sent to the admin.
    The email contains the contact message details.
    """
    try:
        logger.debug("Received event: %s", json.dumps(event))
        records = event.get('Records', [])
        contactMessage = records[0].get('dynamodb', {}).get('NewImage', None)
        if not contactMessage:
            raise ValueError("No contact message found in the event")
        
        logger.debug("Processing contact message: %s", contactMessage.get('Id', {}).get('S', 'Unknown ID'))

        message_details = {  
            "email": contactMessage.get('email', {}).get('S', 'Not provided'),
            "content": contactMessage.get('content', {}).get('S', 'No content'),
        }

        email_sent = send_email_notification(message_details)

        if not email_sent:
            logger.warning("Failed to send email notification")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Contact message processed successfully"
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            }
        }

    except Exception as e:
        logger.error("Error processing event: %s", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "errorMessage": "Internal server error"
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            }
        }
