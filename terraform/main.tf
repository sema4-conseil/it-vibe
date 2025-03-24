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

variable "hosted_zone_id" {
  default = "Z09606333IIM9GKOYXW0S"
}

module "front-end" {
  source = "./front-end"
  hosted_zone_id = var.hosted_zone_id
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
  hosted_zone_id = var.hosted_zone_id
  depends_on = [ module.lambda ]
}
