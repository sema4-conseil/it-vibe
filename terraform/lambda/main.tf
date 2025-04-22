data "archive_file" "get_companies_lambda_code" {
  type        = "zip"
  source_file = "../it-vibe-be/lambda/get-companies/get_companies.py"
  output_path = "../it-vibe-be/lambda/get-companies/get_companies.zip"
}


resource "aws_lambda_function" "get_companies_lambda" {
    filename         = data.archive_file.get_companies_lambda_code.output_path
    function_name    = "get_companies"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_companies.lambda_handler"
    runtime          = "python3.13"
    source_code_hash = data.archive_file.get_companies_lambda_code.output_base64sha256
    environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_DEV_COMPANIES"
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
}

resource "aws_lambda_function" "save_company_lambda" {
    filename         = data.archive_file.save_company_lambda_code.output_path
    function_name    = "save_company"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "save_company.lambda_handler"
    source_code_hash = data.archive_file.save_company_lambda_code.output_base64sha256
    runtime          = "python3.13"
      environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_DEV_COMPANIES"
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
    function_name    = "delete_company"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "delete_company.lambda_handler"
    source_code_hash = data.archive_file.delete_company_code.output_base64sha256
    runtime          = "python3.13"
      environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_DEV_COMPANIES"
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
    function_name    = "get_company_details"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_company_details.lambda_handler"
    runtime          = "python3.13"
    source_code_hash = data.archive_file.get_company_details_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_DEV_COMPANIES"
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
    function_name    = "get_company_review_metrics"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_company_review_metrics.lambda_handler"
    runtime          = "python3.13"
    source_code_hash = data.archive_file.get_company_review_metrics_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANY_REVIEWS_TABLE_NAME = "IT_VIBE_DEV_COMPANY_REVIEWS"
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

resource "aws_lambda_function" "get_reviews_by_company_id_lambda" {
    filename         = data.archive_file.get_reviews_by_company_id_lambda_code.output_path
    function_name    = "get_reviews_by_company_id"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_reviews_by_company_id.lambda_handler"
    runtime          = "python3.13"
    source_code_hash = data.archive_file.get_reviews_by_company_id_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANY_REVIEWS_TABLE_NAME = "IT_VIBE_DEV_COMPANY_REVIEWS"
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
    function_name    = "add_review"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "add_review.lambda_handler"
    runtime          = "python3.13"
    source_code_hash = data.archive_file.add_review_lambda_code.output_base64sha256

    environment {
        variables = {
            COMPANY_REVIEWS_TABLE_NAME = "IT_VIBE_DEV_COMPANY_REVIEWS"
        }
    }
    tags = {
        Name = "add_review"
        Env = "Dev"
        ManagedBy = "Terraform"
        Scope = "Functionnal"
    }

}

data archive_file "push_contact_message_lamnda_code" {
  type        = "zip"
  source_file  = "../it-vibe-be/lambda/push-contact-message/push_contact_message.py"
  output_path = "../it-vibe-be/lambda/push-contact-message/push_contact_message.zip"
}

resource "aws_lambda_function" "push_contact_message_lambda" {
    filename         = data.archive_file.push_contact_message_lamnda_code.output_path
    function_name    = "push_contact_message"
    role             = aws_iam_role.lambda_exec.arn
    handler          = "push_contact_message.lambda_handler"
    runtime          = "python3.13"
    source_code_hash = data.archive_file.push_contact_message_lamnda_code.output_base64sha256
}

resource "aws_iam_role" "lambda_exec" {
    name = "lambda_exec_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Sid    = ""
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
    role       = aws_iam_role.lambda_exec.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}