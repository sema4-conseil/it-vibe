provider "aws" {
  region = "eu-west-3"
}

terraform {
  backend "s3" {
    bucket         = "it-vibe-terraform-backend-state"
    key            = "it-vibe/terraform.tfstate"
    region         = "eu-west-3" 
    encrypt        = true
  }
}

module "front-end" {
  source = "./front-end"
}

module "lambda" {
  source = "./lambda"
}

module "api-gateway" {
  source = "./api-gateway"
  get_companies_lambda_invoke_arn = module.lambda.get_companies_lambda_invoke_arn
  get_companies_lambda_arn = module.lambda.get_companies_lambda_arn
  save_company_lambda_invoke_arn = module.lambda.save_company_lambda_invoke_arn
  save_company_lambda_arn = module.lambda.save_company_lambda_arn
  push_contact_message_lambda_arn = module.lambda.push_contact_message_lambda_arn
  push_contact_message_lambda_invoke_arn = module.lambda.push_contact_message_lambda_invoke_arn
  openapi_spec_location = "../it-vibe-be/open-api/itvibe-api.yaml"
  depends_on = [ module.lambda ]
}
