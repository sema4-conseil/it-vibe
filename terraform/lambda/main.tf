variable "get_companies_code_path" {
  default = "../it-vibe-be/lambda/get-companies/get_companies.zip"
}

variable "save_company_code_path" {
  default = "../it-vibe-be/lambda/save-company/save_company.zip"
}

variable "push_contact_message_code_path" {
  default = "../it-vibe-be/lambda/push-contact-message/push_contact_message.zip"
}

resource "aws_lambda_function" "get_companies_lambda" {
    filename         = var.get_companies_code_path
    function_name    = "get_companies"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "get_companies.lambda_handler"
    runtime          = "python3.13"
    environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_DEV_COMPANIES"
        }
    }
}



resource "aws_lambda_function" "save_company_lambda" {
    filename         = var.save_company_code_path
    function_name    = "save_company"
    role             = "arn:aws:iam::327441465709:role/DynamoDbReadWriteRole"
    handler          = "save_company.lambda_handler"
    runtime          = "python3.13"
      environment {
        variables = {
            COMPANIES_TABLE_NAME = "IT_VIBE_DEV_COMPANIES"
        }
    }
}

resource "aws_lambda_function" "push_contact_message_lambda" {
    filename         = var.push_contact_message_code_path
    function_name    = "push_contact_message"
    role             = aws_iam_role.lambda_exec.arn
    handler          = "push_contact_message.lambda_handler"
    runtime          = "python3.13"
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