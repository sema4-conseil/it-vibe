variable "env"  {}
variable "log_level" {}
variable "contact_message_stream_arn" {}

variable "be_version"  {
  description = "Lambda version"
  type        = string
}

variable "pythonVersion" {
  description = "The Python version to use for the Lambda functions"
  type        = string
  default     = "python3.13"
}

data "archive_file" "get_companies_lambda_code" {
  type        = "zip"
  output_path = "../it-vibe-be/lambda/get-companies/get_companies.zip"
  source {
    content  = file("../it-vibe-be/lambda/get-companies/get_companies.py")
    filename = "get_companies.py"   
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/mappers/company_mapper.py")
    filename = "company_mapper.py"   
  }
}


resource "aws_lambda_function" "get_companies_lambda" {
    filename         = data.archive_file.get_companies_lambda_code.output_path
    function_name    = "get_companies_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_companies.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.get_companies_lambda_code.output_base64sha256
    environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_COMPANIES_${upper(var.env)}"
            VERSION       = var.be_version
            ENV           = var.env
            LOG_LEVEL     = var.log_level
        }
    }
}


data "archive_file" "save_company_lambda_code" {
  type        = "zip"
  output_path = "../it-vibe-be/lambda/save-company/save_company.zip"
  source {
    content  = file("../it-vibe-be/lambda/save-company/save_company.py")
    filename = "save_company.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/is_user_in_group.py")
    filename = "is_user_in_group.py"   
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/get_user_informations.py")
    filename = "get_user_informations.py"   
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/mappers/company_mapper.py")
    filename = "company_mapper.py"   
  }
}

resource "aws_lambda_function" "save_company_lambda" {
    filename         = data.archive_file.save_company_lambda_code.output_path
    function_name    = "save_company_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "save_company.lambda_handler"
    source_code_hash = data.archive_file.save_company_lambda_code.output_base64sha256
    runtime          = var.pythonVersion
      environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_COMPANIES_${upper(var.env)}"
        }
    }
    
}

data "archive_file" "patch_company_lambda_code" {
  type        = "zip"
  output_path = "../it-vibe-be/lambda/patch-company/patch_company.zip"
  source {
    content  = file("../it-vibe-be/lambda/patch-company/patch_company.py")
    filename = "patch_company.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/is_user_in_group.py")
    filename = "is_user_in_group.py"   
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/get_user_informations.py")
    filename = "get_user_informations.py"   
  }
}

resource "aws_lambda_function" "patch_company_lambda" {
    filename         = data.archive_file.patch_company_lambda_code.output_path
    function_name    = "patch_company_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "patch_company.lambda_handler"
    source_code_hash = data.archive_file.patch_company_lambda_code.output_base64sha256
    runtime          = var.pythonVersion
      environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_COMPANIES_${upper(var.env)}"
        }
    }
    
}

data "archive_file" "delete_company_code" {
  type        = "zip"
  output_path = "../it-vibe-be/lambda/delete-company/delete_company.zip"
  source {
    content  = file("../it-vibe-be/lambda/delete-company/delete_company.py")
    filename = "delete_company.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/is_user_in_group.py")
    filename = "is_user_in_group.py"   
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/get_user_informations.py")
    filename = "get_user_informations.py"   
  }
}

resource "aws_lambda_function" "delete_company_lambda" {
    filename         = data.archive_file.delete_company_code.output_path
    function_name    = "delete_company_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "delete_company.lambda_handler"
    source_code_hash = data.archive_file.delete_company_code.output_base64sha256
    runtime          = var.pythonVersion
      environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_COMPANIES_${upper(var.env)}"
        }
    }
}


data "archive_file" "get_company_details_lambda_code" {
  type        = "zip"
  source_file = "../it-vibe-be/lambda/get-company-details/get_company_details.py"
  output_path = "../it-vibe-be/lambda/get-company-details/get_company_details.zip"
}

resource "aws_lambda_function" "get_comany_details_lambda" {
    filename         = data.archive_file.get_company_details_lambda_code.output_path
    function_name    = "get_company_details_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_company_details.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.get_company_details_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_COMPANIES_${upper(var.env)}"
        }
    }
}

data "archive_file" "get_company_review_metrics_lambda_code" {
  type        = "zip"
  source_file = "../it-vibe-be/lambda/get-company-review-metrics/get_company_review_metrics.py"
  output_path = "../it-vibe-be/lambda/get-company-review-metrics/get_company_review_metrics.zip"
}

resource "aws_lambda_function" "get_company_review_metrics_lambda" {
    filename         = data.archive_file.get_company_review_metrics_lambda_code.output_path
    function_name    = "get_company_review_metrics_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_company_review_metrics.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.get_company_review_metrics_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANY_REVIEWS_TABLE_NAME = "IT_VIBE_COMPANY_REVIEWS_${upper(var.env)}"
        }
    }
}

# Reviews Lambda Functions
data "archive_file" "get_reviews_by_company_id_lambda_code" {
  type        = "zip"
  output_path = "../it-vibe-be/lambda/get-reviews-by-company-id/get_reviews_by_company_id.zip"
  source {
    content  = file("../it-vibe-be/lambda/get-reviews-by-company-id/get_reviews_by_company_id.py")
    filename = "get_reviews_by_company_id.py"   
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/mappers/review_mapper.py")
    filename = "review_mapper.py"   
  }
}

# Import companies from json file
data "archive_file" "import_companies_lambda_code" {
  type        = "zip"
  output_path = "../it-vibe-be/lambda/import_companies/import_companies_from_file.zip"
  source {
    content  = file("../it-vibe-be/lambda/import_companies/import_companies_from_file.py")
    filename = "import_companies_from_file.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/is_user_in_group.py")
    filename = "is_user_in_group.py"   
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/get_user_informations.py")
    filename = "get_user_informations.py"   
  }
}

resource "aws_lambda_function" "import_companies_lambda" {
    filename         = data.archive_file.import_companies_lambda_code.output_path
    function_name    = "import_companies_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "import_companies_from_file.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.import_companies_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_COMPANIES_${upper(var.env)}"
            LOG_LEVEL           = var.log_level
        }
    }
}

resource "aws_lambda_function" "get_reviews_by_company_id_lambda" {
    filename         = data.archive_file.get_reviews_by_company_id_lambda_code.output_path
    function_name    = "get_reviews_by_company_id_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_reviews_by_company_id.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.get_reviews_by_company_id_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANY_REVIEWS_TABLE_NAME = "IT_VIBE_COMPANY_REVIEWS_${upper(var.env)}"
        }
    }
}

# Reviews Lambda Functions
data "archive_file" "add_review_lambda_code" {
  type        = "zip"
  output_path = "../it-vibe-be/lambda/add-review/add_review.zip"
  source {
    content  = file("../it-vibe-be/lambda/add-review/add_review.py")
    filename = "add_review.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/get_user_informations.py")
    filename = "get_user_informations.py"   
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/mappers/review_mapper.py")
    filename = "review_mapper.py"   
  }
}

resource "aws_lambda_function" "add_review_lambda" {
    filename         = data.archive_file.add_review_lambda_code.output_path
    function_name    = "add_review_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "add_review.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.add_review_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANY_REVIEWS_TABLE_NAME = "IT_VIBE_COMPANY_REVIEWS_${upper(var.env)}"
        }
    }
}

data "archive_file" "delete_review_code" {
  type        = "zip"
  output_path = "../it-vibe-be/lambda/delete-company/delete_review.zip"
  source {
    content  = file("../it-vibe-be/lambda/delete-review/delete_review.py")
    filename = "delete_review.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/is_user_in_group.py")
    filename = "is_user_in_group.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/get_user_informations.py")
    filename = "get_user_informations.py"
  }
}

resource "aws_lambda_function" "delete_review_lambda" {
  filename         = data.archive_file.delete_review_code.output_path
  function_name    = "delete_review_${var.env}"
  role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
  handler          = "delete_review.lambda_handler"
  source_code_hash = data.archive_file.delete_review_code.output_base64sha256
  runtime          = var.pythonVersion
  environment {
    variables = {
      COMPANY_REVIEWS_TABLE_NAME = "IT_VIBE_COMPANY_REVIEWS_${upper(var.env)}"
      LOG_LEVEL = var.log_level
    }
  }
}

data archive_file "push_contact_message_lambda_code" {
  type        = "zip"
  source {
    content  = file("../it-vibe-be/lambda/contact-messages/push_contact_message.py")
    filename = "push_contact_message.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/contact-messages/message_status.py")
    filename = "message_status.py"
  }
  output_path = "../it-vibe-be/lambda/contact-messages/push_contact_message.zip"
  
}

resource "aws_lambda_function" "push_contact_message_lambda" {
    filename         = data.archive_file.push_contact_message_lambda_code.output_path
    function_name    = "push_contact_message_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "push_contact_message.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.push_contact_message_lambda_code.output_base64sha256
    environment {
        variables = {
            CONTACT_MESSAGE_TABLE_NAME = "IT_VIBE_CONTACT_MESSAGES_${upper(var.env)}"
        }
    }
}

data archive_file "get_contact_messages_lambda_code" {
  type        = "zip"
  source {
    content  = file("../it-vibe-be/lambda/contact-messages/get_contact_messages.py")
    filename = "get_contact_messages.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/contact-messages/message_status.py")
    filename = "message_status.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/is_user_in_group.py")
    filename = "is_user_in_group.py"   
  }
  output_path = "../it-vibe-be/lambda/contact-messages/get_contact_messages.zip"
}

resource "aws_lambda_function" "get_contact_messages_lambda" {
    filename         = data.archive_file.get_contact_messages_lambda_code.output_path
    function_name    = "get_contact_messages_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_contact_messages.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.get_contact_messages_lambda_code.output_base64sha256
    environment {
        variables = {
            CONTACT_MESSAGE_TABLE_NAME = "IT_VIBE_CONTACT_MESSAGES_${upper(var.env)}"
        }
    }
}

data archive_file "patch_contact_message_lambda_code" {
  type        = "zip"
  source {
    content  = file("../it-vibe-be/lambda/contact-messages/patch_contact_message.py")
    filename = "patch_contact_message.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/contact-messages/message_status.py")
    filename = "message_status.py"
  }
  source {
    content  = file("../it-vibe-be/lambda/lib/is_user_in_group.py")
    filename = "is_user_in_group.py"   
  }
  output_path = "../it-vibe-be/lambda/contact-messages/patch_contact_message.zip"
}

resource "aws_lambda_function" "patch_contact_messages_lambda" {
    filename         = data.archive_file.patch_contact_message_lambda_code.output_path
    function_name    = "patch_contact_message_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "patch_contact_message.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.patch_contact_message_lambda_code.output_base64sha256
    environment {
        variables = {
            CONTACT_MESSAGE_TABLE_NAME = "IT_VIBE_CONTACT_MESSAGES_${upper(var.env)}"
        }
    }
}

data archive_file "handle_new_contact_lambda_code" {
  type        = "zip"
  source {
    content  = file("../it-vibe-be/lambda/contact-messages/handle_new_contact.py")
    filename = "handle_new_contact.py"
  }
  output_path = "../it-vibe-be/lambda/utils/handle_new_contact.zip"
}

resource "aws_lambda_function" "handle_new_contact_lambda" {
    filename         = data.archive_file.handle_new_contact_lambda_code.output_path
    function_name    = "handle_new_contact_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoAndSesAndCloudwatchForLambda"
    handler          = "handle_new_contact.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.handle_new_contact_lambda_code.output_base64sha256
    description      = "Handle new contact lambda function for ${var.env} environment"
    environment {
        variables = {
            VERSION       = var.be_version
            ENV           = var.env
            LOG_LEVEL     = var.log_level
            CONFIG_BUCKET = "it-vibe-sema4-conseil-config"
            CONFIG_KEY    = "lambda/handle_new_contact/${var.env}/config.json"
        }
    }
}

# Event Source Mapping (Trigger)
# Allow the Lambda function to be triggered by new records in the DynamoDB stream
resource "aws_lambda_event_source_mapping" "contact_message_stream_trigger" {
  event_source_arn  = var.contact_message_stream_arn
  function_name     = aws_lambda_function.handle_new_contact_lambda.arn
  starting_position = "LATEST"
  batch_size        = 1 # Process one record at a time
}


data archive_file "health_check_lambda_code" {
  type        = "zip"
  source {
    content  = file("../it-vibe-be/lambda/utils/get_health_check.py")
    filename = "get_health_check.py"
  }
  output_path = "../it-vibe-be/lambda/utils/get_health_check.zip"
}

resource "aws_lambda_function" "health_check_lambda" {
    filename         = data.archive_file.health_check_lambda_code.output_path
    function_name    = "get_health_check_${var.env}"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_health_check.lambda_handler"
    runtime          = var.pythonVersion
    source_code_hash = data.archive_file.health_check_lambda_code.output_base64sha256
    description      = "Health check lambda function, it returns the env and version"
    environment {
        variables = {
            VERSION = var.be_version
            ENV     = var.env
        }
    }
}

data archive_file "transform_review_lambda_code" {
  type        = "zip"
  source {
    content  = file("../it-vibe-be/lambda/transform/transform_review.py")
    filename = "transform_review.py"
  }
  output_path = "../../it-vibe-be/lambda/transform/transform_review.zip"
}

resource "aws_lambda_function" "transform_review_lambda" {
  filename         = data.archive_file.transform_review_lambda_code.output_path
  function_name    = "transform_review_${var.env}"
  role             = "arn:aws:iam::327441465709:role/ITVibeBedRockForLambda"
  handler          = "transform_review.lambda_handler"
  runtime          = var.pythonVersion
  source_code_hash = data.archive_file.transform_review_lambda_code.output_base64sha256
  description      = "Lambda to transform a review using generative AI"
  environment {
    variables = {
      VERSION = var.be_version
      ENV     = var.env
      LOG_LEVEL = var.log_level
    }
  }
}